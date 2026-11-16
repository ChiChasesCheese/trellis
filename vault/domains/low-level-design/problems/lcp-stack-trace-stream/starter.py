"""流式调用栈处理器练习骨架。公开 API 与 `solution.py` 一致；三个记录类已经给好，其余方法体待补全。

产品规则（逐条都有测试）：
 1. `Sample(ts, stack)` 的 stack 从最外层到最内层。`confirmations=1` 时：第一个采样按从根到叶的顺序全部开始；
    之后每个采样保留最长公共前缀，先按从叶到根结束旧后缀，再按从根到叶开始新后缀；事件的时间戳都是当前采样的，名字原样。
    栈完全相同什么也不产生；空栈结束所有已开始的帧；输入耗尽时不额外产生结束事件（采样之间的真实执行不可知）。
 2. 栈帧由完整的有序前缀识别（含深度与所有父帧），不是只看名字：递归的同名帧在不同深度是不同的帧；
    根变了，叶子同名也要先结束再开始。不推断两个采样之间没观察到的调用。事件是 `Event(kind, ts, name)`，kind 只有 "start" 与 "end"。
 3. `confirmations` 必须是精确类型 int 且为正，否则 ValueError（bool 也不行）。N > 1 时，一个帧要在同一完整前缀连续出现的第 N 个采样才开始，
    用确认那个采样的时间戳，不回填。保留下来的父帧在子帧变化时保留自己的连续次数；中断一次就把受影响的次数清零，分开的几段不累加。
    已确认的帧在前缀消失的那个采样立刻结束，且先于任何新帧的开始；未确认的帧从不产生结束事件。每个转换器的状态互相独立。
 4. `convert_samples` 产生的事件与新建转换器逐个 `feed` 完全相同；必须惰性：开始迭代之前不读任何采样，
    当前采样的事件还没产完就不读下一个；只保留与最大栈深成正比的状态，不保留全部历史。
    `compress_samples` 把相邻且完全相同的完整栈合成 `StackRun(start, end, stack, count)`：start/end 是第一个和最后一个被合并采样的时间戳，
    stack 是 tuple，count 是采样个数；空栈也是合法的栈；不相邻的相同栈是两段；读到第一个不同的采样就先产出前一段；空输入什么也不产出；不做确认过滤。
 5. 时间戳必须是精确类型 int 或 float、有限、非负，并且在同一条流内严格递增；bool、NaN、无穷、重复或倒退的时间戳、其他类型都抛 ValueError。
    大整数（甚至超出 float 范围）按精确数值比较，int 与 float 混用也一样，绝不把 int 转成 float。
    栈必须是由非空字符串组成的 list 或 tuple（空白与 Unicode 名字合法，原样保留），名字不合格抛 ValueError。
    先校验并复制整个栈，再改状态：失败的 `feed` 不消耗它的时间戳，也不影响连续次数。`compress_samples` 读取输入时做同样的校验；已经产出的结果不能撤回。
 6. `snapshot()` 返回恰好 {"version": 1, "confirmations": N, "last_ts": 时间戳或 None, "previous": [名字], "streaks": [次数]}：
    previous 是最后观察到的栈（含未确认的帧），streaks 是每一层前缀的连续观察次数，封顶 N。还没有采样时 last_ts 是 None 且两个数组为空；
    空栈采样之后 last_ts 是它的时间戳。`from_snapshot(state)` 恢复出新转换器，不产生事件；之后用相同的采样继续，
    事件必须和不中断时完全一样（含未确认的帧和仍然开着的递归帧）；下一个时间戳必须严格大于保存的时间戳。
 7. 非法快照抛 ValueError：必须是 dict 且恰好五个键；version 是精确的 int 1；confirmations 是正的精确 int；
    两个数组都是 list 且等长；名字按采样规则；非 None 的时间戳按采样时间戳规则；None 要求两个数组都空；
    每个次数是 1..N 的精确 int，且父层不小于子层。快照输出与恢复出的状态都不和调用方、也不和别的转换器共享列表。

`Sample`、`Event`、`StackRun` 在真实工作区里来自只读的 `records.py`，这里为了单文件自洽把它们写在一起，字段完全一致。
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Sample:
    ts: float
    stack: tuple[str, ...]


@dataclass(frozen=True)
class Event:
    kind: str
    ts: float
    name: str


@dataclass(frozen=True)
class StackRun:
    start: float
    end: float
    stack: tuple[str, ...]
    count: int


class TraceConverter:
    def __init__(self, confirmations: int = 1) -> None:
        raise NotImplementedError

    def feed(self, sample: Sample) -> list[Event]:
        raise NotImplementedError

    def snapshot(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_snapshot(cls, state: dict) -> TraceConverter:
        raise NotImplementedError


def convert_samples(samples: Iterable[Sample], confirmations: int = 1) -> Iterator[Event]:
    raise NotImplementedError


def compress_samples(samples: Iterable[Sample]) -> Iterator[StackRun]:
    raise NotImplementedError
