"""电影订票（BookMyShow）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass` 和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/movie-booking -q
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, IntEnum


class BookingError(Exception):
    """本设计里所有失败路径的公共基类。"""


class UnknownSeatError(BookingError):
    """请求的座位号在这个影厅里不存在。"""


class SeatNotAvailableError(BookingError):
    """请求的座位里至少有一个已经被别人锁住或卖掉了——整笔请求都不成立。"""


class HoldExpiredError(BookingError):
    """锁座收据已经过期（或已经被释放、被用掉），不能再拿它下单。"""


class PaymentFailedError(BookingError):
    """支付网关拒绝了这笔付款，座位已经退回。"""


class ShowNotFoundError(BookingError):
    """目录里没有这个场次。"""


class BookingNotFoundError(BookingError):
    """订单号不存在。"""


class CancellationNotAllowedError(BookingError):
    """这张订单现在不允许取消：已经取消过，或者场次已经开演。"""


class SeatType(IntEnum):
    NORMAL = 1
    PREMIUM = 2
    RECLINER = 3


@dataclass(frozen=True, slots=True)
class Seat:
    """影厅里的一把物理椅子，不带任何"卖没卖掉"的状态。"""

    row: str
    number: int
    type: SeatType = SeatType.NORMAL

    @property
    def label(self) -> str:
        """座位在影厅内的唯一标识，比如 `"C7"`。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Screen:
    """一个影厅：一串固定的座位，被这个厅的所有场次共用。"""

    id: str
    seats: tuple[Seat, ...]

    @classmethod
    def grid(cls, screen_id: str, rows: Sequence[str], seats_per_row: int,
             types: Mapping[str, SeatType] | None = None) -> "Screen":
        """按"几排乘几座"快速造一个影厅；`types` 给个别排指定档次。"""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Cinema:
    """一家影院：属于某个城市，有若干影厅。城市只是一个字符串，不单开 `City` 类。"""

    id: str
    name: str
    city: str
    screens: tuple[Screen, ...] = ()


@dataclass(frozen=True, slots=True)
class Movie:
    """一部电影：时长决定场次什么时候散场。"""

    id: str
    title: str
    duration: timedelta


class SeatStatus(Enum):
    """一个座位在**某一场**里的三种状态。"""

    AVAILABLE = "available"
    HELD = "held"
    BOOKED = "booked"


@dataclass(frozen=True, slots=True)
class _Slot:
    """`Show` 内部的一格座位状态，不可变；改状态靠 `dataclasses.replace` 整格换掉。"""

    status: SeatStatus
    hold_id: str | None = None
    user_id: str | None = None
    booking_id: str | None = None
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class SeatHold:
    """一张锁座收据：哪一场、哪几个座、谁锁的、什么时候作废。"""

    id: str
    show_id: str
    seat_labels: tuple[str, ...]
    user_id: str
    expires_at: datetime


class BookingStatus(Enum):
    """订单只有两个状态：付过钱的和退掉的——"已选座未付款"由 `SeatHold` 表达。"""

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class Booking:
    """一张成交的订单。金额一律是整数的"分"。"""

    id: str
    show_id: str
    user_id: str
    seat_labels: tuple[str, ...]
    amount: int
    created_at: datetime
    status: BookingStatus = BookingStatus.CONFIRMED
    refunded: int = 0


Clock = Callable[[], datetime]
PaymentGateway = Callable[[str, int], bool]
PricingStrategy = Callable[[Seat, "Show"], int]
CancellationPolicy = Callable[[Booking, "Show", datetime], int]


def by_seat_type(prices: Mapping[SeatType, int]) -> PricingStrategy:
    """按座位档次定价，单位是分。"""
    raise NotImplementedError


def row_surcharge(base: PricingStrategy, extra_by_row: Mapping[str, int]) -> PricingStrategy:
    """在任意一种定价之上，给指定的排加价。"""
    raise NotImplementedError


def weekend_multiplier(base: PricingStrategy, numerator: int, denominator: int) -> PricingStrategy:
    """周末按整数分数加价，整数运算避免浮点分币误差。"""
    raise NotImplementedError


def no_refund(booking: Booking, show: "Show", now: datetime) -> int:
    """一律不退款。"""
    raise NotImplementedError


def tiered_refund(tiers: Sequence[tuple[timedelta, int]]) -> CancellationPolicy:
    """按"离开演还有多久"分档退款：`tiers` 是 (提前量, 退款百分比)。"""
    raise NotImplementedError


class Show:
    """一场放映：持有这一场的座位库存，一把自己的锁保护它。"""

    def __init__(self, show_id: str, movie: Movie, screen: Screen, cinema: Cinema,
                 starts_at: datetime, clock: Clock) -> None:
        raise NotImplementedError

    @property
    def ends_at(self) -> datetime:
        """散场时间，由电影时长算出。"""
        raise NotImplementedError

    @property
    def seat_count(self) -> int:
        """这一场总共有多少座。"""
        raise NotImplementedError

    def seat(self, label: str) -> Seat:
        """按座位号取那把物理椅子；不存在就抛 `UnknownSeatError`。"""
        raise NotImplementedError

    @staticmethod
    def _effective(slot: _Slot, now: datetime) -> SeatStatus:
        """惰性过期：一格 HELD 只要过了时间，对外就已经是 AVAILABLE。"""
        raise NotImplementedError

    def seat_status(self, label: str) -> SeatStatus:
        """某个座位此刻对外的状态（已经考虑过期）。"""
        raise NotImplementedError

    def available_seats(self) -> tuple[Seat, ...]:
        """当前可选座位的一份不可变快照。"""
        raise NotImplementedError

    def count_by_status(self) -> Mapping[SeatStatus, int]:
        """三种状态各有多少座的只读计数快照。"""
        raise NotImplementedError

    def _live_labels(self, hold: SeatHold, now: datetime) -> tuple[str, ...]:
        """收据还活着时返回它占着的座位号，否则抛 `HoldExpiredError`；需已持有锁。"""
        raise NotImplementedError

    def hold(self, seat_labels: Iterable[str], user_id: str, ttl: timedelta) -> SeatHold:
        """锁住一批座位 `ttl` 这么久，全成功或全失败，返回一张收据。"""
        raise NotImplementedError

    def extend_hold(self, hold: SeatHold, window: timedelta) -> SeatHold:
        """把收据的有效期重置为"从现在起 `window`"，返回刷新后的收据。"""
        raise NotImplementedError

    def commit(self, hold: SeatHold, booking_id: str) -> None:
        """把收据上的座位从 HELD 翻成 BOOKED；收据已失效则抛 `HoldExpiredError`。"""
        raise NotImplementedError

    def release(self, hold: SeatHold) -> int:
        """主动放弃一张收据，返回真正退回的座位数；幂等且不抛异常。"""
        raise NotImplementedError

    def release_expired(self) -> int:
        """把所有过期的 HELD 真正写回 AVAILABLE，返回清掉的座位数。"""
        raise NotImplementedError

    def release_booking(self, booking_id: str) -> int:
        """退票：把这张订单占的 BOOKED 座位退回 AVAILABLE。"""
        raise NotImplementedError


class BookingService:
    """订票服务：管目录、算钱、调支付、记订单；座位状态全部委托给 `Show`。"""

    def __init__(self, clock: Clock, pricing: PricingStrategy,
                 cancellation: CancellationPolicy = no_refund,
                 hold_ttl: timedelta = timedelta(minutes=10),
                 payment_window: timedelta = timedelta(minutes=2)) -> None:
        raise NotImplementedError

    def schedule(self, show: Show) -> None:
        """把一场放映上架。"""
        raise NotImplementedError

    def show(self, show_id: str) -> Show:
        """按 id 取场次；不在目录里就抛 `ShowNotFoundError`。"""
        raise NotImplementedError

    def shows_in_city(self, city: str, movie_id: str | None = None) -> tuple[Show, ...]:
        """某城市（可再限定某部电影）在映场次的快照，按开演时间排序。"""
        raise NotImplementedError

    def purge_shows_ended_before(self, cutoff: datetime) -> int:
        """把已经散场的场次从目录里摘掉，返回摘掉的场次数。"""
        raise NotImplementedError

    def quote(self, show_id: str, seat_labels: Iterable[str]) -> int:
        """报价：这批座位一共多少分。"""
        raise NotImplementedError

    def hold(self, show_id: str, seat_labels: Iterable[str], user_id: str) -> SeatHold:
        """选座：按服务配置的 TTL 锁住这批座位。"""
        raise NotImplementedError

    def confirm(self, hold: SeatHold, pay: PaymentGateway) -> Booking:
        """付款成交：延长持有期 → 锁外调支付 → 锁内翻成 BOOKED → 落订单。"""
        raise NotImplementedError

    def release(self, hold: SeatHold) -> int:
        """用户主动放弃选座，立刻把座位还回去。"""
        raise NotImplementedError

    def release_expired_holds(self) -> int:
        """跨所有场次清扫一次过期收据，返回清掉的座位数。"""
        raise NotImplementedError

    def booking(self, booking_id: str) -> Booking:
        """按订单号取订单。"""
        raise NotImplementedError

    def cancel(self, booking_id: str) -> Booking:
        """退票：算退款、把座位退回场次、把订单置为已取消。"""
        raise NotImplementedError
