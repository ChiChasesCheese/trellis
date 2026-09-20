"""交通信号灯（Traffic Signal）——按 tick 推进的相位引擎、可换配时方案、紧急车辆抢占。

核心思路：路口的安全定义不是"南北和东西不能同时绿"，而是一张**冲突图**——哪两个流向
（movement）不能同时放行。相位（phase）只是"一组互不冲突、同时放行的流向"，引擎因此完全
不认识东南西北，第 4 关加行人相位或左转箭头只是多造一个 `Movement` 和一个 `Phase`。
时间靠 `step()` 一格一格走，全程没有 `time.sleep`，真实时间只通过注入的 `clock` 进入时间戳，
所以几千个 tick 的随机压力测试可以确定性复现。相位切换必须经过黄灯 + 全红清空，**全红间隔
正是不变式在切换瞬间仍然成立的原因**；每一 tick 结束都按冲突图复核一次，违反就抛异常。
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Protocol

Clock = Callable[[], datetime]


class SignalError(Exception):
    """本设计全部失败路径的公共基类。"""


class UnknownMovementError(SignalError):
    """这个流向不属于本路口。"""


class ConflictingPhaseError(SignalError):
    """相位里放进了两个互相冲突的流向——这是配置错误，必须在启动时就炸掉。"""


class SafetyViolationError(SignalError):
    """运行中两个冲突流向同时放行了。任何一次都算严重故障，不允许被吞掉。"""


class Aspect(Enum):
    """一个灯组此刻显示什么。机动车和行人用的是**同一套三段语义**，只是名字不同。"""

    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    DONT_WALK = "dont_walk"
    WALK = "walk"
    FLASHING_DONT_WALK = "flashing_dont_walk"

    @property
    def permissive(self) -> bool:
        """此刻是否允许进入路口。黄灯和闪烁的"禁止通行"都**不是**放行——它们是清空。"""
        return self is Aspect.GREEN or self is Aspect.WALK


class MovementKind(Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"


class Stage(Enum):
    """一个相位内部的三段。清空段与全红段合起来构成"相位间隔"（intergreen）。"""

    GREEN = "green"
    CLEARANCE = "clearance"
    ALL_RED = "all_red"


@dataclass(frozen=True, slots=True)
class Movement:
    """一个**流向**：从某个进口道往某个方向走的一股交通流，或者一条人行横道。

    不可变、可哈希，因为它要当字典键和集合成员。`go` / `clear` / `stop` 这三个属性是整个
    设计的枢纽：相位引擎只会问流向这三个问题，于是行人的 走-闪-禁 和机动车的 绿-黄-红
    在引擎眼里是同一件事，加行人相位不需要动引擎一行。
    """

    name: str
    kind: MovementKind = MovementKind.VEHICLE

    @property
    def go(self) -> Aspect:
        return Aspect.WALK if self.kind is MovementKind.PEDESTRIAN else Aspect.GREEN

    @property
    def clear(self) -> Aspect:
        return (Aspect.FLASHING_DONT_WALK if self.kind is MovementKind.PEDESTRIAN
                else Aspect.YELLOW)

    @property
    def stop(self) -> Aspect:
        return Aspect.DONT_WALK if self.kind is MovementKind.PEDESTRIAN else Aspect.RED


@dataclass(frozen=True, slots=True)
class Phase:
    """一组同时放行的流向，加上它的最短绿与最长绿。

    最短绿不是调优参数而是安全参数：绿灯刚亮一格就跳黄，已经起步的司机没有停车距离。
    最长绿是防饿死的上限——感应式方案再怎么"有车就延长"也不能越过它。
    """

    name: str
    movements: frozenset[Movement]
    min_green: int = 4
    max_green: int = 12

    def serves(self, movement: Movement) -> bool:
        return movement in self.movements


class Intersection:
    """路口的几何：有哪些流向、哪两个流向互相冲突。它**拥有"安全"的定义**。

    不变式：冲突关系是对称的，且没有流向和自己冲突；任何相位在被引擎接受之前，都必须通过
    `validate_phase`——配置期就能发现的错误绝不留到运行期。
    """

    def __init__(self, name: str, movements: Iterable[Movement],
                 conflicts: Iterable[tuple[Movement, Movement]]) -> None:
        self._name = name
        self._movements = tuple(movements)
        self._conflicts: dict[Movement, set[Movement]] = {m: set() for m in self._movements}
        for left, right in conflicts:
            self._require(left)
            self._require(right)
            if left == right:
                raise ConflictingPhaseError(f"movement {left.name!r} cannot conflict with itself")
            self._conflicts[left].add(right)
            self._conflicts[right].add(left)  # 冲突天然对称，只让配置写一遍

    @property
    def name(self) -> str:
        return self._name

    @property
    def movements(self) -> tuple[Movement, ...]:
        """全部流向的只读元组；内部的集合从不交出去。"""
        return self._movements

    def conflicting_with(self, movement: Movement) -> frozenset[Movement]:
        return frozenset(self._conflicts[self._require(movement)])

    def conflicts(self, left: Movement, right: Movement) -> bool:
        return right in self._conflicts[self._require(left)]

    def validate_phase(self, phase: Phase) -> None:
        """相位内部不能有互相冲突的流向。启动时查一次，比运行时抛一百次有用。"""
        for left, right in itertools.combinations(sorted(phase.movements, key=lambda m: m.name), 2):
            if self.conflicts(left, right):
                raise ConflictingPhaseError(
                    f"phase {phase.name!r} puts conflicting {left.name!r} and {right.name!r} together")

    def _require(self, movement: Movement) -> Movement:
        if movement not in self._conflicts:
            raise UnknownMovementError(f"{movement.name!r} is not a movement of {self._name!r}")
        return movement


@dataclass(frozen=True, slots=True)
class PhaseContext:
    """交给配时方案的**只读快照**：它要做决定所需要的全部信息，一个字段不多。

    方案拿到的是数字，不是控制器的字典——它既改不了控制器的状态，也不需要控制器的锁。
    """

    phase: Phase
    elapsed: int              # 本相位绿灯已经持续了几个 tick
    tick: int
    waiting: int              # 本相位各流向上还排着多少辆（人）
    gap_since_arrival: int    # 距本相位上一次有车到达过了几个 tick


class TimingPlan(Protocol):
    """配时方案：绿灯还要不要再保持一个 tick。

    这里用协议（Protocol）而不是普通函数，是因为**真的有两个实现**，而且它们都带配置状态
    （定周期的每相位时长表、感应式的断流间隔）。只有一个实现时不该先写接口。
    """

    def hold(self, ctx: PhaseContext) -> bool:
        ...


class FixedTimePlan:
    """定周期（fixed-time）：每个相位绿多久写死在方案里，和路上有没有车无关。

    优点是可预测、可以和相邻路口做绿波协调；缺点是深夜空无一人时仍然让主路等满一个周期。
    """

    def __init__(self, green: Mapping[str, int] | None = None, default: int = 10) -> None:
        self._green = dict(green or {})
        self._default = default

    def hold(self, ctx: PhaseContext) -> bool:
        target = max(ctx.phase.min_green, self._green.get(ctx.phase.name, self._default))
        return ctx.elapsed < target


class ActuatedPlan:
    """感应式（vehicle-actuated）：最短绿之后，只要车还在陆续到达就延长，直到最长绿。

    `gap` 是**断流间隔**（gap-out）：连续 `gap` 个 tick 没有新车到达，就认为这股车流断了，
    立刻切相位。最长绿是硬上限——没有它，一条车流不断的主路可以让支路永远等下去。
    """

    def __init__(self, gap: int = 3) -> None:
        self._gap = gap

    def hold(self, ctx: PhaseContext) -> bool:
        if ctx.elapsed < ctx.phase.min_green:
            return True
        if ctx.elapsed >= ctx.phase.max_green:
            return False
        return ctx.waiting > 0 or ctx.gap_since_arrival <= self._gap


@dataclass(frozen=True, slots=True)
class TickReport:
    """一个 tick 之后路口的完整状态，自带全部上下文。

    这里**没有观察者模式**：`step()` 本来就被驱动循环每一 tick 调用一次，把这一刻发生的事
    直接当返回值交出去，比再挂一套订阅回调更直接。`aspects` 是快照，不是控制器的活字典。
    """

    tick: int
    at: datetime
    stage: Stage
    phase_name: str
    aspects: Mapping[Movement, Aspect]
    preempted_for: Movement | None
    changed: bool  # 这一 tick 是否发生了阶段切换（绿→清空、清空→全红、全红→下一个绿）


class SignalController:
    """一个路口的相位引擎：按环（ring）轮转相位，处理抢占，每一 tick 复核一次安全。

    不变式：
    1. **任意时刻，冲突图上相邻的两个流向不会同时 `permissive`。** 每一 tick 末尾按冲突图
       复核，违反就抛 `SafetyViolationError`——不用裸 `assert`，因为 `python -O` 会把它删掉，
       而这是一条会撞死人的不变式。
    2. 相位切换必须走 绿 → 清空（黄／闪） → 全红 → 下一个绿。**全红段是不变式在切换瞬间
       仍然成立的原因**：上一相位的车驶离路口需要时间，没有这段间隔，两个方向的绿之间就是
       一个物理上重叠的窗口。
    3. `_queues` 只记还在排队的流向，排空的流向立刻删键——排队字典必须会缩，否则一个跑了
       一整天的路口会攒下每个流向一条计数为 0 的僵尸记录。
    4. 抢占有上限 `max_preempt_ticks`：没有上限的抢占就是一个饿死 bug。
    """

    def __init__(self, intersection: Intersection, phases: Sequence[Phase],
                 plan: TimingPlan, clock: Clock, *,
                 clearance_ticks: int = 3, all_red_ticks: int = 2,
                 discharge_per_tick: int = 2, max_preempt_ticks: int = 20) -> None:
        if not phases:
            raise SignalError("a controller needs at least one phase")
        for phase in phases:
            intersection.validate_phase(phase)
            for movement in phase.movements:
                intersection.conflicting_with(movement)  # 顺手校验流向属于本路口
        self._intersection = intersection
        self._phases = tuple(phases)
        self._plan = plan
        self._clock = clock
        self._clearance = clearance_ticks
        self._all_red = all_red_ticks
        self._discharge = discharge_per_tick
        self._max_preempt = max_preempt_ticks
        self._index = 0
        self._stage = Stage.GREEN
        self._stage_left = 0
        self._elapsed = 0
        self._tick = 0
        self._preempt: Movement | None = None
        self._preempt_left = 0
        self._queues: dict[Movement, int] = {}
        self._last_arrival: dict[Movement, int] = {}
        self._aspects: dict[Movement, Aspect] = {m: m.stop for m in intersection.movements}
        self._show_go(self._phases[0])
        self._verify()

    # ---- 只读视图 ---------------------------------------------------------------

    @property
    def tick_count(self) -> int:
        return self._tick

    @property
    def stage(self) -> Stage:
        return self._stage

    @property
    def current_phase(self) -> Phase:
        return self._phases[self._index]

    @property
    def preempted_for(self) -> Movement | None:
        return self._preempt

    @property
    def aspects(self) -> Mapping[Movement, Aspect]:
        """当前各流向的显示，只读快照；控制器从不把自己的字典交出去。"""
        return MappingProxyType(dict(self._aspects))

    @property
    def queue_count(self) -> int:
        """还有多少个流向在排队。排空的流向必须从排队表里消失，这个数字就是证据。"""
        return len(self._queues)

    def aspect_of(self, movement: Movement) -> Aspect:
        return self._aspects[self._intersection_movement(movement)]

    def waiting(self, movement: Movement) -> int:
        return self._queues.get(self._intersection_movement(movement), 0)

    def conflicting_permissive(self) -> tuple[tuple[Movement, Movement], ...]:
        """当前同时放行却互相冲突的流向对。安全时返回空元组——这就是那条不变式。"""
        live = sorted((m for m, a in self._aspects.items() if a.permissive), key=lambda m: m.name)
        return tuple((a, b) for a, b in itertools.combinations(live, 2)
                     if self._intersection.conflicts(a, b))

    # ---- 外部输入 ---------------------------------------------------------------

    def report_arrival(self, movement: Movement, count: int = 1) -> None:
        """检测器报告有车（或按钮报告有行人）到达某个流向。"""
        movement = self._intersection_movement(movement)
        if count <= 0:
            return
        self._queues[movement] = self._queues.get(movement, 0) + count
        self._last_arrival[movement] = self._tick

    def request_preemption(self, movement: Movement) -> None:
        """紧急车辆抢占：某个流向要求放行。

        它**不会**让当前绿灯立刻跳黄：最短绿必须走完（已经起步的车没有停车距离），然后照常
        经过清空 + 全红才切过去。抢占改变的是"下一个相位是谁"，不是"能不能跳过间隔"。
        """
        movement = self._intersection_movement(movement)
        if not any(p.serves(movement) for p in self._phases):
            raise UnknownMovementError(f"no phase serves {movement.name!r}")
        self._preempt = movement
        self._preempt_left = self._max_preempt

    def release_preemption(self) -> None:
        """紧急车辆通过了。控制器从当前相位继续它的环，不跳回被打断的那个相位。"""
        self._preempt = None
        self._preempt_left = 0

    # ---- 推进 -------------------------------------------------------------------

    def step(self) -> TickReport:
        """推进一个 tick。一个 tick 只做一件事，所以每一步都能被单独断言，也不需要等待。"""
        self._tick += 1
        changed = False
        if self._stage is Stage.GREEN:
            self._elapsed += 1
            self._drain()
            if not self._should_hold():
                self._begin_clearance()
                changed = True
        else:
            self._stage_left -= 1
            if self._stage_left <= 0:
                if self._stage is Stage.CLEARANCE:
                    self._enter_all_red()
                else:
                    self._begin_green(self._next_index())
                changed = True
        if self._preempt is not None:
            self._preempt_left -= 1
            if self._preempt_left <= 0:
                self.release_preemption()
        self._verify()
        return TickReport(tick=self._tick, at=self._clock(), stage=self._stage,
                          phase_name=self.current_phase.name, aspects=self.aspects,
                          preempted_for=self._preempt, changed=changed)

    def run(self, ticks: int) -> tuple[TickReport, ...]:
        """连推若干 tick，返回每一 tick 的报告。演示和测试都用它。"""
        return tuple(self.step() for _ in range(ticks))

    # ---- 内部 -------------------------------------------------------------------

    def _intersection_movement(self, movement: Movement) -> Movement:
        if movement not in self._aspects:
            raise UnknownMovementError(f"{movement.name!r} is not a movement of this intersection")
        return movement

    def _should_hold(self) -> bool:
        phase = self.current_phase
        if self._preempt is not None:
            if phase.serves(self._preempt):
                return True  # 正在为紧急车辆放行，保持到释放或到上限
            return self._elapsed < phase.min_green  # 最短绿一走完就让路
        return self._plan.hold(self._context(phase))

    def _context(self, phase: Phase) -> PhaseContext:
        waiting = sum(self._queues.get(m, 0) for m in phase.movements)
        last = [self._last_arrival[m] for m in phase.movements if m in self._last_arrival]
        gap = self._tick - max(last) if last else self._tick
        return PhaseContext(phase=phase, elapsed=self._elapsed, tick=self._tick,
                            waiting=waiting, gap_since_arrival=gap)

    def _next_index(self) -> int:
        """下一个相位：正常按环轮转；有抢占请求时，直接转到第一个服务它的相位。"""
        if self._preempt is not None:
            for offset in range(len(self._phases)):
                index = (self._index + offset) % len(self._phases)
                if self._phases[index].serves(self._preempt):
                    return index
        return (self._index + 1) % len(self._phases)

    def _drain(self) -> None:
        """绿灯期间每 tick 放走若干辆；队列清空的流向立刻从排队表里删掉。"""
        for movement in self.current_phase.movements:
            waiting = self._queues.get(movement)
            if waiting is None:
                continue
            left = waiting - self._discharge
            if left > 0:
                self._queues[movement] = left
            else:
                del self._queues[movement]

    def _begin_clearance(self) -> None:
        for movement in self.current_phase.movements:
            self._aspects[movement] = movement.clear
        self._stage = Stage.CLEARANCE
        self._stage_left = self._clearance

    def _enter_all_red(self) -> None:
        """全红：所有流向一起停。这一段是相位间隔的后半截，不变式全靠它。"""
        for movement in self._aspects:
            self._aspects[movement] = movement.stop
        self._stage = Stage.ALL_RED
        self._stage_left = self._all_red

    def _begin_green(self, index: int) -> None:
        self._index = index
        self._elapsed = 0
        self._stage = Stage.GREEN
        self._show_go(self._phases[index])

    def _show_go(self, phase: Phase) -> None:
        for movement in self._aspects:
            self._aspects[movement] = movement.go if phase.serves(movement) else movement.stop

    def _verify(self) -> None:
        clashes = self.conflicting_permissive()
        if clashes:
            names = ", ".join(f"{a.name}|{b.name}" for a, b in clashes)
            raise SafetyViolationError(f"conflicting movements are permissive at tick {self._tick}: {names}")


NORTH = Movement("north")
SOUTH = Movement("south")
EAST = Movement("east")
WEST = Movement("west")


def four_way_intersection() -> tuple[Intersection, tuple[Phase, ...]]:
    """标准十字路口：四个进口道，南北一相位、东西一相位。

    同向的两个进口道（北与南）互不冲突，所以它们在同一个相位里；跨向的每一对都冲突。
    冲突写成数据而不是 `if direction in ("north", "south")`，引擎才可能对第 4 关的新流向
    一无所知却依然安全。
    """
    movements = (NORTH, SOUTH, EAST, WEST)
    conflicts = [(ns, ew) for ns in (NORTH, SOUTH) for ew in (EAST, WEST)]
    intersection = Intersection("main-st-x-1st-ave", movements, conflicts)
    phases = (Phase("north-south", frozenset({NORTH, SOUTH})),
              Phase("east-west", frozenset({EAST, WEST})))
    return intersection, phases


if __name__ == "__main__":
    from datetime import timedelta

    now = datetime(2026, 4, 1, 8, 0)

    def clock() -> datetime:
        return now

    junction, ring = four_way_intersection()
    controller = SignalController(junction, ring, ActuatedPlan(gap=2), clock,
                                  clearance_ticks=2, all_red_ticks=1)
    controller.report_arrival(EAST, 6)
    for _ in range(18):
        now = now + timedelta(seconds=2)
        report = controller.step()
        if report.changed:
            shown = {m.name: a.value for m, a in report.aspects.items() if a.permissive}
            print(f"t={report.tick:>3} {report.stage.value:<9} {report.phase_name:<12} go={shown}")
    print("queues left:", controller.queue_count, "conflicts:", controller.conflicting_permissive())
