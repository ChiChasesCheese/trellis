"""交通信号灯（Traffic Signal）——练习骨架：公开 API 与参考解一致，方法体全部待补。

把每个 `raise NotImplementedError` 换成你自己的实现；内部表示随你选（冲突怎么存、相位怎么
轮转），测试只断言公开行为与只读视图（`aspects`、`stage`、`queue_count`、
`conflicting_permissive()`），不会碰任何私有属性。全程不许 `sleep`，时间只从 `clock` 进来。
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol

Clock = Callable[[], datetime]


class SignalError(Exception):
    """本设计全部失败路径的公共基类。"""


class UnknownMovementError(SignalError):
    """这个流向不属于本路口。"""


class ConflictingPhaseError(SignalError):
    """相位里放进了两个互相冲突的流向。"""


class SafetyViolationError(SignalError):
    """运行中两个冲突流向同时放行了。"""


class Aspect(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    DONT_WALK = "dont_walk"
    WALK = "walk"
    FLASHING_DONT_WALK = "flashing_dont_walk"

    @property
    def permissive(self) -> bool:
        """此刻是否允许进入路口；黄灯与闪烁的禁止通行都不是放行。"""
        raise NotImplementedError


class MovementKind(Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class Stage(Enum):
    GREEN = "green"
    CLEARANCE = "clearance"
    ALL_RED = "all_red"


@dataclass(frozen=True, slots=True)
class Movement:
    """一个流向：一股交通流或一条人行横道。引擎只问它 `go` / `clear` / `stop` 三个问题。"""

    name: str
    kind: MovementKind = MovementKind.VEHICLE

    @property
    def go(self) -> Aspect:
        raise NotImplementedError

    @property
    def clear(self) -> Aspect:
        raise NotImplementedError

    @property
    def stop(self) -> Aspect:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Phase:
    """一组同时放行的流向，加上最短绿与最长绿。"""

    name: str
    movements: frozenset[Movement]
    min_green: int = 4
    max_green: int = 12

    def serves(self, movement: Movement) -> bool:
        raise NotImplementedError


class Intersection:
    """路口的几何：有哪些流向、哪两个流向互相冲突。"""

    def __init__(self, name: str, movements: Iterable[Movement],
                 conflicts: Iterable[tuple[Movement, Movement]]) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def movements(self) -> tuple[Movement, ...]:
        raise NotImplementedError

    def conflicting_with(self, movement: Movement) -> frozenset[Movement]:
        raise NotImplementedError

    def conflicts(self, left: Movement, right: Movement) -> bool:
        raise NotImplementedError

    def validate_phase(self, phase: Phase) -> None:
        """相位内部不能有互相冲突的流向；违反就抛 `ConflictingPhaseError`。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class PhaseContext:
    """交给配时方案的只读快照。"""

    phase: Phase
    elapsed: int
    tick: int
    waiting: int
    gap_since_arrival: int


class TimingPlan(Protocol):
    """配时方案：绿灯还要不要再保持一个 tick。"""

    def hold(self, ctx: PhaseContext) -> bool:
        ...


class FixedTimePlan:
    """定周期：每个相位绿多久写死在方案里。"""

    def __init__(self, green: Mapping[str, int] | None = None, default: int = 10) -> None:
        raise NotImplementedError

    def hold(self, ctx: PhaseContext) -> bool:
        raise NotImplementedError


class ActuatedPlan:
    """感应式：最短绿之后只要车还在陆续到达就延长，直到最长绿。`gap` 是断流间隔。"""

    def __init__(self, gap: int = 3) -> None:
        raise NotImplementedError

    def hold(self, ctx: PhaseContext) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class TickReport:
    """一个 tick 之后路口的完整状态；`aspects` 是快照，不是控制器的活字典。"""

    tick: int
    at: datetime
    stage: Stage
    phase_name: str
    aspects: Mapping[Movement, Aspect]
    preempted_for: Movement | None
    changed: bool


class SignalController:
    """一个路口的相位引擎：按环轮转相位，处理抢占，每一 tick 复核一次安全。"""

    def __init__(self, intersection: Intersection, phases: Sequence[Phase],
                 plan: TimingPlan, clock: Clock, *,
                 clearance_ticks: int = 3, all_red_ticks: int = 2,
                 discharge_per_tick: int = 2, max_preempt_ticks: int = 20) -> None:
        raise NotImplementedError

    @property
    def tick_count(self) -> int:
        raise NotImplementedError

    @property
    def stage(self) -> Stage:
        raise NotImplementedError

    @property
    def current_phase(self) -> Phase:
        raise NotImplementedError

    @property
    def preempted_for(self) -> Movement | None:
        raise NotImplementedError

    @property
    def aspects(self) -> Mapping[Movement, Aspect]:
        """当前各流向的显示，只读快照。"""
        raise NotImplementedError

    @property
    def queue_count(self) -> int:
        """还有多少个流向在排队；排空的流向必须从排队表里消失。"""
        raise NotImplementedError

    def aspect_of(self, movement: Movement) -> Aspect:
        raise NotImplementedError

    def waiting(self, movement: Movement) -> int:
        raise NotImplementedError

    def conflicting_permissive(self) -> tuple[tuple[Movement, Movement], ...]:
        """当前同时放行却互相冲突的流向对；安全时返回空元组。"""
        raise NotImplementedError

    def report_arrival(self, movement: Movement, count: int = 1) -> None:
        raise NotImplementedError

    def request_preemption(self, movement: Movement) -> None:
        """紧急车辆抢占；最短绿走完后照常经过清空 + 全红才切过去。"""
        raise NotImplementedError

    def release_preemption(self) -> None:
        raise NotImplementedError

    def step(self) -> TickReport:
        """推进一个 tick。"""
        raise NotImplementedError

    def run(self, ticks: int) -> tuple[TickReport, ...]:
        raise NotImplementedError


NORTH = Movement("north")
SOUTH = Movement("south")
EAST = Movement("east")
WEST = Movement("west")


def four_way_intersection() -> tuple[Intersection, tuple[Phase, ...]]:
    """标准十字路口：四个进口道，南北一相位、东西一相位。"""
    raise NotImplementedError
