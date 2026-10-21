"""机器人餐厅练习骨架：公开 API 与 solution.py 完全一致，方法体全部待补全。
把每个 raise NotImplementedError 换成你自己的实现，然后用 IMPL=starter uv run --with pytest python -m pytest <本目录> -q 验收。
内部表示随你换，测试只通过公开方法断言。"""
from __future__ import annotations
import threading
from collections import deque
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from enum import Enum

class RestaurantError(Exception):
    """本模块所有异常的根。"""

class UnknownDishError(RestaurantError, LookupError):
    """菜单上没有这道菜。"""

class UnknownOrderError(RestaurantError, LookupError):
    """没有这个订单号。"""

class OrderRejectedError(RestaurantError, ValueError):
    """订单本身无法被任何机器人完成（耗电超过一台满足阈值的机器人能承担的量）。"""

class OrderNotCancellableError(RestaurantError):
    """订单已被机器人接走（或已结束），不能再取消。"""

class InvalidTransitionError(RestaurantError):
    """机器人状态机收到了表里没有的转移。"""

class PolicyError(RestaurantError):
    """分配策略返回了不在候选里的机器人。"""

@dataclass(frozen=True, slots=True)
class Dish:
    """菜品：名字与做菜需要的刻数。"""
    name: str
    cook_ticks: int

class OrderState(Enum):
    PENDING = 'pending'
    COOKING = 'cooking'
    DELIVERING = 'delivering'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class RobotState(Enum):
    IDLE = 'idle'
    COOKING = 'cooking'
    DELIVERING = 'delivering'
    CHARGING = 'charging'

class EventKind(Enum):
    ASSIGNED = 'assigned'
    COOKED = 'cooked'
    DELIVERED = 'delivered'
    CHARGE_STARTED = 'charge_started'
    CHARGE_DONE = 'charge_done'
    CANCELLED = 'cancelled'

@dataclass(frozen=True, slots=True)
class Event:
    """发生了什么：订阅者靠它更新自己，不必回头读餐厅内部。"""
    tick: int
    kind: EventKind
    robot_id: int | None
    order_id: int | None

@dataclass(frozen=True, slots=True)
class Config:
    """餐厅参数。电量是 0–100 的整数百分点。"""
    chargers: int = 1
    deliver_ticks: int = 3
    cook_drain: int = 1
    move_drain: int = 2
    charge_rate: int = 10
    full: int = 100
    low_battery: int = 30
    reserve: int = 10

    def __post_init__(self) -> None:
        pass

    def job_cost(self, dish: Dish) -> int:
        """做完并送到一份菜要耗多少电。"""
        raise NotImplementedError

    @property
    def max_job_cost(self) -> int:
        """保证进度的上限：电量不低于 low_battery 的机器人，任何合法订单做完后仍不低于 reserve。"""
        raise NotImplementedError

@dataclass(slots=True)
class Order:
    id: int
    table: int
    dish: Dish
    state: OrderState = OrderState.PENDING

@dataclass(frozen=True, slots=True)
class RobotView:
    """机器人的只读快照；策略与调用方只看得到这个。"""
    id: int
    state: RobotState
    battery: int
    order_id: int | None
AssignmentPolicy = Callable[[Sequence[RobotView], Dish], int | None]

def first_idle(candidates: Sequence[RobotView], dish: Dish) -> int | None:
    """编号最小的候选。"""
    raise NotImplementedError

def most_battery(candidates: Sequence[RobotView], dish: Dish) -> int | None:
    """电量最多的候选；同电量取编号小的。"""
    raise NotImplementedError
_ALLOWED: dict[RobotState, frozenset[RobotState]] = {RobotState.IDLE: frozenset({RobotState.COOKING, RobotState.CHARGING}), RobotState.COOKING: frozenset({RobotState.DELIVERING}), RobotState.DELIVERING: frozenset({RobotState.IDLE}), RobotState.CHARGING: frozenset({RobotState.IDLE})}

class Robot:
    """一台机器人：自己拥有状态、电量、手上的订单与剩余刻数；每刻 `step()` 一次。"""

    def __init__(self, robot_id: int, battery: int, cfg: Config) -> None:
        raise NotImplementedError

    def _to(self, new: RobotState) -> None:
        raise NotImplementedError

    def view(self) -> RobotView:
        raise NotImplementedError

    def can_take(self, dish: Dish) -> bool:
        """空闲，且做完这单后电量仍不低于保底电量。"""
        raise NotImplementedError

    def start_job(self, order: Order) -> None:
        raise NotImplementedError

    def start_charging(self) -> None:
        raise NotImplementedError

    def step(self) -> EventKind | None:
        """走一刻；这一刻若完成了一个里程碑就返回它。"""
        raise NotImplementedError

class Restaurant:
    """餐厅：收单、排队、每刻推进机器人、把空闲机器人派给队首订单。"""

    def __init__(self, menu: Iterable[Dish], batteries: Sequence[int], config: Config=Config(), policy: AssignmentPolicy=first_idle) -> None:
        raise NotImplementedError

    @property
    def now(self) -> int:
        raise NotImplementedError

    @property
    def robots(self) -> tuple[RobotView, ...]:
        raise NotImplementedError

    @property
    def events(self) -> tuple[Event, ...]:
        raise NotImplementedError

    @property
    def pending_count(self) -> int:
        raise NotImplementedError

    def order_state(self, order_id: int) -> OrderState:
        raise NotImplementedError

    def place_order(self, table: int, dish_name: str) -> int:
        """收一张单，立即排进队尾，返回订单号。"""
        raise NotImplementedError

    def cancel_order(self, order_id: int) -> None:
        """只有还在排队的订单可以取消；机器人一旦接手就不行。"""
        raise NotImplementedError

    def tick(self) -> None:
        """推进一刻：先让每台机器人走一步，再安排充电，最后派单。三步顺序是设计的一部分。"""
        raise NotImplementedError

    def run_until_quiet(self, max_ticks: int=10000) -> int:
        """一直推进到没有排队订单、也没有机器人在做菜或送餐；返回用了多少刻。"""
        raise NotImplementedError

    def _order(self, order_id: int) -> Order:
        raise NotImplementedError

    def _log(self, kind: EventKind, robot: Robot | None, order: Order | None) -> None:
        raise NotImplementedError

    def _send_low_to_charge(self) -> None:
        """电量低的空闲机器人按「最低电量优先」去占空桩；没有空桩就留在原地等。"""
        raise NotImplementedError

    def _dispatch(self) -> None:
        """严格先来先服务：队首派不出去，后面的也不越过它。"""
        raise NotImplementedError
