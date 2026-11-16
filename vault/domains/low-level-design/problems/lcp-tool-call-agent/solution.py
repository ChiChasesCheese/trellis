"""可靠的工具调用智能体：模型与工具交替运行的有界循环。

设计分五层，各管一件事：
1. `Limits` 在第一次调用模型之前校验三个预算（精确的 int，布尔无效）。
2. `parse_response` 把模型输出一次性校验完并深拷贝成 `ToolCall`，之后循环只处理自己拥有的数据。
3. `ReplayCache` 按调用 ID 记住已执行的结果，同一 ID 同名同参直接重放，名字或参数不同则拒绝。
4. `BatchRunner` 在 worker 上限内并发执行一批互不相同的调用，结果按请求顺序返回，返回前所有线程已结束。
5. `AgentRun` 持有对话记录与计数器，按「预检 → 执行 → 按序追加」处理每个响应，`run_agent` 只是入口。
"""

from __future__ import annotations

import copy
import json
import math
import threading
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

Tool = Callable[..., Any]
Model = Callable[[list[dict[str, Any]]], Any]

UNKNOWN_TOOL: dict[str, Any] = {"ok": False, "error": "unknown_tool"}
TOOL_ERROR: dict[str, Any] = {"ok": False, "error": "tool_error"}


def is_json(value: object) -> bool:
    """协议里的 JSON 值：None、精确的 bool/int/str、有限 float、元素合法的 list、键为 str 的 dict。"""
    kind = type(value)
    if value is None or kind in (bool, int, str):
        return True
    if kind is float:
        return math.isfinite(value)  # type: ignore[arg-type]
    try:
        if isinstance(value, list):
            return all(is_json(item) for item in value)
        if isinstance(value, dict):
            return all(isinstance(k, str) and is_json(v) for k, v in value.items())
    except RecursionError:  # 嵌套过深按非法处理，不让它变成别的异常
        return False
    return False


def canonical(arguments: Mapping[str, Any]) -> str:
    """参数相等的判据：键排序、紧凑分隔符、不转义非 ASCII；数组顺序与数字写法（1 与 1.0）保留。"""
    return json.dumps(arguments, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class Limits:
    """三个预算，构造即校验：违规抛 ValueError，此时模型一次也没有被调用。"""

    max_turns: int
    max_tool_calls: int
    max_workers: int

    def __post_init__(self) -> None:
        for name, value, floor in (("max_turns", self.max_turns, 1),
                                   ("max_tool_calls", self.max_tool_calls, 0),
                                   ("max_workers", self.max_workers, 1)):
            if type(value) is not int or value < floor:  # 布尔和浮点都不是精确的 int
                raise ValueError(f"{name} must be an int >= {floor}, got {value!r}")


@dataclass(frozen=True)
class ToolCall:
    """一次工具调用请求。`arguments` 是解析时做的私有深拷贝：执行时再给工具一份拷贝，对话记录直接引用它。"""

    id: str
    name: str
    arguments: dict[str, Any]

    @property
    def signature(self) -> tuple[str, str]:
        return (self.name, canonical(self.arguments))

    def wire(self) -> dict[str, Any]:
        """写进对话记录的形状。"""
        return {"id": self.id, "name": self.name, "arguments": self.arguments}


def parse_response(raw: object) -> tuple[str, list[ToolCall]]:
    """校验整个模型响应（任何工具执行之前），通过后深拷贝；畸形输出抛 ValueError。"""
    if not isinstance(raw, dict) or set(raw) != {"text", "tool_calls"}:
        raise ValueError("model response must be a dict with exactly text and tool_calls")
    text, items = raw["text"], raw["tool_calls"]
    if not isinstance(text, str) or not isinstance(items, list):
        raise ValueError("text must be a str and tool_calls a list")
    calls: list[ToolCall] = []
    for item in items:
        if not isinstance(item, dict) or set(item) != {"id", "name", "arguments"}:
            raise ValueError("a tool call must be a dict with exactly id, name and arguments")
        call_id, name, arguments = item["id"], item["name"], item["arguments"]
        if not (isinstance(call_id, str) and call_id and isinstance(name, str) and name):
            raise ValueError("tool call id and name must be nonempty strings")
        if not isinstance(arguments, dict) or not is_json(arguments):
            raise ValueError("tool call arguments must be a dict of JSON values")
        calls.append(ToolCall(call_id, name, copy.deepcopy(arguments)))
    return text, calls


class ReplayCache:
    """按调用 ID 记住 (名字, 参数文本) 与结果；缓存里的条目数就是已用的工具尝试数。"""

    def __init__(self) -> None:
        self._entries: dict[str, tuple[tuple[str, str], dict[str, Any]]] = {}

    def __len__(self) -> int:
        return len(self._entries)

    def admit(self, calls: Sequence[ToolCall]) -> list[ToolCall]:
        """预检整个响应：同 ID 不同名或不同参数抛 ValueError；返回真正要执行的新 ID（首次出现顺序）。"""
        seen: dict[str, tuple[str, str]] = {}
        fresh: list[ToolCall] = []
        for call in calls:
            known = self._entries.get(call.id)
            previous = known[0] if known else seen.get(call.id)
            if previous is not None and previous != call.signature:
                raise ValueError(f"call id {call.id!r} reused with a different name or arguments")
            if previous is None:
                seen[call.id] = call.signature
                fresh.append(call)
        return fresh

    def store(self, call: ToolCall, content: dict[str, Any]) -> None:
        self._entries[call.id] = (call.signature, content)

    def replay(self, call_id: str) -> dict[str, Any]:
        """每次出现拿到独立的副本，改一份不会影响缓存和别的消息。"""
        return copy.deepcopy(self._entries[call_id][1])


class BatchRunner:
    """在 worker 上限内并发执行一批互不相同的调用；返回或抛出之前，所有已启动的线程都已结束。"""

    def __init__(self, tools: Mapping[str, Tool], max_workers: int) -> None:
        self._tools = dict(tools)  # 运行开始时复制注册表，之后外部改它不影响本次运行
        self._max_workers = max_workers

    def run(self, calls: Sequence[ToolCall]) -> list[dict[str, Any]]:
        if not calls:
            return []
        halted = threading.Event()  # 某个工具抛了非 Exception 的异常后，还没开始的调用不再启动
        with ThreadPoolExecutor(max_workers=min(self._max_workers, len(calls))) as pool:
            futures = [pool.submit(self._invoke, call, halted) for call in calls]
            outcomes = [future.result() for future in futures]  # 离开 with 时线程池 join 全部线程
        for _, fatal in outcomes:
            if fatal is not None:
                raise fatal
        return [content for content, _ in outcomes if content is not None]

    def _invoke(self, call: ToolCall, halted: threading.Event
                ) -> tuple[dict[str, Any] | None, BaseException | None]:
        """返回 (结果内容, 致命异常)；任何工具失败都在这里收口，不会漏出线程。"""
        if halted.is_set():
            return None, None
        tool = self._tools.get(call.name)
        if tool is None:
            return copy.deepcopy(UNKNOWN_TOOL), None
        try:
            value = tool(**copy.deepcopy(call.arguments))
            if not is_json(value):
                return copy.deepcopy(TOOL_ERROR), None
            return {"ok": True, "value": copy.deepcopy(value)}, None
        except Exception:  # 绑定错误、工具自己的异常：只给模型一个固定的错误码，不带异常文本
            return copy.deepcopy(TOOL_ERROR), None
        except BaseException as fatal:  # KeyboardInterrupt 之类：等同批已启动的调用结束后原样抛出
            halted.set()
            return None, fatal


class AgentRun:
    """一次运行的全部可变状态：对话记录、重放缓存、模型调用计数。"""

    def __init__(self, question: str, model: Model, tools: Mapping[str, Tool], limits: Limits) -> None:
        self._model = model
        self._limits = limits
        self._runner = BatchRunner(tools, limits.max_workers)
        self._cache = ReplayCache()
        self._messages: list[dict[str, Any]] = [{"role": "user", "content": question}]
        self._model_calls = 0

    def run(self) -> dict[str, Any]:
        for _ in range(self._limits.max_turns):
            raw = self._model(copy.deepcopy(self._messages))  # 模型拿到的是快照
            self._model_calls += 1
            text, calls = parse_response(raw)
            self._messages.append({"role": "assistant", "content": text,
                                   "tool_calls": [call.wire() for call in calls]})
            if not calls:
                return {"answer": text, "messages": self._messages,
                        "model_calls": self._model_calls, "tool_calls": len(self._cache)}
            self._run_batch(calls)
        raise RuntimeError("model budget exceeded")  # 最后一轮的批次已经处理完才报

    def _run_batch(self, calls: list[ToolCall]) -> None:
        fresh = self._cache.admit(calls)  # 冲突与预算都在启动任何线程之前判定
        if len(fresh) > self._limits.max_tool_calls - len(self._cache):
            raise RuntimeError("tool budget exceeded")
        for call, content in zip(fresh, self._runner.run(fresh)):
            self._cache.store(call, content)
        for call in calls:  # 每次出现各一条结果，顺序与请求一致
            self._messages.append({"role": "tool", "tool_call_id": call.id, "name": call.name,
                                   "content": self._cache.replay(call.id)})


def run_agent(question: str, model: Model, tools: Mapping[str, Tool], *, max_turns: int = 4,
              max_tool_calls: int = 8, max_workers: int = 4) -> dict[str, Any]:
    """运行智能体循环，返回 answer、完整对话记录和两个计数。"""
    if not isinstance(question, str):
        raise ValueError("question must be a string")
    if not isinstance(tools, Mapping) or not all(
            isinstance(name, str) and name and callable(tool) for name, tool in tools.items()):
        raise ValueError("tools must map nonempty names to callables")
    limits = Limits(max_turns, max_tool_calls, max_workers)
    return AgentRun(question, model, tools, limits).run()


if __name__ == "__main__":
    replies = iter([
        {"text": "Checking both prices", "tool_calls": [
            {"id": "a", "name": "price", "arguments": {"symbol": "A"}},
            {"id": "b", "name": "price", "arguments": {"symbol": "B"}}]},
        {"text": "A is cheaper", "tool_calls": []},
    ])
    result = run_agent("Compare A and B", lambda messages: next(replies),
                       {"price": lambda symbol: {"A": 100, "B": 200}[symbol]}, max_workers=2)
    print(result["answer"], result["model_calls"], result["tool_calls"])
