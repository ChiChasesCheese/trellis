"""可靠的工具调用智能体练习骨架。公开 API 与 `solution.py` 一致，`run_agent` 可原样放进真实工作区的 `service.py`。

产品规则（逐条都有测试）：
 1. 入口校验：`question` 必须是 `str`（空串可以）；`tools` 把非空名字映射到可调用对象；
    `max_turns` 是正的精确 `int`，`max_tool_calls` 是非负的精确 `int`，`max_workers` 是正的精确 `int`，
    布尔值和浮点数都无效。违规抛 `ValueError`，且此时模型一次也没有被调用。
 2. 对话记录以 `{"role": "user", "content": question}` 开头；每次调模型，传完整记录的深拷贝；
    每个响应按 `{"role": "assistant", "content": text, "tool_calls": calls}` 追加。
 3. 没有工具调用的响应是终止响应（空文本也算）；带调用的响应里，文本只是中间文字。
    成功时恰好返回 `{"answer", "messages", "model_calls", "tool_calls"}` 四个键，记录里含最后一条 assistant 消息。
 4. 模型响应必须恰好是 `{"text": str, "tool_calls": list}`；每个调用恰好有 `id`、`name`、`arguments`；
    id 与 name 是非空字符串，arguments 是键为字符串的字典，值只能是 JSON 值
    （`None`、精确的 bool/int、有限 float、str、元素合法的 list、键为字符串的 dict）；
    元组、非字符串键、NaN、无穷、任意对象都无效。整个响应先校验完，再执行任何工具，违规抛 `ValueError`。
 5. 同一个响应里先预检、后执行：同 ID 但名字或参数不同抛 `ValueError`；新 ID 的个数超过剩余工具预算抛
    `RuntimeError("tool budget exceeded")`，这个响应的工具一个都不执行，之前批次的结果不回滚。
 6. 参数相等按 JSON 文本判断：键排序、分隔符 `(",", ":")`、`ensure_ascii=False`；键的顺序无关，
    数组顺序和数字写法（`1` 与 `1.0`）有关。
 7. 每个不同的 ID 只执行一次，算一次工具尝试（未知工具和出错的也算）；同名同参的重复 ID，不论在同一响应内还是
    之后的响应里，都直接重放缓存，不再执行、不再计数，但每次出现仍各得一条结果。缓存按运行隔离。
 8. 一个批次里互不相同的调用并发执行，同时活跃的不超过 `max_workers`；`max_workers > 1` 时它们必须能重叠。
    `max_workers == 1` 时按首次出现的顺序执行。结果按请求顺序追加，与谁先完成无关。
 9. 每条结果是 `{"role": "tool", "tool_call_id", "name", "content"}`，成功时 content 是
    `{"ok": True, "value": 结果}`；未知工具是 `{"ok": False, "error": "unknown_tool"}`；已知工具抛出任何
    `Exception`（含参数绑定错误）或返回非 JSON 值，是 `{"ok": False, "error": "tool_error"}`，不带异常文本。
    出错不取消同批其余调用。
10. 整批结束之后才进入下一次模型调用、返回或抛预算错误；`run_agent` 结束时不留任何线程。
11. 预算：每次模型调用算一轮；最后一轮允许的响应若仍请求工具，先把这个批次处理完，再抛
    `RuntimeError("model budget exceeded")`，不再多调一次模型。
12. 异常：模型自己抛出的异常原样传出；工具抛出的非 `Exception`（`BaseException`）在同批已启动的调用结束后原样传出。
13. 数据所有权：模型响应、传给工具的参数、工具结果、模型看到的快照全部深拷贝；模型和工具事后改自己手里的对象，
    不能改动记录和缓存。工具注册表在运行开始时复制。模型文本和工具输出永远不当作代码或指令执行。
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

Tool = Callable[..., Any]
Model = Callable[[list[dict[str, Any]]], Any]

UNKNOWN_TOOL: dict[str, Any] = {"ok": False, "error": "unknown_tool"}
TOOL_ERROR: dict[str, Any] = {"ok": False, "error": "tool_error"}


def is_json(value: object) -> bool:
    raise NotImplementedError


def canonical(arguments: Mapping[str, Any]) -> str:
    raise NotImplementedError


@dataclass(frozen=True)
class Limits:
    max_turns: int
    max_tool_calls: int
    max_workers: int

    def __post_init__(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]

    @property
    def signature(self) -> tuple[str, str]:
        raise NotImplementedError

    def wire(self) -> dict[str, Any]:
        raise NotImplementedError


def parse_response(raw: object) -> tuple[str, list[ToolCall]]:
    raise NotImplementedError


class ReplayCache:
    def __init__(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def admit(self, calls: Sequence[ToolCall]) -> list[ToolCall]:
        raise NotImplementedError

    def store(self, call: ToolCall, content: dict[str, Any]) -> None:
        raise NotImplementedError

    def replay(self, call_id: str) -> dict[str, Any]:
        raise NotImplementedError


class BatchRunner:
    def __init__(self, tools: Mapping[str, Tool], max_workers: int) -> None:
        raise NotImplementedError

    def run(self, calls: Sequence[ToolCall]) -> list[dict[str, Any]]:
        raise NotImplementedError


class AgentRun:
    def __init__(self, question: str, model: Model, tools: Mapping[str, Tool], limits: Limits) -> None:
        raise NotImplementedError

    def run(self) -> dict[str, Any]:
        raise NotImplementedError


def run_agent(question: str, model: Model, tools: Mapping[str, Tool], *, max_turns: int = 4,
              max_tool_calls: int = 8, max_workers: int = 4) -> dict[str, Any]:
    raise NotImplementedError
