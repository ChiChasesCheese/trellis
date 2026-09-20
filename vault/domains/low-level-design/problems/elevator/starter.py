"""电梯系统（Elevator System）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的地方一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/elevator -q
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, IntEnum

Clock = Callable[[], datetime]


class Direction(IntEnum):
    UP = 1
    DOWN = -1

    @property
    def opposite(self) -> Direction:
        raise NotImplementedError


class CarState(Enum):
    IDLE = "idle"
    MOVING_UP = "moving_up"
    MOVING_DOWN = "moving_down"
    DOORS_OPEN = "doors_open"


class EventKind(Enum):
    MOVED = "moved"
    DOORS_OPENED = "doors_opened"
    DOORS_CLOSED = "doors_closed"


class ElevatorError(Exception):
    """本设计全部失败路径的公共基类。"""


class UnknownCarError(ElevatorError):
    """给出的轿厢 id 在这组电梯里不存在。"""


class FloorNotServedError(ElevatorError):
    """这部梯不停这一层（直达梯／分区梯）。"""


class DoorsNotOpenError(ElevatorError):
    """门没开的时候不能"挡门"。"""


@dataclass(frozen=True, slots=True)
class HallCall:
    floor: int
    direction: Direction


@dataclass(frozen=True, slots=True)
class CarEvent:
    car_id: str
    kind: EventKind
    floor: int
    at: datetime
    served: Direction | None = None


CarObserver = Callable[[CarEvent], None]


@dataclass(frozen=True, slots=True)
class CarSnapshot:
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
        raise NotImplementedError

    def serves(self, floor: int) -> bool:
        raise NotImplementedError

    def stops_for(self, direction: Direction) -> frozenset[int]:
        """朝 `direction` 扫描时会停的楼层：该方向的外呼，加上全部内选。"""
        raise NotImplementedError

    def distance_to(self, floor: int) -> int:
        raise NotImplementedError

    def is_heading_toward(self, call: HallCall) -> bool:
        raise NotImplementedError


ServicePolicy = Callable[[CarSnapshot], int | None]


def nearest_request(car: CarSnapshot) -> int | None:
    """最近请求优先：永远去当前最近的一站，不看方向。"""
    raise NotImplementedError


def scan(car: CarSnapshot) -> int | None:
    """电梯算法（SCAN / LOOK）：朝一个方向一路服务到底，没有顺路的了才掉头。"""
    raise NotImplementedError


DispatchPolicy = Callable[[HallCall, Sequence[CarSnapshot]], str | None]


def nearest_car(call: HallCall, cars: Sequence[CarSnapshot]) -> str | None:
    """最近的梯优先：只看楼层差。"""
    raise NotImplementedError


def directional_dispatch(call: HallCall, cars: Sequence[CarSnapshot]) -> str | None:
    """顺路优先：正朝这一层开且方向一致的排第一，空闲的排第二，要掉头的排最后。"""
    raise NotImplementedError


class ElevatorCar:
    """一部轿厢：自己的状态机、自己的停靠集合，按注入的策略决定下一站。"""

    def __init__(self, car_id: str, policy: ServicePolicy, clock: Clock, *,
                 floor: int = 1, door_ticks: int = 1,
                 served_floors: Iterable[int] | None = None) -> None:
        self._car_id = car_id
        self._policy = policy
        self._clock = clock
        self._floor = floor
        self._door_dwell = door_ticks
        self._served_floors = None if served_floors is None else frozenset(served_floors)

    @property
    def car_id(self) -> str:
        return self._car_id

    @property
    def current_floor(self) -> int:
        raise NotImplementedError

    @property
    def state(self) -> CarState:
        raise NotImplementedError

    @property
    def in_service(self) -> bool:
        raise NotImplementedError

    def snapshot(self) -> CarSnapshot:
        raise NotImplementedError

    def subscribe(self, observer: CarObserver) -> None:
        raise NotImplementedError

    def serves(self, floor: int) -> bool:
        raise NotImplementedError

    def request_floor(self, floor: int) -> None:
        """内选：车里的人按下目标楼层。"""
        raise NotImplementedError

    def accept_hall_call(self, call: HallCall) -> None:
        """接下一个外呼：只在扫描方向和它一致时才会为它停。"""
        raise NotImplementedError

    def drop_hall_call(self, call: HallCall) -> None:
        """撤掉一个还没服务的外呼；内选不受影响。"""
        raise NotImplementedError

    def take_out_of_service(self) -> None:
        raise NotImplementedError

    def return_to_service(self) -> None:
        raise NotImplementedError

    def hold_doors(self, extra_ticks: int = 1) -> None:
        """挡门：把关门倒计时往后推。"""
        raise NotImplementedError

    def step(self) -> CarEvent | None:
        """推进一个 tick：开着门就数门的计时，否则按策略走一格或者开门。"""
        raise NotImplementedError


class ElevatorBank:
    """一组电梯加一个派梯器：外呼进来，恰好一部梯去接。"""

    def __init__(self, cars: Iterable[ElevatorCar], dispatch: DispatchPolicy, clock: Clock) -> None:
        self._cars: dict[str, ElevatorCar] = {car.car_id: car for car in cars}
        self._dispatch = dispatch
        self._clock = clock

    def snapshots(self) -> tuple[CarSnapshot, ...]:
        raise NotImplementedError

    def pending_calls(self) -> frozenset[HallCall]:
        raise NotImplementedError

    def assignment_of(self, call: HallCall) -> str | None:
        raise NotImplementedError

    def subscribe(self, observer: CarObserver) -> None:
        raise NotImplementedError

    def hall_call(self, floor: int, direction: Direction) -> str | None:
        """外呼：某一层有人要往某个方向走。返回接单的轿厢 id。"""
        raise NotImplementedError

    def press_floor(self, car_id: str, floor: int) -> None:
        """内选：车里的人按目标楼层。"""
        raise NotImplementedError

    def take_out_of_service(self, car_id: str) -> tuple[HallCall, ...]:
        """停用一部梯：手上还没完成的外呼立刻收回重派。"""
        raise NotImplementedError

    def return_to_service(self, car_id: str) -> None:
        raise NotImplementedError

    def step(self) -> tuple[CarEvent, ...]:
        """推进一个 tick。"""
        raise NotImplementedError

    def run_until_idle(self, max_ticks: int = 500) -> int:
        """一直推进到所有梯都没活干；返回用掉的 tick 数。"""
        raise NotImplementedError
