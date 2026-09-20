"""航班管理（Airline Management）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/airline -q
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum, IntEnum


class AirlineError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownFlightError(AirlineError):
    """目录里没有这个航班实例。"""

class NoSeatsAvailableError(AirlineError):
    """行程里至少有一段的这个舱位已经售罄（含超售额度）。"""

class InvalidItineraryError(AirlineError):
    """行程本身不合法：空行程、机场接不上，或中转时间短于最短衔接时间。"""

class SeatUnavailableError(AirlineError):
    """指定的座位号不存在、不属于这个舱位，或者已经被别人选走了。"""

class BookingNotFoundError(AirlineError):
    """订单号不存在。"""

class InvalidTransitionError(AirlineError):
    """订单当前状态不允许这次状态转移。"""

class HoldExpiredError(AirlineError):
    """占座已经超时释放，不能再拿它出票。"""


class CabinClass(IntEnum):
    """舱位等级，数值越大越贵。"""

    ECONOMY = 1
    PREMIUM = 2
    BUSINESS = 3
    FIRST = 4


@dataclass(frozen=True, slots=True)
class Seat:
    """机舱里的一把物理座椅，不带"这一班被谁占了"的状态。"""

    cabin: CabinClass
    row: int
    letter: str

    @property
    def label(self) -> str:
        """座位号，比如 `"12C"`。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Aircraft:
    """一种客舱布局：座位表固定，被排班表上所有用它的航班共用。"""

    id: str
    model: str
    seats: tuple[Seat, ...]

    @classmethod
    def layout(cls, aircraft_id: str, model: str,
               cabins: Mapping[CabinClass, tuple[int, str]]) -> "Aircraft":
        """按"每个舱位几排、每排哪些字母"生成座位表；排号从高舱位往低舱位连续编下去。"""
        raise NotImplementedError

    def seats_in(self, cabin: CabinClass) -> tuple[Seat, ...]:
        """某个舱位的座位快照，按排号顺序。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Flight:
    """排班表上的一行，**没有日期**；`marketed_as` 是代码共享用的市场航班号。"""

    number: str
    origin: str
    destination: str
    departs_at: time
    duration: timedelta
    aircraft: Aircraft
    operated_by: str
    marketed_as: tuple[str, ...] = ()


OverbookingPolicy = Callable[[CabinClass, "FlightInstance"], int]
FarePolicy = Callable[["Itinerary"], int]
RefundPolicy = Callable[["Booking", datetime], int]
Clock = Callable[[], datetime]


def no_overbooking(cabin: CabinClass, instance: "FlightInstance") -> int:
    """不超售：可售数就是实际座位数。"""
    raise NotImplementedError


def percent_overbooking(by_cabin: Mapping[CabinClass, int]) -> OverbookingPolicy:
    """按舱位给一个超售百分比。"""
    raise NotImplementedError


def cabin_fare(prices: Mapping[CabinClass, int]) -> FarePolicy:
    """按舱位逐段累加票价，单位是"分"。"""
    raise NotImplementedError


def no_refund(booking: "Booking", now: datetime) -> int:
    """一律不退。"""
    raise NotImplementedError


def tiered_refund(tiers: Sequence[tuple[timedelta, int]]) -> RefundPolicy:
    """按"离首段起飞还有多久"分档退款。"""
    raise NotImplementedError


class FlightInstance:
    """某一天的那一班：这一班的舱位库存、座位图和一把私有锁都在这里。"""

    def __init__(self, flight: Flight, service_date: date,
                 overbooking: OverbookingPolicy = no_overbooking) -> None:
        raise NotImplementedError

    @property
    def key(self) -> str:
        """`航班号@执飞日期`。"""
        raise NotImplementedError

    @property
    def departure(self) -> datetime:
        """起飞时刻。"""
        raise NotImplementedError

    @property
    def arrival(self) -> datetime:
        """落地时刻。"""
        raise NotImplementedError

    def capacity(self, cabin: CabinClass) -> int:
        """这个舱位真实有几把椅子。"""
        raise NotImplementedError

    def authorized(self, cabin: CabinClass) -> int:
        """这个舱位允许卖出几张票 = 座位数 + 超售额度。"""
        raise NotImplementedError

    def available(self, cabin: CabinClass) -> int:
        """这个舱位还能卖几张票。"""
        raise NotImplementedError

    def refs_in(self, cabin: CabinClass) -> tuple[str, ...]:
        """这个舱位的旅客订单号快照，按订单号排序。"""
        raise NotImplementedError

    @classmethod
    def reserve_across(cls, requests: Sequence[tuple["FlightInstance", CabinClass]],
                       ref: str) -> None:
        """跨若干航班实例一次性占位：全部占上，或者一个都不占。"""
        raise NotImplementedError

    def release(self, ref: str) -> bool:
        """把一个订单从这一班上摘掉，连同它的座位。幂等。"""
        raise NotImplementedError

    def assign_seat(self, ref: str, preferred: str | None = None) -> str | None:
        """选座：本舱没有空位时返回 `None`；点名的座位拿不到才抛异常。"""
        raise NotImplementedError

    def seat_of(self, ref: str) -> str | None:
        """这个订单在这一班上的座位号，没选到就是 `None`。"""
        raise NotImplementedError

    def free_seats(self, cabin: CabinClass) -> tuple[str, ...]:
        """本舱还没被选走的座位号快照。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Segment:
    """旅客行程里的一段：他在某一班上占的一个舱位。"""

    instance: FlightInstance
    cabin: CabinClass

    @property
    def departure(self) -> datetime:
        """这一段的起飞时刻。"""
        raise NotImplementedError

    @property
    def arrival(self) -> datetime:
        """这一段的落地时刻。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Itinerary:
    """一条行程：按时间排好的若干航段，订座的原子单位。"""

    segments: tuple[Segment, ...]

    @property
    def origin(self) -> str:
        """全程出发机场。"""
        raise NotImplementedError

    @property
    def destination(self) -> str:
        """全程到达机场。"""
        raise NotImplementedError

    @property
    def departure(self) -> datetime:
        """首段起飞时刻。"""
        raise NotImplementedError

    @property
    def arrival(self) -> datetime:
        """末段落地时刻。"""
        raise NotImplementedError

    @property
    def stops(self) -> int:
        """中转次数。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class MinimumConnectionTime:
    """最短衔接时间（MCT）表：按机场给基准，换承运人再加一档。"""

    default: timedelta
    by_airport: Mapping[str, timedelta] = field(default_factory=dict)
    carrier_change: timedelta = timedelta(0)

    def required(self, arriving: Segment, departing: Segment) -> timedelta:
        """这次中转至少需要多少时间。"""
        raise NotImplementedError

    def connects(self, arriving: Segment, departing: Segment) -> bool:
        """前一段能不能接上后一段。"""
        raise NotImplementedError


class BookingStatus(Enum):
    """订单生命周期。"""

    HELD = "held"
    TICKETED = "ticketed"
    CHECKED_IN = "checked_in"
    BOARDED = "boarded"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS: Mapping[BookingStatus, frozenset[BookingStatus]] = {
    BookingStatus.HELD: frozenset({BookingStatus.TICKETED, BookingStatus.CANCELLED}),
    BookingStatus.TICKETED: frozenset({BookingStatus.CHECKED_IN, BookingStatus.CANCELLED}),
    BookingStatus.CHECKED_IN: frozenset({BookingStatus.BOARDED, BookingStatus.TICKETED,
                                         BookingStatus.CANCELLED}),
    BookingStatus.BOARDED: frozenset(),
    BookingStatus.CANCELLED: frozenset(),
}


@dataclass(slots=True)
class Booking:
    """一张订单：行程、旅客、票价（整数"分"）、状态。"""

    id: str
    itinerary: Itinerary
    passenger: str
    fare: int
    created_at: datetime
    held_until: datetime
    status: BookingStatus = BookingStatus.HELD
    checked_in_at: datetime | None = None
    boarded: tuple[str, ...] = ()
    refunded: int = 0

    def transition_to(self, target: BookingStatus) -> None:
        """按转移表改状态；非法迁移抛 `InvalidTransitionError`。"""
        raise NotImplementedError


class AirlineService:
    """门面：查行程、占座、出票、值机、登机、取消、改签，外加清扫与历史清理。"""

    def __init__(self, clock: Clock, connection: MinimumConnectionTime, fare: FarePolicy,
                 refund: RefundPolicy = no_refund,
                 hold_ttl: timedelta = timedelta(minutes=20),
                 check_in_opens: timedelta = timedelta(hours=24),
                 check_in_closes: timedelta = timedelta(minutes=45)) -> None:
        raise NotImplementedError

    def schedule(self, instance: FlightInstance) -> None:
        """把某一天的某一班上架；代码共享的市场航班号登记成别名。"""
        raise NotImplementedError

    def instance(self, key: str) -> FlightInstance:
        """按 `航班号@日期` 取一班；市场航班号也能取到同一班。"""
        raise NotImplementedError

    @property
    def instance_count(self) -> int:
        """目录里还有几班（按对象去重）。"""
        raise NotImplementedError

    @property
    def booking_count(self) -> int:
        """订单表里还有几张单。"""
        raise NotImplementedError

    @property
    def route_index_size(self) -> int:
        """`(出发机场, 日期) → 航班` 这张二级索引里还有多少个非空桶。"""
        raise NotImplementedError

    def search(self, origin: str, destination: str, day: date, cabin: CabinClass,
               max_stops: int = 1) -> tuple[Itinerary, ...]:
        """查这一天这条航线上还有票的行程，按落地时间排序。"""
        raise NotImplementedError

    def purge_flown_before(self, cutoff: datetime) -> int:
        """把已经落地的航班实例（和终结的历史订单）清掉，返回摘掉的班数。"""
        raise NotImplementedError

    def hold(self, itinerary: Itinerary, passenger: str) -> Booking:
        """占座：整条行程一次性占上，拿到一张有过期时间的订单。"""
        raise NotImplementedError

    def booking(self, booking_id: str) -> Booking:
        """按订单号取订单。"""
        raise NotImplementedError

    def ticket(self, booking_id: str) -> Booking:
        """出票：占座没过期就把 HELD 翻成 TICKETED。"""
        raise NotImplementedError

    def release_expired_holds(self) -> int:
        """清扫所有超时未出票的占座，返回释放的订单数。"""
        raise NotImplementedError

    def check_in(self, booking_id: str,
                 preferred: Mapping[str, str] | None = None) -> Mapping[str, str]:
        """值机：在窗口期内给每一段选座，返回 `航班key → 座位号` 的只读快照。"""
        raise NotImplementedError

    def board(self, flight_key: str) -> tuple[str, ...]:
        """关舱门结算：送上飞机，卖超的按公开规则拒载，返回被拒载的订单号。"""
        raise NotImplementedError

    def cancel(self, booking_id: str) -> Booking:
        """取消：认领状态、算退款、还库存。"""
        raise NotImplementedError

    def change(self, booking_id: str, new_itinerary: Itinerary) -> Booking:
        """改签：换一条行程，先占新段再放旧段。"""
        raise NotImplementedError
