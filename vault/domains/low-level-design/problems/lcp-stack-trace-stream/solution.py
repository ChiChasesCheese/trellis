"""流式调用栈处理器（Streaming Stack Trace Processor）参考解。

设计五句话：
1. 转换器只记住"上一次观察到的完整栈"和"每一层前缀连续出现了几次（封顶 N）"，状态大小只和栈深有关。
2. 一层栈帧由它的完整前缀识别，所以只比较两个栈的最长公共前缀，前缀之外的旧帧结束、新帧开始。
3. "是否已确认"不单独存：连续次数等于 N 就是已确认，快照因此只有两个数组，恢复后行为逐字相同。
4. 每个采样先整体校验、复制，再一次性写入状态；失败的调用不留任何痕迹。
5. `convert_samples` 与 `compress_samples` 都是生成器：先产出手上已完成的结果，再读下一个采样。
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Any

SNAPSHOT_KEYS = frozenset({"version", "confirmations", "last_ts", "previous", "streaks"})


@dataclass(frozen=True)
class Sample:
    """一次采样：时间戳和从最外层到最内层的栈。"""

    ts: float
    stack: tuple[str, ...]


@dataclass(frozen=True)
class Event:
    """一次观察到的转移：kind 只有 "start" 和 "end"。"""

    kind: str
    ts: float
    name: str


@dataclass(frozen=True)
class StackRun:
    """相邻且完全相同的栈合并成一段：首尾采样时间和采样个数。"""

    start: float
    end: float
    stack: tuple[str, ...]
    count: int


# ---------------------------------------------------------------- 校验：只读、不改任何状态

def check_confirmations(value: Any) -> int:
    """确认次数必须是正的 int；bool 是 int 的子类，所以用 type() 精确比较。"""
    if type(value) is not int or value < 1:
        raise ValueError(f"confirmations must be a positive int, got {value!r}")
    return value


def check_timestamp(ts: Any, last: float | None) -> float:
    """精确类型 int 或 float、有限、非负，并且严格大于上一个时间戳。

    int 与 float 直接用 Python 的精确比较；绝不把 int 转成 float，否则 2**53 与 2**53+1 会变成同一个数。
    `math.isfinite` 只对 float 调用：对超出 float 范围的大整数它会溢出。
    """
    kind = type(ts)
    if kind is not int and kind is not float:
        raise ValueError(f"timestamp must be int or float, got {kind.__name__}")
    if kind is float and not math.isfinite(ts):
        raise ValueError(f"timestamp must be finite, got {ts!r}")
    if ts < 0:
        raise ValueError(f"timestamp must be nonnegative, got {ts!r}")
    if last is not None and ts <= last:
        raise ValueError(f"timestamp must increase: {ts!r} after {last!r}")
    return ts


def check_names(names: Any) -> tuple[str, ...]:
    """栈必须是由非空字符串组成的 list 或 tuple；返回一份拷贝，调用方之后再改也不影响状态。"""
    if not isinstance(names, (list, tuple)):
        raise ValueError(f"stack must be a list or tuple, got {type(names).__name__}")
    copy = tuple(names)
    for name in copy:
        if not isinstance(name, str) or not name:
            raise ValueError(f"frame name must be a nonempty string, got {name!r}")
    return copy


def check_sample(sample: Sample, last: float | None) -> tuple[float, tuple[str, ...]]:
    """校验整个采样并返回干净的 (时间戳, 栈拷贝)；任何一项不合格都在写入之前抛出。"""
    return check_timestamp(sample.ts, last), check_names(sample.stack)


def check_snapshot(state: Any) -> tuple[int, float | None, list[str], list[int]]:
    """快照的结构检查：五个键、版本、数组等长、连续次数在 1..N 且父层不小于子层。"""
    if not isinstance(state, dict) or set(state) != SNAPSHOT_KEYS:
        raise ValueError("snapshot must be a dict with exactly the five snapshot keys")
    if type(state["version"]) is not int or state["version"] != 1:
        raise ValueError(f"unsupported snapshot version {state['version']!r}")
    n = check_confirmations(state["confirmations"])
    previous, streaks, last = state["previous"], state["streaks"], state["last_ts"]
    if not isinstance(previous, list) or not isinstance(streaks, list) or len(previous) != len(streaks):
        raise ValueError("previous and streaks must be lists of equal length")
    names = list(check_names(previous))
    if last is None:
        if names:
            raise ValueError("last_ts is None only when both lists are empty")
    else:
        check_timestamp(last, None)
    for i, count in enumerate(streaks):
        if type(count) is not int or not 1 <= count <= n:
            raise ValueError(f"streak {count!r} must be an int in 1..{n}")
        if i and count > streaks[i - 1]:
            raise ValueError("a parent's streak must be at least its child's")
    return n, last, names, list(streaks)


def shared_prefix(a: list[str], b: tuple[str, ...]) -> int:
    """两个栈从最外层起相同的帧数。"""
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


# ---------------------------------------------------------------- 转换器

class TraceConverter:
    """把一串采样逐个转换成 start/end 事件。

    状态只有四项：确认次数 N、上一个时间戳、上一个观察到的栈（含还没确认的帧）、
    每一层前缀的连续观察次数（封顶 N）。已确认的帧恰好是 streaks 中等于 N 的那一段前缀。
    """

    def __init__(self, confirmations: int = 1) -> None:
        self._n = check_confirmations(confirmations)
        self._last_ts: float | None = None
        self._previous: list[str] = []
        self._streaks: list[int] = []

    def feed(self, sample: Sample) -> list[Event]:
        """处理一个采样：先校验，再算事件，最后一次性写入状态。"""
        ts, stack = check_sample(sample, self._last_ts)
        n, old = self._n, self._streaks
        keep = shared_prefix(self._previous, stack)  # 保留的公共前缀
        active = sum(1 for count in old if count == n)  # 旧栈里已确认的层数，总是一段前缀
        # 先结束：只结束已确认且不在公共前缀里的旧帧，从叶子到根
        events = [Event("end", ts, self._previous[i]) for i in range(active - 1, keep - 1, -1)]
        # 公共前缀的连续次数加一，其余层是新前缀，从 1 开始
        streaks = [min(n, old[i] + 1) for i in range(keep)] + [1] * (len(stack) - keep)
        # 再开始：本次刚满 N 的层，从根到叶；已经确认且保留的层不会重复开始
        events += [Event("start", ts, stack[i]) for i in range(min(keep, active), len(stack)) if streaks[i] == n]
        self._last_ts, self._previous, self._streaks = ts, list(stack), streaks
        return events

    def snapshot(self) -> dict:
        """导出全部状态；两个数组是拷贝，调用方改它们不会影响转换器。"""
        return {
            "version": 1,
            "confirmations": self._n,
            "last_ts": self._last_ts,
            "previous": list(self._previous),
            "streaks": list(self._streaks),
        }

    @classmethod
    def from_snapshot(cls, state: dict) -> TraceConverter:
        """校验通过之后恢复出一个新的转换器；不产生任何事件，也不共享调用方的列表。"""
        n, last, previous, streaks = check_snapshot(state)
        converter = cls(n)
        converter._last_ts, converter._previous, converter._streaks = last, previous, streaks
        return converter


# ---------------------------------------------------------------- 惰性流

def convert_samples(samples: Iterable[Sample], confirmations: int = 1) -> Iterator[Event]:
    """惰性转换。确认次数在调用时就校验（不读任何采样）；采样要等第一次迭代才开始读。"""
    return _stream_events(TraceConverter(confirmations), samples)


def _stream_events(converter: TraceConverter, samples: Iterable[Sample]) -> Iterator[Event]:
    for sample in samples:
        yield from converter.feed(sample)  # 当前采样的事件产完，才会读下一个采样


def compress_samples(samples: Iterable[Sample]) -> Iterator[StackRun]:
    """把相邻且完全相同的栈合并成段。读到第一个不同的采样就立刻产出前一段，不再往前看。"""
    last: float | None = None
    start = end = 0.0
    stack: tuple[str, ...] | None = None
    count = 0
    for sample in samples:
        ts, names = check_sample(sample, last)
        last = ts
        if names == stack:
            end, count = ts, count + 1
            continue
        if stack is not None:
            yield StackRun(start, end, stack, count)
        start, end, stack, count = ts, ts, names, 1
    if stack is not None:
        yield StackRun(start, end, stack, count)


if __name__ == "__main__":
    demo = [Sample(1, ("main",)), Sample(2, ("main", "read")), Sample(3, ("main", "write")), Sample(4, ())]
    for event in convert_samples(demo):
        print(event)
