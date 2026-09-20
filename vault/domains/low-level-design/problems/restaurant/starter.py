"""餐厅管理（Restaurant Management）——起始模板：把每个方法体补完。"""

from __future__ import annotations

import itertools
import threading
from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable

Clock = Callable[[], datetime]


class RestaurantError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownTableError(RestaurantError):
    """桌号不存在。"""

class UnknownOrderError(RestaurantError):
    """点单号，或点单里的某一行菜号，不存在。"""

class UnknownReservationError(RestaurantError):
    """预订号不存在，或已经被使用过。"""

class TableOccupiedError(RestaurantError):
    """这张桌子已经坐着人，不能重复入座。"""

class NoTableAvailableError(RestaurantError):
    """没有任何一张桌子能在这个时段坐下这么多人。"""

class ItemUnavailableError(RestaurantError):
    """点的菜里有一道（或多道）此刻做不了。"""

class IllegalLineTransitionError(RestaurantError):
    """这道菜的状态机里根本没有这条边。"""

class SplitMismatchError(RestaurantError):
    """拆账的参数和账单对不上：份额非法，或者按菜分账没有覆盖每一件已上桌的菜。"""

class SettlementError(RestaurantError):
    """这张单还没结清，或者还有菜在路上，不能关单清台。"""


class Course(Enum):
    STARTER = 1
    MAIN = 2
    DESSERT = 3


@dataclass(frozen=True, slots=True)
class MenuItem:
    id: str
    name: str
    price: int
    course: Course


class TableStatus(Enum):
    FREE = "free"
    OCCUPIED = "occupied"


class Table:
    """一张桌子：容量固定不变，占用状态可以转移。"""

    def __init__(self, table_id: str, capacity: int) -> None:
        raise NotImplementedError

    @property
    def status(self) -> TableStatus:
        raise NotImplementedError

    def occupy(self) -> None:
        raise NotImplementedError

    def free(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Reservation:
    id: str
    table_id: str
    party_size: int
    start: datetime
    duration: timedelta

    @property
    def end(self) -> datetime:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class WaitlistEntry:
    id: str
    party_size: int
    joined_at: datetime


@dataclass(frozen=True, slots=True)
class SeatingResult:
    table_id: str | None
    waitlist_id: str | None


class FloorManager:
    """前厅：桌位分配、按时段预订、候位名单。"""

    def __init__(self, clock: Clock, grace: timedelta = timedelta(minutes=30)) -> None:
        raise NotImplementedError

    def add_table(self, table: Table) -> None:
        raise NotImplementedError

    def table(self, table_id: str) -> Table:
        raise NotImplementedError

    @property
    def waitlist_length(self) -> int:
        raise NotImplementedError

    @property
    def reservation_count(self) -> int:
        raise NotImplementedError

    def seat_walk_in(self, party_size: int, now: datetime) -> SeatingResult:
        raise NotImplementedError

    def reserve(self, party_size: int, start: datetime, duration: timedelta) -> Reservation:
        raise NotImplementedError

    def seat_reservation(self, reservation_id: str) -> SeatingResult:
        raise NotImplementedError

    def clear_table(self, table_id: str) -> None:
        raise NotImplementedError

    def seat_from_waitlist(self, table_id: str, now: datetime) -> SeatingResult | None:
        raise NotImplementedError


class OrderKind(Enum):
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"


class LineState(Enum):
    ORDERED = "ordered"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    UNAVAILABLE = "unavailable"


LINE_TRANSITIONS: Mapping[LineState, frozenset[LineState]] = {
    LineState.ORDERED: frozenset({LineState.PREPARING, LineState.UNAVAILABLE}),
    LineState.PREPARING: frozenset({LineState.READY}),
    LineState.READY: frozenset({LineState.SERVED}),
    LineState.SERVED: frozenset(),
    LineState.UNAVAILABLE: frozenset(),
}


class OrderLine:
    """点单里的一行：数量、下单那一刻的价格快照、以及它在后厨的状态机。"""

    def __init__(self, line_id: str, order_id: str, menu_item: MenuItem, quantity: int) -> None:
        raise NotImplementedError

    @property
    def state(self) -> LineState:
        raise NotImplementedError

    @property
    def amount(self) -> int:
        raise NotImplementedError

    def transition_to(self, target: LineState) -> None:
        raise NotImplementedError


class Order:
    """一张点单：堂食挂在一张桌上，外带/外送则不挂桌。账单只认已经上桌的菜。"""

    def __init__(self, order_id: str, kind: OrderKind, table_id: str | None) -> None:
        raise NotImplementedError

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        raise NotImplementedError

    def add_line(self, line: OrderLine) -> None:
        raise NotImplementedError

    def discard_line(self, line_id: str) -> None:
        raise NotImplementedError

    def line(self, line_id: str) -> OrderLine:
        raise NotImplementedError

    @property
    def served_total(self) -> int:
        raise NotImplementedError

    @property
    def paid_total(self) -> int:
        raise NotImplementedError

    @property
    def balance_due(self) -> int:
        raise NotImplementedError

    def record_payment(self, amount: int) -> None:
        raise NotImplementedError

    def pending_lines(self) -> tuple[OrderLine, ...]:
        raise NotImplementedError

    def is_settled(self) -> bool:
        raise NotImplementedError


class Kitchen:
    """后厨：点单进来的菜排成一条队列，课程序号更小的必须先就绪，缺货整批拒收。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def submit(self, order: Order, lines: Sequence[OrderLine]) -> None:
        raise NotImplementedError

    def start_next(self) -> OrderLine | None:
        raise NotImplementedError

    def mark_ready(self, line: OrderLine) -> None:
        raise NotImplementedError

    def mark_unavailable(self, menu_item_id: str) -> tuple[OrderLine, ...]:
        raise NotImplementedError

    def restock(self, menu_item_id: str) -> None:
        raise NotImplementedError

    def forget_order(self, order_id: str) -> None:
        raise NotImplementedError

    @property
    def queue_length(self) -> int:
        raise NotImplementedError

    @property
    def known_order_count(self) -> int:
        raise NotImplementedError


def split_even(amount: int, payer_count: int) -> tuple[int, ...]:
    raise NotImplementedError


def split_by_share(amount: int, shares: Sequence[int]) -> tuple[int, ...]:
    raise NotImplementedError


def split_by_item(lines: Sequence[OrderLine], assignment: Mapping[str, tuple[str, ...]]
                   ) -> Mapping[str, int]:
    raise NotImplementedError


class RestaurantService:
    """餐厅：入座与候位、点单进后厨、上菜、结账；外带外送走同一条点单流水线，不碰桌位。"""

    def __init__(self, clock: Clock, floor: FloorManager, kitchen: Kitchen) -> None:
        raise NotImplementedError

    def add_menu_item(self, item: MenuItem) -> None:
        raise NotImplementedError

    def order(self, order_id: str) -> Order:
        raise NotImplementedError

    def seat_walk_in(self, party_size: int) -> tuple[Order | None, str | None]:
        raise NotImplementedError

    def reserve(self, party_size: int, start: datetime, duration: timedelta) -> Reservation:
        raise NotImplementedError

    def seat_reservation(self, reservation_id: str) -> Order:
        raise NotImplementedError

    def reseat_waitlist(self, table_id: str) -> Order | None:
        raise NotImplementedError

    def open_takeaway_order(self) -> Order:
        raise NotImplementedError

    def open_delivery_order(self) -> Order:
        raise NotImplementedError

    def submit_items(self, order_id: str, requests: Sequence[tuple[str, int]]
                     ) -> tuple[OrderLine, ...]:
        raise NotImplementedError

    def start_next_in_kitchen(self) -> OrderLine | None:
        raise NotImplementedError

    def mark_ready(self, order_id: str, line_id: str) -> OrderLine:
        raise NotImplementedError

    def serve(self, order_id: str, line_id: str) -> OrderLine:
        raise NotImplementedError

    def mark_unavailable(self, menu_item_id: str) -> tuple[OrderLine, ...]:
        raise NotImplementedError

    def record_payment(self, order_id: str, amount: int) -> None:
        raise NotImplementedError

    def close_order(self, order_id: str) -> Order:
        raise NotImplementedError

    def floor_status(self) -> Mapping[str, tuple[OrderLine, ...]]:
        raise NotImplementedError
