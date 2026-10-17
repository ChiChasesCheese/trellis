"""机器人餐厅（Robot Restaurant）参考解。

设计五句话：
1. 时间是离散的「刻」（tick）：`Restaurant.tick()` 推进一刻，所有机器人各走一步，所以测试不需要睡眠或真实时钟。
2. `Robot` 是一台状态机（IDLE → COOKING → DELIVERING → IDLE，或 IDLE ↔ CHARGING），合法转移写成一张表，非法转移抛异常。
3. 「哪台机器人接这张单」是一个可替换的策略函数 `AssignmentPolicy`：输入空闲候选的只读视图，返回机器人编号。
4. 充电桩数不另设计数器：数一数处于 CHARGING 的机器人就是占用数；电量低于阈值且有空桩才去充，没桩就继续等或干活。
5. `Restaurant` 用一把锁保护「待处理队列 + 全部机器人 + 事件日志」，对外只给快照（`RobotView`、事件元组）。
"""

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
    PENDING = "pending"
    COOKING = "cooking"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class RobotState(Enum):
    IDLE = "idle"
    COOKING = "cooking"
    DELIVERING = "delivering"
    CHARGING = "charging"


class EventKind(Enum):
    ASSIGNED = "assigned"
    COOKED = "cooked"
    DELIVERED = "delivered"
    CHARGE_STARTED = "charge_started"
    CHARGE_DONE = "charge_done"
    CANCELLED = "cancelled"


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
        if self.chargers < 0 or self.charge_rate < 1 or self.deliver_ticks < 1:
            raise ValueError("chargers >= 0, charge_rate >= 1, deliver_ticks >= 1")
        if not 0 <= self.reserve < self.low_battery <= self.full:
            raise ValueError("需要 0 <= reserve < low_battery <= full")

    def job_cost(self, dish: Dish) -> int:
        """做完并送到一份菜要耗多少电。"""
        return dish.cook_ticks * self.cook_drain + self.deliver_ticks * self.move_drain

    @property
    def max_job_cost(self) -> int:
        """保证进度的上限：电量不低于 low_battery 的机器人，任何合法订单做完后仍不低于 reserve。"""
        return self.low_battery - self.reserve


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


# 一个策略 = 一个纯函数：从空闲候选里选一台，返回它的编号；没有合适的返回 None。
AssignmentPolicy = Callable[[Sequence[RobotView], Dish], int | None]


def first_idle(candidates: Sequence[RobotView], dish: Dish) -> int | None:
    """编号最小的候选。"""
    return min((r.id for r in candidates), default=None)


def most_battery(candidates: Sequence[RobotView], dish: Dish) -> int | None:
    """电量最多的候选；同电量取编号小的。"""
    best = max(candidates, key=lambda r: (r.battery, -r.id), default=None)
    return None if best is None else best.id


# 合法转移表：状态机的全部规则只在这一处。
_ALLOWED: dict[RobotState, frozenset[RobotState]] = {
    RobotState.IDLE: frozenset({RobotState.COOKING, RobotState.CHARGING}),
    RobotState.COOKING: frozenset({RobotState.DELIVERING}),
    RobotState.DELIVERING: frozenset({RobotState.IDLE}),
    RobotState.CHARGING: frozenset({RobotState.IDLE}),
}


class Robot:
    """一台机器人：自己拥有状态、电量、手上的订单与剩余刻数；每刻 `step()` 一次。"""

    def __init__(self, robot_id: int, battery: int, cfg: Config) -> None:
        self.id = robot_id
        self.battery = battery
        self.state = RobotState.IDLE
        self.order: Order | None = None
        self._remaining = 0
        self._cfg = cfg

    def _to(self, new: RobotState) -> None:
        if new not in _ALLOWED[self.state]:
            raise InvalidTransitionError(f"机器人 {self.id}: {self.state.name} -> {new.name}")
        self.state = new

    def view(self) -> RobotView:
        return RobotView(self.id, self.state, self.battery, self.order.id if self.order else None)

    def can_take(self, dish: Dish) -> bool:
        """空闲，且做完这单后电量仍不低于保底电量。"""
        return self.state is RobotState.IDLE and self.battery - self._cfg.job_cost(dish) >= self._cfg.reserve

    def start_job(self, order: Order) -> None:
        self._to(RobotState.COOKING)
        self.order = order
        self._remaining = order.dish.cook_ticks
        order.state = OrderState.COOKING

    def start_charging(self) -> None:
        self._to(RobotState.CHARGING)

    def step(self) -> EventKind | None:
        """走一刻；这一刻若完成了一个里程碑就返回它。"""
        cfg = self._cfg
        if self.state is RobotState.COOKING:
            assert self.order is not None
            self.battery -= cfg.cook_drain
            self._remaining -= 1
            if self._remaining == 0:
                self._to(RobotState.DELIVERING)
                self._remaining = cfg.deliver_ticks
                self.order.state = OrderState.DELIVERING
                return EventKind.COOKED
        elif self.state is RobotState.DELIVERING:
            assert self.order is not None
            self.battery -= cfg.move_drain
            self._remaining -= 1
            if self._remaining == 0:
                self.order.state = OrderState.DELIVERED
                self._to(RobotState.IDLE)
                return EventKind.DELIVERED
        elif self.state is RobotState.CHARGING:
            self.battery = min(cfg.full, self.battery + cfg.charge_rate)
            if self.battery == cfg.full:
                self._to(RobotState.IDLE)
                return EventKind.CHARGE_DONE
        return None


class Restaurant:
    """餐厅：收单、排队、每刻推进机器人、把空闲机器人派给队首订单。"""

    def __init__(
        self,
        menu: Iterable[Dish],
        batteries: Sequence[int],
        config: Config = Config(),
        policy: AssignmentPolicy = first_idle,
    ) -> None:
        self._menu = {d.name: d for d in menu}
        self._cfg = config
        self._policy = policy
        self._robots = [Robot(i, b, config) for i, b in enumerate(batteries)]
        self._orders: dict[int, Order] = {}
        self._pending: deque[Order] = deque()
        self._events: list[Event] = []
        self._now = 0
        self._next_id = 1
        self._lock = threading.Lock()

    # ---- 查询：全部返回快照 ----
    @property
    def now(self) -> int:
        with self._lock:
            return self._now

    @property
    def robots(self) -> tuple[RobotView, ...]:
        with self._lock:
            return tuple(r.view() for r in self._robots)

    @property
    def events(self) -> tuple[Event, ...]:
        with self._lock:
            return tuple(self._events)

    @property
    def pending_count(self) -> int:
        with self._lock:
            return len(self._pending)

    def order_state(self, order_id: int) -> OrderState:
        with self._lock:
            return self._order(order_id).state

    # ---- 命令 ----
    def place_order(self, table: int, dish_name: str) -> int:
        """收一张单，立即排进队尾，返回订单号。"""
        dish = self._menu.get(dish_name)
        if dish is None:
            raise UnknownDishError(dish_name)
        if self._cfg.job_cost(dish) > self._cfg.max_job_cost:
            raise OrderRejectedError(f"{dish_name} 耗电 {self._cfg.job_cost(dish)}，超过上限 {self._cfg.max_job_cost}")
        with self._lock:
            order = Order(self._next_id, table, dish)
            self._next_id += 1
            self._orders[order.id] = order
            self._pending.append(order)
            return order.id

    def cancel_order(self, order_id: int) -> None:
        """只有还在排队的订单可以取消；机器人一旦接手就不行。"""
        with self._lock:
            order = self._order(order_id)
            if order.state is not OrderState.PENDING:
                raise OrderNotCancellableError(f"订单 {order_id} 已是 {order.state.name}")
            self._pending.remove(order)
            order.state = OrderState.CANCELLED
            self._log(EventKind.CANCELLED, None, order)

    def tick(self) -> None:
        """推进一刻：先让每台机器人走一步，再安排充电，最后派单。三步顺序是设计的一部分。"""
        with self._lock:
            self._now += 1
            for robot in self._robots:
                kind = robot.step()
                if kind is not None:
                    self._log(kind, robot, robot.order if kind is not EventKind.CHARGE_DONE else None)
                    if kind is EventKind.DELIVERED:
                        robot.order = None
            self._send_low_to_charge()
            self._dispatch()

    def run_until_quiet(self, max_ticks: int = 10_000) -> int:
        """一直推进到没有排队订单、也没有机器人在做菜或送餐；返回用了多少刻。"""
        for used in range(max_ticks + 1):
            with self._lock:
                busy = bool(self._pending) or any(
                    r.state in (RobotState.COOKING, RobotState.DELIVERING) for r in self._robots
                )
            if not busy:
                return used
            self.tick()
        raise RestaurantError(f"{max_ticks} 刻内没有安静下来")

    # ---- 内部（调用时已持锁）----
    def _order(self, order_id: int) -> Order:
        try:
            return self._orders[order_id]
        except KeyError:
            raise UnknownOrderError(order_id) from None

    def _log(self, kind: EventKind, robot: Robot | None, order: Order | None) -> None:
        self._events.append(Event(self._now, kind, robot.id if robot else None, order.id if order else None))

    def _send_low_to_charge(self) -> None:
        """电量低的空闲机器人按「最低电量优先」去占空桩；没有空桩就留在原地等。"""
        used = sum(r.state is RobotState.CHARGING for r in self._robots)
        low = sorted(
            (r for r in self._robots if r.state is RobotState.IDLE and r.battery < self._cfg.low_battery),
            key=lambda r: (r.battery, r.id),
        )
        for robot in low[: max(0, self._cfg.chargers - used)]:
            robot.start_charging()
            self._log(EventKind.CHARGE_STARTED, robot, None)

    def _dispatch(self) -> None:
        """严格先来先服务：队首派不出去，后面的也不越过它。"""
        while self._pending:
            order = self._pending[0]
            candidates = [r.view() for r in self._robots if r.can_take(order.dish)]
            chosen = self._policy(candidates, order.dish)
            if chosen is None:
                return
            if chosen not in {c.id for c in candidates}:
                raise PolicyError(f"策略选了不可用的机器人 {chosen}")
            self._pending.popleft()
            robot = self._robots[chosen]
            robot.start_job(order)
            self._log(EventKind.ASSIGNED, robot, order)


if __name__ == "__main__":
    shop = Restaurant([Dish("面", 4), Dish("汤", 2)], batteries=(100, 100))
    first = shop.place_order(table=1, dish_name="面")
    second = shop.place_order(table=2, dish_name="汤")
    print("用了", shop.run_until_quiet(), "刻")
    print(shop.order_state(first), shop.order_state(second))
    for event in shop.events:
        print(event)
