"""电影订票（BookMyShow）——选座、锁座、超时释放与并发下单的参考实现。

核心思路：座位分两层——`Seat` 是影厅里那把**物理**椅子，不可变、被同一影厅的所有场次共用；
"这把椅子在这一场里被谁占着"是**每场独有**的库存状态，因此由 `Show` 自己持有一张
`座位号 → _Slot` 的表，一把 `Show` 私有的锁保护它，两个不同场次天然不互相阻塞。锁座
（`SeatHold`）是一张有过期时间的收据：过期判断永远按注入的时钟**惰性**算，所以哪怕清扫线程
没跑，可用座位数也不会错；`release_expired` 只是把惰性结论落成实状态。支付是慢 IO，绝不能在
持有座位锁时调用——`confirm` 先在锁内把持有期延长到支付窗口，出锁后付款，再入锁把 HELD 翻成
BOOKED。定价与退票规则是注入的普通函数，加一档新价格或新退票政策都碰不到上面的锁座机器。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import Enum, IntEnum


# --------------------------------------------------------------------------
# 失败路径：一个小的异常家族，调用方可以只 catch 基类，也可以分别处理。


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
    """目录里没有这个场次（未上架，或已经被 `purge_shows_ended_before` 清掉）。"""

class BookingNotFoundError(BookingError):
    """订单号不存在。"""

class CancellationNotAllowedError(BookingError):
    """这张订单现在不允许取消：已经取消过，或者场次已经开演。"""


# --------------------------------------------------------------------------
# 物理层：座位、影厅、影院、电影。全部不可变——它们描述的是"这座楼里有什么"，
# 一天之内不会变，和"今晚这一场卖掉了几个座"是两件事。


class SeatType(IntEnum):
    """座位档次，数值越大越贵；按档定价靠这把标尺，不靠一串 `if`。"""

    NORMAL = 1
    PREMIUM = 2
    RECLINER = 3


@dataclass(frozen=True, slots=True)
class Seat:
    """影厅里的一把物理椅子：排号、座号、档次。不带任何"卖没卖掉"的状态——
    同一把椅子当天每一场都会出现，状态放这里会让 19:00 那场污染 21:30 那场。
    """

    row: str
    number: int
    type: SeatType = SeatType.NORMAL

    @property
    def label(self) -> str:
        """座位在影厅内的唯一标识，比如 `"C7"`。"""
        return f"{self.row}{self.number}"


@dataclass(frozen=True, slots=True)
class Screen:
    """一个影厅：一串固定的座位，被这个厅的所有场次共用。"""

    id: str
    seats: tuple[Seat, ...]

    @classmethod
    def grid(cls, screen_id: str, rows: Sequence[str], seats_per_row: int,
             types: Mapping[str, SeatType] | None = None) -> "Screen":
        """按"几排乘几座"快速造一个影厅；`types` 给个别排指定档次，其余是普通座。"""
        types = types or {}
        seats = tuple(Seat(row=row, number=n, type=types.get(row, SeatType.NORMAL))
                      for row in rows for n in range(1, seats_per_row + 1))
        return cls(id=screen_id, seats=seats)


@dataclass(frozen=True, slots=True)
class Cinema:
    """一家影院：属于某个城市，有若干影厅。城市只是一个字符串，没有单开 `City` 类——
    它除了"有个名字、下面挂着几家影院"没有行为，建成类只会多一层双向引用要维护。
    """

    id: str
    name: str
    city: str
    screens: tuple[Screen, ...] = ()


@dataclass(frozen=True, slots=True)
class Movie:
    """一部电影：时长决定散场时间，散场时间决定这场什么时候能从目录里清掉。"""

    id: str
    title: str
    duration: timedelta


# --------------------------------------------------------------------------
# 每场独有的座位状态。


class SeatStatus(Enum):
    """一个座位在**某一场**里的三种状态，状态机只有这三个点和四条边。"""

    AVAILABLE = "available"
    HELD = "held"
    BOOKED = "booked"


@dataclass(frozen=True, slots=True)
class _Slot:
    """`Show` 内部的一格座位状态。不可变，改状态靠 `replace` 整格换掉，因此没有"改了
    一半"的中间态。`hold_id` / `booking_id` 记的是"是谁占着"，过期时间只有 HELD 才有。
    """

    status: SeatStatus
    hold_id: str | None = None
    user_id: str | None = None
    booking_id: str | None = None
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class SeatHold:
    """一张锁座收据：哪一场、哪几个座、谁锁的、什么时候作废。这是交给调用方的**副本**，
    真相永远在 `Show` 的那张表里；它不可变，跨线程传递是安全的。
    """

    id: str
    show_id: str
    seat_labels: tuple[str, ...]
    user_id: str
    expires_at: datetime


class BookingStatus(Enum):
    """订单只有两个状态：付过钱的和退掉的。这里**没有** PENDING——"已选座、未付款"
    已经由 `SeatHold` 表达，再建一个 PENDING 就是同一件事的第二份表示，迟早对不上。
    """

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class Booking:
    """一张成交的订单，金额是整数的"分"。它是业务档案，不随场次结束而删除；
    能变的只有 `status` 和 `refunded`。
    """

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


# --------------------------------------------------------------------------
# 定价与退票：两类"会变的规则"，都是普通函数。它们只读 `Seat` / `Show` / `Booking`，
# 没有跨调用要记的状态，所以不需要抽象基类，也不需要各配一个实现类。


def by_seat_type(prices: Mapping[SeatType, int]) -> PricingStrategy:
    """按座位档次定价，单位是分。最常见的一档。"""

    def price(seat: Seat, show: "Show") -> int:
        return prices[seat.type]

    return price


def row_surcharge(base: PricingStrategy, extra_by_row: Mapping[str, int]) -> PricingStrategy:
    """在任意一种定价之上，给指定的排加价——策略是函数，所以"叠一层"就是包一个函数。"""

    def price(seat: Seat, show: "Show") -> int:
        return base(seat, show) + extra_by_row.get(seat.row, 0)

    return price


def weekend_multiplier(base: PricingStrategy, numerator: int, denominator: int) -> PricingStrategy:
    """周末按整数分数加价（比如 12/10 就是上浮两成），整数运算避免浮点分币误差。"""

    def price(seat: Seat, show: "Show") -> int:
        if show.starts_at.weekday() < 5:
            return base(seat, show)
        return base(seat, show) * numerator // denominator

    return price


def no_refund(booking: Booking, show: "Show", now: datetime) -> int:
    """一律不退款——影院最省事的政策，也是退票规则的下界。"""
    return 0


def tiered_refund(tiers: Sequence[tuple[timedelta, int]]) -> CancellationPolicy:
    """按"离开演还有多久"分档退款：`tiers` 是 (提前量, 退款百分比)，按提前量从大到小给。"""

    ordered = tuple(sorted(tiers, key=lambda t: t[0], reverse=True))

    def refund(booking: Booking, show: "Show", now: datetime) -> int:
        ahead = show.starts_at - now
        for threshold, percent in ordered:
            if ahead >= threshold:
                return booking.amount * percent // 100
        return 0

    return refund


# --------------------------------------------------------------------------
# Show：一场放映。本设计的核心——"这一场的座位卖到哪一步了"这份状态只此一份。


class Show:
    """一场放映：绑定一部电影、一个影厅、一个开演时间，持有这一场的座位库存。

    不变量：每个座位号任一时刻只有一个状态，HELD 必定带 `hold_id` 和过期时间，
    而"检查可选"和"写入占用"永远在同一把锁里，所以同一个座位不可能被两个人同时选中。
    锁放在场次上而不是全局一把：同一场的观众才真正抢同一批座位，一场一锁就是刚好的
    粒度；又因为一笔下单只涉及一个场次，永远不用同时持两把锁，也就没有锁顺序死锁。
    """

    def __init__(self, show_id: str, movie: Movie, screen: Screen, cinema: Cinema,
                 starts_at: datetime, clock: Clock) -> None:
        self.id = show_id
        self.movie = movie
        self.screen = screen
        self.cinema = cinema
        self.starts_at = starts_at
        self._clock = clock
        self._seats: dict[str, Seat] = {seat.label: seat for seat in screen.seats}
        self._slots: dict[str, _Slot] = {label: _Slot(SeatStatus.AVAILABLE) for label in self._seats}
        self._lock = threading.Lock()
        self._hold_ids = (f"{show_id}-H{n}" for n in itertools.count(1))

    @property
    def ends_at(self) -> datetime:
        """散场时间，由电影时长算出；目录清理用它判断这场是不是已经结束。"""
        return self.starts_at + self.movie.duration

    @property
    def seat_count(self) -> int:
        """这一场总共有多少座——影厅固定，所以这个数不随售卖变化。"""
        return len(self._seats)

    def seat(self, label: str) -> Seat:
        """按座位号取那把物理椅子；不存在就抛 `UnknownSeatError`。"""
        try:
            return self._seats[label]
        except KeyError:
            raise UnknownSeatError(f"screen {self.screen.id} has no seat {label!r}") from None

    # ---- 读：一律返回快照或计数，从不把内部的表交出去 --------------------

    @staticmethod
    def _effective(slot: _Slot, now: datetime) -> SeatStatus:
        """惰性过期：一格 HELD 只要过了时间，对外就已经是 AVAILABLE。把过期算在每次
        读写的那一刻，正确性就不依赖清扫任务跑没跑；`release_expired` 只是把结论落实。
        """
        if slot.status is SeatStatus.HELD and slot.expires_at is not None and slot.expires_at <= now:
            return SeatStatus.AVAILABLE
        return slot.status

    def seat_status(self, label: str) -> SeatStatus:
        """某个座位此刻对外的状态（已经考虑过期）。"""
        self.seat(label)
        now = self._clock()
        with self._lock:
            return self._effective(self._slots[label], now)

    def available_seats(self) -> tuple[Seat, ...]:
        """当前可选座位的一份不可变快照，按影厅里的固定顺序给出。"""
        now = self._clock()
        with self._lock:
            labels = [label for label, slot in self._slots.items()
                      if self._effective(slot, now) is SeatStatus.AVAILABLE]
        return tuple(self._seats[label] for label in labels)

    def count_by_status(self) -> Mapping[SeatStatus, int]:
        """三种状态各有多少座的只读计数快照——展示层要的是数字，不是座位表本身。"""
        now = self._clock()
        counts = dict.fromkeys(SeatStatus, 0)
        with self._lock:
            for slot in self._slots.values():
                counts[self._effective(slot, now)] += 1
        return counts

    # ---- 写：锁座、延期、成交、释放 --------------------------------------

    def _live_labels(self, hold: SeatHold, now: datetime) -> tuple[str, ...]:
        """收据还活着时返回它占着的座位号；有一个对不上就说明失效。调用方须已持有锁。"""
        live = tuple(label for label in hold.seat_labels
                     if (slot := self._slots.get(label)) is not None
                     and slot.hold_id == hold.id
                     and self._effective(slot, now) is SeatStatus.HELD)
        if len(live) != len(hold.seat_labels):
            raise HoldExpiredError(f"hold {hold.id} no longer holds {hold.seat_labels}")
        return live

    def hold(self, seat_labels: Iterable[str], user_id: str, ttl: timedelta) -> SeatHold:
        """锁住一批座位 `ttl` 这么久，全成功或全失败，返回一张收据。

        "检查都可选"和"标成 HELD"必须在同一把锁里做完，拆成两段两个线程就会都写进去；
        部分成功同样不可接受——选三个座只锁住两个，用户拿到的是一笔没法用的订单。
        """
        labels = tuple(dict.fromkeys(seat_labels))  # 去重且保序
        if not labels:
            raise UnknownSeatError("a hold must name at least one seat")
        now = self._clock()
        with self._lock:
            unknown = [label for label in labels if label not in self._slots]
            if unknown:
                raise UnknownSeatError(f"screen {self.screen.id} has no seat(s) {unknown}")
            taken = [label for label in labels
                     if self._effective(self._slots[label], now) is not SeatStatus.AVAILABLE]
            if taken:
                raise SeatNotAvailableError(f"seat(s) {taken} are not available on show {self.id}")
            receipt = SeatHold(id=next(self._hold_ids), show_id=self.id, seat_labels=labels,
                               user_id=user_id, expires_at=now + ttl)
            for label in labels:
                self._slots[label] = _Slot(SeatStatus.HELD, hold_id=receipt.id,
                                           user_id=user_id, expires_at=receipt.expires_at)
        return receipt

    def extend_hold(self, hold: SeatHold, window: timedelta) -> SeatHold:
        """把有效期重置为"从现在起 `window`"，返回刷新后的收据。`confirm` 在调支付
        网关**之前**用它，延长发生在锁内，所以和"别人抢座"之间没有缝隙。
        """
        now = self._clock()
        expires_at = now + window
        with self._lock:
            for label in self._live_labels(hold, now):
                self._slots[label] = replace(self._slots[label], expires_at=expires_at)
        return replace(hold, expires_at=expires_at)

    def commit(self, hold: SeatHold, booking_id: str) -> None:
        """把收据上的座位从 HELD 翻成 BOOKED；收据已失效则抛 `HoldExpiredError`。"""
        now = self._clock()
        with self._lock:
            for label in self._live_labels(hold, now):
                self._slots[label] = _Slot(SeatStatus.BOOKED, booking_id=booking_id)

    def release(self, hold: SeatHold) -> int:
        """主动放弃一张收据（退出选座、支付失败），返回退回的座位数。故意做成幂等且
        不抛异常：它总跑在失败路径上，再抛异常只会盖掉真正的错误原因。
        """
        now = self._clock()
        freed = 0
        with self._lock:
            for label in hold.seat_labels:
                slot = self._slots.get(label)
                if slot is not None and slot.hold_id == hold.id and slot.status is SeatStatus.HELD:
                    self._slots[label] = _Slot(SeatStatus.AVAILABLE)
                    freed += 1
        return freed

    def release_expired(self) -> int:
        """把所有过期的 HELD 真正写回 AVAILABLE，返回清掉的座位数。座位表长度恒等于
        影厅座位数；这里清的是格子里残留的 `hold_id` 和过期时间。
        """
        now = self._clock()
        freed = 0
        with self._lock:
            for label, slot in self._slots.items():
                if slot.status is SeatStatus.HELD and self._effective(slot, now) is SeatStatus.AVAILABLE:
                    self._slots[label] = _Slot(SeatStatus.AVAILABLE)
                    freed += 1
        return freed

    def release_booking(self, booking_id: str) -> int:
        """退票：把这张订单占的 BOOKED 座位退回 AVAILABLE，返回退回的座位数。"""
        freed = 0
        with self._lock:
            for label, slot in self._slots.items():
                if slot.status is SeatStatus.BOOKED and slot.booking_id == booking_id:
                    self._slots[label] = _Slot(SeatStatus.AVAILABLE)
                    freed += 1
        return freed


# --------------------------------------------------------------------------
# BookingService：面向用户的门面。它管目录、算钱、调支付、记订单；
# 座位归谁这件事它一个字节都不存，全部委托给对应的 `Show`。


class BookingService:
    """订票服务：按城市/电影找场次，锁座、付款成交、退票，以及清扫过期收据。

    锁纪律：它自己的锁只保护目录和订单表，**绝不**在持有它时去拿某个 `Show` 的锁——
    两把锁永远"先放后拿"，不存在嵌套，也就不存在锁顺序死锁。
    """

    def __init__(self, clock: Clock, pricing: PricingStrategy,
                 cancellation: CancellationPolicy = no_refund,
                 hold_ttl: timedelta = timedelta(minutes=10),
                 payment_window: timedelta = timedelta(minutes=2)) -> None:
        self._clock = clock
        self._pricing = pricing
        self._cancellation = cancellation
        self._hold_ttl = hold_ttl
        self._payment_window = payment_window
        self._shows: dict[str, Show] = {}
        self._bookings: dict[str, Booking] = {}
        self._lock = threading.Lock()
        self._booking_ids = (f"B{n}" for n in itertools.count(1))

    # ---- 目录 ------------------------------------------------------------

    def schedule(self, show: Show) -> None:
        """把一场放映上架。"""
        with self._lock:
            self._shows[show.id] = show

    def show(self, show_id: str) -> Show:
        """按 id 取场次；不在目录里就抛 `ShowNotFoundError`。"""
        with self._lock:
            show = self._shows.get(show_id)
        if show is None:
            raise ShowNotFoundError(f"unknown show {show_id!r}")
        return show

    def shows_in_city(self, city: str, movie_id: str | None = None) -> tuple[Show, ...]:
        """某城市（可再限定某部电影）在映场次的快照，按开演时间排序。

        这里是全表扫描，没有另建"城市 → 场次"索引：索引是第二份要保持一致的状态，而
        一家院线同时在映也就几千场。真到了需要索引的量级，再加也只改这一个方法。
        """
        with self._lock:
            shows = list(self._shows.values())
        picked = [s for s in shows if s.cinema.city == city and (movie_id is None or s.movie.id == movie_id)]
        return tuple(sorted(picked, key=lambda s: (s.starts_at, s.id)))

    def purge_shows_ended_before(self, cutoff: datetime) -> int:
        """把已经散场的场次从目录里摘掉，返回摘掉的场次数。

        这是目录唯一会缩小的地方——没有它 `_shows` 会随排片无限增长。订单不跟着删，
        但它记的是 `show_id` 而不是 `Show` 引用，所以摘掉之后场次对象真的能被回收。
        """
        with self._lock:
            gone = [show_id for show_id, show in self._shows.items() if show.ends_at <= cutoff]
            for show_id in gone:
                del self._shows[show_id]
        return len(gone)

    # ---- 下单 ------------------------------------------------------------

    def quote(self, show_id: str, seat_labels: Iterable[str]) -> int:
        """报价：这批座位一共多少分。定价规则来自注入的策略。"""
        show = self.show(show_id)
        return sum(self._pricing(show.seat(label), show) for label in seat_labels)

    def hold(self, show_id: str, seat_labels: Iterable[str], user_id: str) -> SeatHold:
        """选座：按服务配置的 TTL 锁住这批座位。"""
        return self.show(show_id).hold(seat_labels, user_id, self._hold_ttl)

    def confirm(self, hold: SeatHold, pay: PaymentGateway) -> Booking:
        """付款成交：延长持有期 → 锁外调支付 → 锁内把座位翻成 BOOKED → 落订单。

        支付必须在座位锁之外调：握着锁调外部 IO，网关一慢就是全场卡死。代价是付完款
        到落单之间有个窗口，所以进窗口前先把持有期延到 `payment_window`；万一还是超了，
        这里宁可抛错也不会覆盖别人已经买到的座位，并在消息里点明这笔钱需要退。
        """
        show = self.show(hold.show_id)
        amount = self.quote(hold.show_id, hold.seat_labels)
        hold = show.extend_hold(hold, self._payment_window)
        try:
            approved = pay(hold.user_id, amount)
        except Exception:
            show.release(hold)
            raise
        if not approved:
            show.release(hold)
            raise PaymentFailedError(f"payment declined for hold {hold.id}")
        with self._lock:
            booking_id = next(self._booking_ids)
        try:
            show.commit(hold, booking_id)
        except HoldExpiredError as exc:
            raise HoldExpiredError(
                f"payment for hold {hold.id} succeeded but the seats were already released; refund {amount}"
            ) from exc
        booking = Booking(id=booking_id, show_id=show.id, user_id=hold.user_id,
                          seat_labels=hold.seat_labels, amount=amount, created_at=self._clock())
        with self._lock:
            self._bookings[booking.id] = booking
        return booking

    def release(self, hold: SeatHold) -> int:
        """用户主动放弃选座，立刻把座位还回去，不用等 TTL。"""
        return self.show(hold.show_id).release(hold)

    def release_expired_holds(self) -> int:
        """跨所有场次清扫一次过期收据，返回清掉的座位数。先在服务锁内拿一份场次快照，
        出锁后再逐场去拿各自的锁，不形成"服务锁 → 场次锁"的嵌套。
        """
        with self._lock:
            shows = list(self._shows.values())
        return sum(show.release_expired() for show in shows)

    # ---- 订单 ------------------------------------------------------------

    def booking(self, booking_id: str) -> Booking:
        """按订单号取订单。"""
        with self._lock:
            booking = self._bookings.get(booking_id)
        if booking is None:
            raise BookingNotFoundError(f"unknown booking {booking_id!r}")
        return booking

    def cancel(self, booking_id: str) -> Booking:
        """退票：算退款、把座位退回场次、把订单置为已取消，返回更新后的订单。

        状态位在锁内先翻，这一步就是"认领"订单：两个线程同时点退票，只有一个能把
        CONFIRMED 翻成 CANCELLED，不会退两次款。开演后不许退票，也让清理场次永远安全。
        """
        now = self._clock()
        with self._lock:
            booking = self._bookings.get(booking_id)
            if booking is None:
                raise BookingNotFoundError(f"unknown booking {booking_id!r}")
            show = self._shows.get(booking.show_id)
            if show is None:
                raise ShowNotFoundError(f"show {booking.show_id!r} is no longer scheduled")
            if booking.status is BookingStatus.CANCELLED:
                raise CancellationNotAllowedError(f"booking {booking_id} is already cancelled")
            if now >= show.starts_at:
                raise CancellationNotAllowedError(f"show {show.id} has already started")
            booking.status = BookingStatus.CANCELLED
        booking.refunded = self._cancellation(booking, show, now)
        show.release_booking(booking.id)
        return booking


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 5, 15, 18, 0, tzinfo=UTC)
    screen = Screen.grid("S1", rows="ABC", seats_per_row=6, types={"C": SeatType.PREMIUM})
    cinema = Cinema(id="C1", name="Grand", city="Shanghai", screens=(screen,))
    movie = Movie(id="M1", title="Dune", duration=timedelta(minutes=155))
    show = Show("SH1", movie, screen, cinema, starts_at=now + timedelta(hours=2), clock=lambda: now)

    service = BookingService(
        clock=lambda: now,
        pricing=row_surcharge(by_seat_type({SeatType.NORMAL: 4500, SeatType.PREMIUM: 6800,
                                            SeatType.RECLINER: 9900}), {"A": 500}),
        cancellation=tiered_refund([(timedelta(hours=4), 100), (timedelta(hours=1), 50)]),
        hold_ttl=timedelta(minutes=10),
    )
    service.schedule(show)

    def free() -> int:
        """演示用：当前还剩几个空座。"""
        return show.count_by_status()[SeatStatus.AVAILABLE]

    receipt = service.hold("SH1", ["A1", "A2"], user_id="u1")
    print(f"held {receipt.seat_labels} until {receipt.expires_at:%H:%M}, free now: {free()}")
    booking = service.confirm(receipt, pay=lambda user, amount: True)
    print(f"booking {booking.id}: {booking.amount} fen, free {free()}")
    service.hold("SH1", ["B1"], user_id="u2")
    now = now + timedelta(minutes=11)  # 时钟往前拨：u2 的锁座超时了
    print(f"swept {service.release_expired_holds()} expired seat(s), free {free()}")
    print(f"refunded {service.cancel(booking.id).refunded} fen, free {free()}")
