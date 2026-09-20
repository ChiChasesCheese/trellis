"""电梯系统（Elevator System）——一部梯的状态机、可换的调度策略、一组梯的派梯。

核心思路：时间用 tick 推进，`step()` 走一格，全程没有 `time.sleep`，所以整套逻辑可以被
确定性地测试；真实时间只通过注入的 `clock` 进入事件的时间戳。一部梯把"此刻在做什么"
（`CarState`：IDLE / MOVING_UP / MOVING_DOWN / DOORS_OPEN）和"这一趟扫描朝哪走"（`_sweep`）
分开存——后者必须跨越开关门存活，否则 SCAN 每停一次就忘记方向。停靠请求按来源分三个集合：
外呼向上、外呼向下、内选；内选两个方向都停，外呼只在方向一致时停。选下一站（`scan` /
`nearest_request`）和派梯（`nearest_car` / `directional_dispatch`）都是普通函数，轿厢和梯群
都不知道它们的内容。
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum

Clock = Callable[[], datetime]


class Direction(IntEnum):
    """外呼要走的方向，同时也是楼层增量：`floor + direction` 就是相邻的下一层。

    没有 `IDLE` 成员——"没有方向"是 `None`，不是第三种方向。
    """

    UP = 1
    DOWN = -1

    @property
    def opposite(self) -> Direction:
        return Direction.DOWN if self is Direction.UP else Direction.UP


class CarState(Enum):
    """一部梯此刻在做什么——只描述机械动作，不描述"是否可用"。

    "停用/检修"不做成这里的成员：它和四个动作状态正交，做成状态就要再多出
    IDLE_OUT_OF_SERVICE、DOORS_OPEN_OUT_OF_SERVICE……这是状态爆炸的标准起点。
    """

    IDLE = "idle"
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    DOORS_OPEN = "doors_open"


class EventKind(Enum):
    MOVED = "moved"
    DOORS_OPENED = "doors_opened"
    DOORS_CLOSED = "doors_closed"


class ElevatorError(Exception):
    """本设计全部失败路径的公共基类，调用方可以一次性捕获。"""


class UnknownCarError(ElevatorError):
    """给出的轿厢 id 在这组电梯里不存在。"""


class FloorNotServedError(ElevatorError):
    """这部梯不停这一层（直达梯／分区梯）。"""


class DoorsNotOpenError(ElevatorError):
    """门没开的时候不能"挡门"。"""


@dataclass(frozen=True, slots=True)
class HallCall:
    """一次外呼：站在 `floor` 的人想往 `direction` 走。

    不可变、可哈希，因为它要当字典的键——"一个按钮只叫来一部梯"正是靠
    `HallCall -> car_id` 这张表保证的。
    """

    floor: int
    direction: Direction


@dataclass(frozen=True, slots=True)
class CarEvent:
    """轿厢身上发生的一件事，自带全部上下文：订阅者（显示牌、派梯器）只看这份不可变
    记录就能更新自己，不必回头去读轿厢的内部集合——那样既绕过不变式，并发下也无保护。
    """

    car_id: str
    kind: EventKind
    floor: int
    at: datetime
    served: Direction | None = None  # 仅 DOORS_OPENED：这一停服务的是哪个方向的扫描


CarObserver = Callable[[CarEvent], None]


@dataclass(frozen=True, slots=True)
class CarSnapshot:
    """轿厢在某一刻的只读快照：策略函数看到的全部信息。三个停靠集合都是 `frozenset`，
    策略拿到手也改不了轿厢的真实状态；轿厢从不把自己的 `set` 交出去。
    """

    car_id: str
    floor: int
    state: CarState
    sweep: Direction | None
    up_calls: frozenset[int]
    down_calls: frozenset[int]
    car_calls: frozenset[int]
    in_service: bool
    served_floors: frozenset[int] | None

    @property
    def is_busy(self) -> bool:
        return bool(self.up_calls or self.down_calls or self.car_calls)

    def serves(self, floor: int) -> bool:
        """这部梯停不停这一层；`served_floors` 为 `None` 表示层层都停。"""
        return self.served_floors is None or floor in self.served_floors

    def stops_for(self, direction: Direction) -> frozenset[int]:
        """朝 `direction` 扫描时会停的楼层：该方向的外呼，加上全部内选。

        内选出现在两个方向里——车里的人按了 7 层，上行下行到 7 层都必须停；只有外呼挑方向。
        """
        hall = self.up_calls if direction is Direction.UP else self.down_calls
        return hall | self.car_calls

    def distance_to(self, floor: int) -> int:
        return abs(floor - self.floor)

    def is_heading_toward(self, call: HallCall) -> bool:
        """这部梯正在做的扫描方向和外呼一致，而且外呼那一层还在它前方（顺路）。"""
        if self.sweep is not call.direction:
            return False
        return (call.floor - self.floor) * int(self.sweep) >= 0


# --------------------------------------------------------------------------
# 停靠策略：给一份快照，回答"下一站去哪"。两种规则在调用之间都不需要记住任何东西（该记
# 的方向已在快照的 `sweep` 里），所以是普通函数，不是抽象基类加两个实现类。

ServicePolicy = Callable[[CarSnapshot], int | None]


def _nearest(car: CarSnapshot) -> int | None:
    stops = car.up_calls | car.down_calls | car.car_calls
    if not stops:
        return None
    return min(stops, key=lambda floor: (abs(floor - car.floor), floor))


def nearest_request(car: CarSnapshot) -> int | None:
    """最近请求优先：永远去当前最近的一站，不看方向。

    实现最短，但没有任何公平性保证：只要近处一直有人按，远处那一层可以永远等下去。
    """
    return _nearest(car)


def scan(car: CarSnapshot) -> int | None:
    """电梯算法（SCAN / LOOK）：朝一个方向一路服务到底，没有顺路的了才掉头。

    公平性来自"一趟扫描最多走一个来回"：任何一个请求最迟在电梯扫到它所在的那一段时
    被服务，等待时间有上界，不会被后来的近处请求无限插队。
    """
    if car.sweep is None:
        return _nearest(car)
    ahead = [f for f in car.stops_for(car.sweep) if (f - car.floor) * int(car.sweep) >= 0]
    if ahead:
        return min(ahead) if car.sweep is Direction.UP else max(ahead)
    back = car.stops_for(car.sweep.opposite)
    if back:
        # 掉头：先开到反向扫描的起点（本方向上最远的那一站），再一路扫回来。
        return max(back) if car.sweep is Direction.UP else min(back)
    # 只剩同向、却落在身后的外呼：开回去重新起一趟扫描。
    rest = car.up_calls if car.sweep is Direction.UP else car.down_calls
    if not rest:
        return None
    return min(rest) if car.sweep is Direction.UP else max(rest)


# --------------------------------------------------------------------------
# 派梯策略：给一个外呼和全部轿厢的快照，回答"派哪一部"。它优化这位乘客的等待时间；
# "同一个外呼绝不派给两部梯"则由 `ElevatorBank` 的分派表保证，不靠策略自觉。

DispatchPolicy = Callable[[HallCall, Sequence[CarSnapshot]], str | None]


def _eligible(call: HallCall, cars: Sequence[CarSnapshot]) -> list[CarSnapshot]:
    return [c for c in cars if c.in_service and c.serves(call.floor)]


def nearest_car(call: HallCall, cars: Sequence[CarSnapshot]) -> str | None:
    """最近的梯优先：只看楼层差。简单，但会把外呼派给一部正在反方向跑的梯。"""
    candidates = _eligible(call, cars)
    if not candidates:
        return None
    return min(candidates, key=lambda c: (c.distance_to(call.floor), c.car_id)).car_id


def directional_dispatch(call: HallCall, cars: Sequence[CarSnapshot]) -> str | None:
    """顺路优先：正朝这一层开且方向一致的排第一，空闲的排第二，要掉头的排最后。"""
    candidates = _eligible(call, cars)
    if not candidates:
        return None

    def cost(c: CarSnapshot) -> tuple[int, int, str]:
        if c.is_heading_toward(call):
            rank = 0
        elif not c.is_busy:
            rank = 1
        else:
            rank = 2
        return (rank, c.distance_to(call.floor), c.car_id)

    return min(candidates, key=cost).car_id


class ElevatorCar:
    """一部轿厢：自己的状态机、自己的停靠集合，按注入的策略决定下一站。

    不变式：
    1. `state is MOVING_UP` 蕴含 `sweep is Direction.UP`（MOVING_DOWN 同理）；`sweep` 跨越
       开关门保持不变——这正是 SCAN 停一次后还知道往哪走的原因；停靠集合全空才清成 `None`。
    2. 每次开门都把这一层从"被服务的那个集合"里移除；三个集合只随未完成的请求增长，
       服务完就缩小，不会无限膨胀。
    3. 停用（`in_service`）与状态机正交：只意味着不再接外呼，车里的人照样送到，
       所以 `step()` 根本不看这个标志。
    """

    def __init__(self, car_id: str, policy: ServicePolicy, clock: Clock, *,
                 floor: int = 1, door_ticks: int = 1,
                 served_floors: Iterable[int] | None = None) -> None:
        self._car_id = car_id
        self._policy = policy
        self._clock = clock
        self._floor = floor
        self._state = CarState.IDLE
        self._sweep: Direction | None = None
        self._up_calls: set[int] = set()
        self._down_calls: set[int] = set()
        self._car_calls: set[int] = set()
        self._door_dwell = door_ticks
        self._door_ticks = 0
        self._in_service = True
        self._served_floors = None if served_floors is None else frozenset(served_floors)
        self._observers: list[CarObserver] = []

    @property
    def car_id(self) -> str:
        return self._car_id

    @property
    def current_floor(self) -> int:
        return self._floor

    @property
    def state(self) -> CarState:
        return self._state

    @property
    def in_service(self) -> bool:
        return self._in_service

    def serves(self, floor: int) -> bool:
        return self._served_floors is None or floor in self._served_floors

    def snapshot(self) -> CarSnapshot:
        """一份不可变快照；这是外界能看到轿厢内部的唯一形式。"""
        return CarSnapshot(car_id=self._car_id, floor=self._floor, state=self._state,
                           sweep=self._sweep, up_calls=frozenset(self._up_calls),
                           down_calls=frozenset(self._down_calls),
                           car_calls=frozenset(self._car_calls), in_service=self._in_service,
                           served_floors=self._served_floors)

    def subscribe(self, observer: CarObserver) -> None:
        """订阅这部梯的事件；派梯器和显示牌都是这样接进来的。"""
        self._observers.append(observer)

    def request_floor(self, floor: int) -> None:
        """内选：车里的人按下目标楼层。没有方向，两个方向的扫描都会在这一层停。"""
        if not self.serves(floor):
            raise FloorNotServedError(f"car {self._car_id!r} does not serve floor {floor}")
        if floor == self._floor and self._state is CarState.DOORS_OPEN:
            return
        self._car_calls.add(floor)

    def accept_hall_call(self, call: HallCall) -> None:
        """接下一个外呼：只在扫描方向和它一致时才会为它停。由梯群调用。"""
        if not self.serves(call.floor):
            raise FloorNotServedError(f"car {self._car_id!r} does not serve floor {call.floor}")
        target = self._up_calls if call.direction is Direction.UP else self._down_calls
        target.add(call.floor)

    def drop_hall_call(self, call: HallCall) -> None:
        """撤掉一个还没服务的外呼（这部梯被停用时由梯群收回重派）。内选不受影响——这
        正是外呼和内选分开存的实际收益：撤掉"7 层有人要上行"，不会连"车里有人要去 7 层"一起撤。
        """
        target = self._up_calls if call.direction is Direction.UP else self._down_calls
        target.discard(call.floor)

    def take_out_of_service(self) -> None:
        """停用：不再接新的外呼；已经在车里的人照常送到。"""
        self._in_service = False

    def return_to_service(self) -> None:
        self._in_service = True

    def hold_doors(self, extra_ticks: int = 1) -> None:
        """挡门：把关门倒计时往后推。复用已有的门计时，不需要新增任何状态。"""
        if self._state is not CarState.DOORS_OPEN:
            raise DoorsNotOpenError(f"car {self._car_id!r} doors are not open")
        self._door_ticks += extra_ticks

    def step(self) -> CarEvent | None:
        """推进一个 tick：开着门就数门的计时，否则按策略走一格或者开门。

        一个 tick 只做一件事，因此每一步都能在测试里被单独断言，也不需要任何真实等待。
        """
        if self._state is CarState.DOORS_OPEN:
            self._door_ticks -= 1
            if self._door_ticks > 0:
                return None
            self._state = CarState.IDLE
            return self._emit(EventKind.DOORS_CLOSED)
        target = self._policy(self.snapshot())
        if target is None:
            self._state = CarState.IDLE
            self._sweep = None
            return None
        if target == self._floor:
            return self._serve()
        step_dir = Direction.UP if target > self._floor else Direction.DOWN
        self._sweep = step_dir
        self._floor += int(step_dir)
        self._state = (CarState.MOVING_UP if step_dir is Direction.UP else CarState.MOVING_DOWN)
        return self._emit(EventKind.MOVED)

    def _serve(self) -> CarEvent:
        """到站开门：判断这一停服务的是哪个方向的扫描，并把对应请求移除。"""
        floor = self._floor
        served: Direction | None = None
        sweep_hall = (self._up_calls if self._sweep is Direction.UP else self._down_calls)
        if self._sweep is not None and (floor in sweep_hall or floor in self._car_calls):
            served = self._sweep
        elif floor in self._up_calls:
            served = Direction.UP
        elif floor in self._down_calls:
            served = Direction.DOWN
        if served is not None:
            self._sweep = served  # 掉头点：服务哪个方向，扫描方向就跟着翻过来
            hall = self._up_calls if served is Direction.UP else self._down_calls
            hall.discard(floor)
        self._car_calls.discard(floor)
        self._state = CarState.DOORS_OPEN
        self._door_ticks = self._door_dwell
        return self._emit(EventKind.DOORS_OPENED, served=served)

    def _emit(self, kind: EventKind, served: Direction | None = None) -> CarEvent:
        event = CarEvent(car_id=self._car_id, kind=kind, floor=self._floor,
                         at=self._clock(), served=served)
        for observer in self._observers:
            observer(event)
        return event


class ElevatorBank:
    """一组电梯加一个派梯器：外呼进来，恰好一部梯去接。

    不变式：一个还没被服务的外呼在 `_assigned` 里最多对应一部梯——同一个按钮按两次不会叫来
    两部梯；某部梯真的到了那层、开门、且开门服务的正是这个方向时，这条记录立刻删除。
    `_assigned` 和 `_pending` 都必须缩：不缩的话，同一层同一方向的第二次呼叫会被静默吞掉。
    """

    def __init__(self, cars: Iterable[ElevatorCar], dispatch: DispatchPolicy, clock: Clock) -> None:
        self._cars: dict[str, ElevatorCar] = {car.car_id: car for car in cars}
        self._dispatch = dispatch
        self._clock = clock
        self._lock = threading.Lock()
        self._assigned: dict[HallCall, str] = {}
        self._pending: set[HallCall] = set()
        self._observers: list[CarObserver] = []
        for car in self._cars.values():
            car.subscribe(self._on_car_event)

    def snapshots(self) -> tuple[CarSnapshot, ...]:
        """全部轿厢的只读快照；梯群从不把 `ElevatorCar` 的集合或字典交出去。"""
        return tuple(car.snapshot() for car in self._cars.values())

    def pending_calls(self) -> frozenset[HallCall]:
        """当前没有任何梯能接、正在等重试的外呼。"""
        with self._lock:
            return frozenset(self._pending)

    def assignment_of(self, call: HallCall) -> str | None:
        """这个外呼当前派给了哪部梯；没派出去就是 `None`。"""
        with self._lock:
            return self._assigned.get(call)

    def subscribe(self, observer: CarObserver) -> None:
        self._observers.append(observer)

    def hall_call(self, floor: int, direction: Direction) -> str | None:
        """外呼：某一层有人要往某个方向走。返回接单的轿厢 id，暂时没人能接则返回 `None`。"""
        call = HallCall(floor, direction)
        with self._lock:
            if call in self._assigned:
                return self._assigned[call]  # 幂等：按两次按钮不会叫来第二部梯
            self._pending.discard(call)
            return self._assign(call)

    def press_floor(self, car_id: str, floor: int) -> None:
        """内选：车里的人按目标楼层。梯群校验 id，不把轿厢对象交出去。"""
        self._require(car_id).request_floor(floor)

    def take_out_of_service(self, car_id: str) -> tuple[HallCall, ...]:
        """停用一部梯：手上还没完成的外呼立刻收回重派，内选（车里的人）照常送到。"""
        with self._lock:
            car = self._require(car_id)
            car.take_out_of_service()
            stranded = tuple(c for c, owner in self._assigned.items() if owner == car_id)
            for call in stranded:
                del self._assigned[call]
                car.drop_hall_call(call)
            for call in stranded:
                self._assign(call)
        return stranded

    def return_to_service(self, car_id: str) -> None:
        self._require(car_id).return_to_service()

    def step(self) -> tuple[CarEvent, ...]:
        """推进一个 tick：先重试挂起的外呼，再让每一部梯各走一格。"""
        with self._lock:
            for call in tuple(self._pending):
                self._pending.discard(call)
                self._assign(call)
        # 轿厢的 step() 会同步回调 `_on_car_event`，因此这里必须已经出了锁。
        return tuple(e for car in self._cars.values() if (e := car.step()) is not None)

    def run_until_idle(self, max_ticks: int = 500) -> int:
        """一直推进到所有梯都没活干；返回用掉的 tick 数。超过上限说明设计出了环。"""
        for tick in range(1, max_ticks + 1):
            self.step()
            if not any(s.is_busy for s in self.snapshots()) and not self.pending_calls():
                return tick
        raise ElevatorError(f"still busy after {max_ticks} ticks")

    def _require(self, car_id: str) -> ElevatorCar:
        car = self._cars.get(car_id)
        if car is None:
            raise UnknownCarError(f"unknown car {car_id!r}")
        return car

    def _assign(self, call: HallCall) -> str | None:
        """在锁内把一个外呼派给恰好一部梯；没梯能接就挂起，下一个 tick 再试。"""
        car_id = self._dispatch(call, self.snapshots())
        if car_id is None:
            self._pending.add(call)
            return None
        car = self._require(car_id)
        self._assigned[call] = car_id
        car.accept_hall_call(call)
        return car_id

    def _on_car_event(self, event: CarEvent) -> None:
        """轿厢的每一件事都经过这里：开门就销掉已完成的外呼，再转发给外部订阅者。
        订阅者在锁外通知——一个慢订阅者（哪怕只是写一行日志）不该把所有外呼堵在门口。
        """
        if event.kind is EventKind.DOORS_OPENED and event.served is not None:
            call = HallCall(event.floor, event.served)
            with self._lock:
                self._assigned.pop(call, None)
                self._pending.discard(call)
        for observer in self._observers:
            observer(event)


if __name__ == "__main__":
    from datetime import UTC, timedelta

    now = datetime(2026, 1, 1, 9, 0, tzinfo=UTC)

    def tick_clock() -> datetime:
        return now

    cars = [ElevatorCar("A", policy=scan, clock=tick_clock, floor=1),
            ElevatorCar("B", policy=scan, clock=tick_clock, floor=8)]
    bank = ElevatorBank(cars, dispatch=directional_dispatch, clock=tick_clock)
    bank.subscribe(lambda e: print(f"  {e.car_id} {e.kind.value} @ {e.floor}"))
    print("hall call 7↓ ->", bank.hall_call(7, Direction.DOWN))
    print("hall call 2↑ ->", bank.hall_call(2, Direction.UP))
    for _ in range(6):
        now = now + timedelta(seconds=3)
        bank.step()
    print("pending:", bank.pending_calls())
