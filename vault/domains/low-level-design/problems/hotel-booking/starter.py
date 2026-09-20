"""酒店预订（Hotel Booking）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/hotel-booking -q
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class HotelError(Exception):
    """本设计里所有失败路径的公共基类。"""


class InvalidStayError(HotelError):
    """日期区间不合法：退房日期不晚于入住日期。"""


class NoAvailabilityError(HotelError):
    """这段日期里至少有一晚订不到这个房型——整笔预订都不成立。"""


class HotelNotFoundError(HotelError):
    """目录里没有这家酒店。"""


class BookingNotFoundError(HotelError):
    """订单号不存在。"""


class InvalidTransitionError(HotelError):
    """订单当前状态不允许这次状态转移。"""


class NoRoomToAssignError(HotelError):
    """前台没有这个房型的空房可分配——超卖兑现失败。"""


class RoomType(Enum):
    """房型。库存、定价、超卖全部按房型统计。"""

    SINGLE = "single"
    DOUBLE = "double"
    DELUXE = "deluxe"
    SUITE = "suite"


@dataclass(frozen=True, slots=True)
class Room:
    """一间物理客房，不带"这几天被谁订了"的状态。"""

    number: str
    type: RoomType
    floor: int = 1


@dataclass(frozen=True, slots=True)
class Stay:
    """一次入住的日期区间，**半开**：`[check_in, check_out)`，占用其中每一晚。"""

    check_in: date
    check_out: date

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def nights(self) -> int:
        """住几晚。"""
        raise NotImplementedError

    def each_night(self) -> Iterator[date]:
        """逐晚迭代：第一晚是入住日，最后一晚是退房日的前一天。"""
        raise NotImplementedError

    def overlaps(self, other: "Stay") -> bool:
        """两段入住是否共用至少一晚。"""
        raise NotImplementedError


OverbookingPolicy = Callable[[RoomType, date, int], int]
NightlyRate = Callable[[RoomType, date, int], int]
Clock = Callable[[], datetime]


def no_overbooking(room_type: RoomType, night: date, capacity: int) -> int:
    """不超卖：可订量就是实际房量。"""
    raise NotImplementedError


def percent_overbooking(percent: int) -> OverbookingPolicy:
    """按房量的百分比超卖，对冲爽约（no-show）。"""
    raise NotImplementedError


def weekday_overbooking(percent: int) -> OverbookingPolicy:
    """只在周一到周四超卖。"""
    raise NotImplementedError


def flat_nightly(prices: Mapping[RoomType, int]) -> NightlyRate:
    """按房型给一张每晚房价表，单位是分。"""
    raise NotImplementedError


def weekend_uplift(base: NightlyRate, numerator: int, denominator: int) -> NightlyRate:
    """周五、周六两晚按整数分数加价。"""
    raise NotImplementedError


def scarcity_uplift(base: NightlyRate, threshold: int, numerator: int, denominator: int) -> NightlyRate:
    """剩余可订量低于阈值时加价；剩余量是传进来的，不去读 `Inventory`。"""
    raise NotImplementedError


class Inventory:
    """一家酒店的按夜库存：房量固定，已订数按 (房型, 日期) 逐晚记。"""

    def __init__(self, capacity: Mapping[RoomType, int],
                 overbooking: OverbookingPolicy = no_overbooking) -> None:
        raise NotImplementedError

    @property
    def tracked_nights(self) -> int:
        """计数表里当前有多少个非零格子。"""
        raise NotImplementedError

    def capacity_of(self, room_type: RoomType) -> int:
        """这个房型一共有几间实体房。"""
        raise NotImplementedError

    def _available_locked(self, room_type: RoomType, night: date) -> int:
        """某一晚还能订几间；调用方必须已经持有锁。"""
        raise NotImplementedError

    def available_on(self, room_type: RoomType, night: date) -> int:
        """某一晚这个房型还能订几间（已计入超卖额度）。"""
        raise NotImplementedError

    def min_available(self, room_type: RoomType, stay: Stay) -> int:
        """整段入住期间最紧的那一晚还剩几间。"""
        raise NotImplementedError

    def reserve(self, room_type: RoomType, stay: Stay) -> None:
        """为整段入住各占一间，全有或全无；任一晚不足就抛 `NoAvailabilityError`。"""
        raise NotImplementedError

    def release(self, room_type: RoomType, stay: Stay) -> None:
        """退掉整段入住占的库存；计数减到 0 的格子直接删键。"""
        raise NotImplementedError

    def purge_nights_before(self, cutoff: date) -> int:
        """清掉 `cutoff` 之前的历史晚次，返回清掉的格子数。"""
        raise NotImplementedError


class FrontDesk:
    """一家酒店的前台：入住时分配实体房间，退房时收回。"""

    def __init__(self, rooms: Iterable[Room]) -> None:
        raise NotImplementedError

    @property
    def occupied_count(self) -> int:
        """当前有人住的房间数。"""
        raise NotImplementedError

    def occupancy(self) -> Mapping[str, str]:
        """当前"房号 → 订单号"的一份快照副本。"""
        raise NotImplementedError

    def assign(self, room_type: RoomType, booking_id: str) -> Room:
        """给订单挑一间该房型的空房；没有空房时抛 `NoRoomToAssignError`。"""
        raise NotImplementedError

    def release_room(self, room_number: str) -> None:
        """退房：按房号把房间收回。"""
        raise NotImplementedError


class Hotel:
    """一家酒店：实体房间，以及属于它自己的 `Inventory` 和 `FrontDesk`。"""

    def __init__(self, hotel_id: str, name: str, city: str, rooms: Iterable[Room],
                 overbooking: OverbookingPolicy = no_overbooking) -> None:
        raise NotImplementedError

    def room_types(self) -> tuple[RoomType, ...]:
        """这家店有哪些房型。"""
        raise NotImplementedError


class BookingStatus(Enum):
    """订单生命周期的四个状态。"""

    RESERVED = "reserved"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS: Mapping[BookingStatus, frozenset[BookingStatus]] = {
    BookingStatus.RESERVED: frozenset({BookingStatus.CHECKED_IN, BookingStatus.CANCELLED}),
    BookingStatus.CHECKED_IN: frozenset({BookingStatus.CHECKED_OUT}),
    BookingStatus.CHECKED_OUT: frozenset(),
    BookingStatus.CANCELLED: frozenset(),
}
"""合法转移写成一张数据表，而不是散落在各个方法里的 `if`。"""


@dataclass(slots=True)
class Booking:
    """一笔预订：只认房型，房号是入住后才填上的。"""

    id: str
    hotel_id: str
    guest: str
    room_type: RoomType
    stay: Stay
    amount: int
    status: BookingStatus = BookingStatus.RESERVED
    room_number: str | None = None

    def transition_to(self, new_status: BookingStatus) -> None:
        """按转移表改状态；不合法的转移抛 `InvalidTransitionError`。"""
        raise NotImplementedError


class HotelService:
    """酒店预订服务：跨店搜索、下单、取消、入住、退房，以及清理历史晚次。"""

    def __init__(self, clock: Clock, rate: NightlyRate) -> None:
        raise NotImplementedError

    def register(self, hotel: Hotel) -> None:
        """把一家酒店加进目录。"""
        raise NotImplementedError

    def hotel(self, hotel_id: str) -> Hotel:
        """按 id 取酒店；不存在就抛 `HotelNotFoundError`。"""
        raise NotImplementedError

    def search(self, city: str, room_type: RoomType, stay: Stay) -> tuple[Hotel, ...]:
        """某城市里，整段日期每一晚都还有这个房型的酒店。"""
        raise NotImplementedError

    def quote(self, hotel_id: str, room_type: RoomType, stay: Stay) -> int:
        """整段入住的总价（分）：逐晚算，把那一晚的剩余可订量喂给定价函数。"""
        raise NotImplementedError

    def purge_nights_before(self, cutoff: date) -> int:
        """跨所有酒店清掉历史晚次。"""
        raise NotImplementedError

    def book(self, hotel_id: str, room_type: RoomType, stay: Stay, guest: str) -> Booking:
        """下单：先报价，再原子地占掉整段库存，最后落订单。"""
        raise NotImplementedError

    def booking(self, booking_id: str) -> Booking:
        """按订单号取订单。"""
        raise NotImplementedError

    def cancel(self, booking_id: str) -> Booking:
        """取消预订：把整段库存还回去。"""
        raise NotImplementedError

    def check_in(self, booking_id: str) -> Room:
        """办理入住：分配一间实体房，并把订单推进 CHECKED_IN。"""
        raise NotImplementedError

    def check_out(self, booking_id: str) -> Booking:
        """办理退房：收回房间，订单推进 CHECKED_OUT；**不**归还库存。"""
        raise NotImplementedError
