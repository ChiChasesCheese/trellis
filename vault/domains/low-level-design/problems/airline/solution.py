"""航班管理（Airline Management）——航班/航班实例/航段三层模型、跨航段原子订座与值机的参考实现。

核心思路：`Flight` 是排班表上那条**每天重复**的航线（航班号、起降机场、起飞钟点、机型），
`FlightInstance` 才是"某一天的那一班"，库存、座位图和锁都只长在它身上；旅客买到的是
`Segment`（他在某一班上占的一个舱位），若干段拼成 `Itinerary`，**整条行程要么全订上要么一段都不订**——
跨航段的原子性靠 `FlightInstance.reserve_across` 按 key 排序后一次性持有多把锁实现，固定顺序即无死锁。
中转是否成立由注入的 `MinimumConnectionTime`（最短衔接时间）裁决，它属于机场而不属于航班；
超售是按舱位注入的政策，它的代价在值机拿不到座位、在登机口被拒载时才兑现，改签则是"先占新段再放旧段"。
"""

from __future__ import annotations

import itertools
import threading
from collections.abc import Callable, Mapping, Sequence
from contextlib import ExitStack
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum, IntEnum


# --------------------------------------------------------------------------
# 失败路径：一个小的异常家族。调用方可以只 catch 基类，也可以分别处理。

class AirlineError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownFlightError(AirlineError):
    """目录里没有这个航班实例（航班号写错，或者这一班已经被清理掉了）。"""

class NoSeatsAvailableError(AirlineError):
    """行程里至少有一段的这个舱位已经售罄（含超售额度）——整条行程都不成立。"""

class InvalidItineraryError(AirlineError):
    """行程本身不合法：空行程、前后段机场接不上，或者中转时间短于最短衔接时间。"""

class SeatUnavailableError(AirlineError):
    """指定的座位号不存在、不属于这个舱位，或者已经被别人选走了。"""

class BookingNotFoundError(AirlineError):
    """订单号不存在。"""

class InvalidTransitionError(AirlineError):
    """订单当前状态不允许这次状态转移。"""

class HoldExpiredError(AirlineError):
    """占座已经超时释放，不能再拿它出票。"""


# --------------------------------------------------------------------------
# 静态的物理层：舱位、座位、机型、航班（排班表上的一行）。全部不可变。

class CabinClass(IntEnum):
    """舱位等级。数值越大越贵：超售额度、票价、拒载顺序都按这把标尺来，不靠一串 `if`。"""

    ECONOMY = 1
    PREMIUM = 2
    BUSINESS = 3
    FIRST = 4


@dataclass(frozen=True, slots=True)
class Seat:
    """机舱里的一把物理座椅：舱位、排号、座位字母。不带"这一班被谁占了"的状态——
    同一架飞机今天飞上海、明天飞成都，占用属于某一天的那一班，不属于这把椅子。
    """

    cabin: CabinClass
    row: int
    letter: str

    @property
    def label(self) -> str:
        """座位号，比如 `"12C"`。"""
        return f"{self.row}{self.letter}"


@dataclass(frozen=True, slots=True)
class Aircraft:
    """一架飞机（更准确地说是一种客舱布局）：座位表固定，被排班表上所有用它的航班共用。"""

    id: str
    model: str
    seats: tuple[Seat, ...]

    @classmethod
    def layout(cls, aircraft_id: str, model: str,
               cabins: Mapping[CabinClass, tuple[int, str]]) -> "Aircraft":
        """按"每个舱位几排、每排哪些字母"生成座位表；排号从高舱位往低舱位连续编下去。"""
        seats: list[Seat] = []
        row = 1
        for cabin in sorted(cabins, reverse=True):
            rows, letters = cabins[cabin]
            for _ in range(rows):
                seats.extend(Seat(cabin, row, letter) for letter in letters)
                row += 1
        return cls(id=aircraft_id, model=model, seats=tuple(seats))

    def seats_in(self, cabin: CabinClass) -> tuple[Seat, ...]:
        """某个舱位的座位快照，按排号顺序。"""
        return tuple(seat for seat in self.seats if seat.cabin is cabin)


@dataclass(frozen=True, slots=True)
class Flight:
    """排班表上的一行：航班号、起降机场、起飞钟点、飞行时长、机型、实际承运人。

    它**没有日期**——"MU5100 每天 08:00 从 SHA 飞 PEK"是一条排班规则，不是一件可以被卖掉的
    东西。`marketed_as` 是代码共享（codeshare）用的市场航班号：同一班飞机在别家航司的目录里
    叫另一个号，但它仍然只有一份库存，所以代码共享在本设计里只是目录上的一个别名。
    """

    number: str
    origin: str
    destination: str
    departs_at: time
    duration: timedelta
    aircraft: Aircraft
    operated_by: str
    marketed_as: tuple[str, ...] = ()


# --------------------------------------------------------------------------
# 可注入的政策：超售、票价、退票。都是无状态的普通函数，不需要抽象基类。

OverbookingPolicy = Callable[[CabinClass, "FlightInstance"], int]
FarePolicy = Callable[["Itinerary"], int]
RefundPolicy = Callable[["Booking", datetime], int]
Clock = Callable[[], datetime]


def no_overbooking(cabin: CabinClass, instance: "FlightInstance") -> int:
    """不超售：可售数就是实际座位数。"""
    return 0


def percent_overbooking(by_cabin: Mapping[CabinClass, int]) -> OverbookingPolicy:
    """按舱位给一个超售百分比（经济舱常见 5%–15%，头等舱通常是 0）。"""

    def extra(cabin: CabinClass, instance: "FlightInstance") -> int:
        return instance.capacity(cabin) * by_cabin.get(cabin, 0) // 100

    return extra


def cabin_fare(prices: Mapping[CabinClass, int]) -> FarePolicy:
    """按舱位逐段累加票价，单位是"分"；整数运算避免浮点分币误差。"""

    def fare(itinerary: "Itinerary") -> int:
        return sum(prices[segment.cabin] for segment in itinerary.segments)

    return fare


def no_refund(booking: "Booking", now: datetime) -> int:
    """一律不退——最便宜的特价票政策，也是退票规则的下界。"""
    return 0


def tiered_refund(tiers: Sequence[tuple[timedelta, int]]) -> RefundPolicy:
    """按"离首段起飞还有多久"分档退款：`tiers` 是 (提前量, 退款百分比)，提前量从大到小生效。"""

    ordered = tuple(sorted(tiers, key=lambda tier: tier[0], reverse=True))

    def refund(booking: "Booking", now: datetime) -> int:
        ahead = booking.itinerary.departure - now
        for threshold, percent in ordered:
            if ahead >= threshold:
                return booking.fare * percent // 100
        return 0

    return refund


# --------------------------------------------------------------------------
# FlightInstance：某一天的那一班。本设计里唯一持有库存状态的对象。

class FlightInstance:
    """把一条排班规则钉到某个日期上：这一班的舱位库存、座位图和一把私有锁都在这里。

    两份状态、一个不变量：`_sold` 是 `订单号 → 舱位` 的旅客名单（所以退订天然幂等，也天然
    能回答"这一班这个舱有谁"），`_seats` 是 `座位号 → 订单号` 的座位图。不变量是
    **任一舱位的名单人数 ≤ 座位数 + 超售额度**，检查与写入永远在同一把锁里完成。
    锁放在"实例"而不是"航班"上：同一天同一班的旅客才真正抢同一批座位。
    """

    def __init__(self, flight: Flight, service_date: date,
                 overbooking: OverbookingPolicy = no_overbooking) -> None:
        self.flight = flight
        self.service_date = service_date
        self._overbooking = overbooking
        self._sold: dict[str, CabinClass] = {}
        self._seats: dict[str, str] = {}
        # 可重入锁：一条行程里同一班出现两次（极少见，但合法）时不会自锁。
        self._lock = threading.RLock()

    @property
    def key(self) -> str:
        """这一班的唯一标识：航班号 + 执飞日期，比如 `"MU5100@2026-07-01"`。"""
        return f"{self.flight.number}@{self.service_date.isoformat()}"

    @property
    def departure(self) -> datetime:
        """实际起飞时刻（本设计统一用 UTC，时区换算留给展示层）。"""
        return datetime.combine(self.service_date, self.flight.departs_at)

    @property
    def arrival(self) -> datetime:
        """落地时刻，由排班表上的飞行时长算出。"""
        return self.departure + self.flight.duration

    def capacity(self, cabin: CabinClass) -> int:
        """这个舱位真实有几把椅子。"""
        return len(self.flight.aircraft.seats_in(cabin))

    def authorized(self, cabin: CabinClass) -> int:
        """这个舱位允许卖出几张票 = 座位数 + 超售额度。"""
        return self.capacity(cabin) + self._overbooking(cabin, self)

    def _free(self, cabin: CabinClass) -> int:
        """还能卖几张。调用方须已持有锁。"""
        sold = sum(1 for booked in self._sold.values() if booked is cabin)
        return self.authorized(cabin) - sold

    def available(self, cabin: CabinClass) -> int:
        """这个舱位还能卖几张票。"""
        with self._lock:
            return self._free(cabin)

    def refs_in(self, cabin: CabinClass) -> tuple[str, ...]:
        """这个舱位的旅客订单号快照，按订单号排序，供登机结算使用。"""
        with self._lock:
            return tuple(sorted(ref for ref, booked in self._sold.items() if booked is cabin))

    @classmethod
    def reserve_across(cls, requests: Sequence[tuple["FlightInstance", CabinClass]],
                       ref: str) -> None:
        """跨若干航班实例一次性占位：全部占上，或者一个都不占。

        这是本题与单场次订票最大的不同：一条中转行程横跨两班飞机，两把锁必须**同时**握住，
        否则"第一段订上、第二段满员"会给旅客一张飞到中转站就断掉的机票。按 `key` 排序后
        依次进入临界区，全局固定的加锁顺序就是不死锁的全部理由。
        """
        ordered = sorted(requests, key=lambda request: request[0].key)
        with ExitStack() as stack:
            for instance, _ in ordered:
                stack.enter_context(instance._lock)
            short = [instance.key for instance, cabin in ordered
                     if instance._sold.get(ref) is not cabin and instance._free(cabin) <= 0]
            if short:
                raise NoSeatsAvailableError(f"no {ref} seat left on {short}")
            for instance, cabin in ordered:
                if instance._sold.get(ref) is not cabin:
                    instance._drop_seat(ref)  # 换舱意味着原来那个座位号作废
                instance._sold[ref] = cabin

    def release(self, ref: str) -> bool:
        """把一个订单从这一班上摘掉，连同它的座位。幂等：它总跑在失败路径和取消路径上。"""
        with self._lock:
            self._drop_seat(ref)
            return self._sold.pop(ref, None) is not None

    def _drop_seat(self, ref: str) -> None:
        """释放这个订单占的座位号。调用方须已持有锁。"""
        for label, holder in list(self._seats.items()):
            if holder == ref:
                del self._seats[label]

    def assign_seat(self, ref: str, preferred: str | None = None) -> str | None:
        """给旅客选座：指定座位号就按指定的来，没指定就挑本舱第一个空位。

        返回座位号；**本舱已经没有空位时返回 `None` 而不是抛异常**——超售卖出去的那张票
        本来就没有椅子，值机时它是"座位待定"，代价要留到登机口兑现。只有旅客点名的座位拿不到
        才算真失败。
        """
        with self._lock:
            cabin = self._sold.get(ref)
            if cabin is None:
                raise BookingNotFoundError(f"{ref} is not booked on {self.key}")
            free = [s.label for s in self.flight.aircraft.seats_in(cabin)
                    if self._seats.get(s.label, ref) == ref]
            if preferred is not None and preferred not in free:
                raise SeatUnavailableError(f"seat {preferred!r} is not free in {cabin.name}")
            chosen = preferred or (free[0] if free else None)
            if chosen is not None:
                self._drop_seat(ref)  # 重复值机时先收回旧座位，座位图里不会留下两把椅子
                self._seats[chosen] = ref
            return chosen

    def seat_of(self, ref: str) -> str | None:
        """这个订单在这一班上的座位号，没选到就是 `None`。"""
        with self._lock:
            return next((label for label, holder in self._seats.items() if holder == ref), None)

    def free_seats(self, cabin: CabinClass) -> tuple[str, ...]:
        """本舱还没被选走的座位号快照。"""
        with self._lock:
            return tuple(s.label for s in self.flight.aircraft.seats_in(cabin)
                         if s.label not in self._seats)


# --------------------------------------------------------------------------
# 旅客侧：航段、行程、最短衔接时间。

@dataclass(frozen=True, slots=True)
class Segment:
    """旅客行程里的一段：他在**某一班**上占的一个舱位。座位号不在这里——座位属于那一班的
    座位图，一个旅客改签换班之后座位号必须跟着作废，放在这里就会留下一份过期副本。
    """

    instance: FlightInstance
    cabin: CabinClass

    @property
    def departure(self) -> datetime:
        """这一段的起飞时刻。"""
        return self.instance.departure

    @property
    def arrival(self) -> datetime:
        """这一段的落地时刻。"""
        return self.instance.arrival


@dataclass(frozen=True, slots=True)
class Itinerary:
    """一条行程：按时间排好的若干航段，**订座的原子单位**。

    它比裸 `tuple[Segment, ...]` 多出来的正是"整条行程才有意义"的那些事实：全程起降机场、
    全程时刻、中转几次。它**不**负责判断中转时间够不够——那条规则属于机场，见
    `MinimumConnectionTime`。
    """

    segments: tuple[Segment, ...]

    @property
    def origin(self) -> str:
        """全程出发机场。"""
        return self.segments[0].instance.flight.origin

    @property
    def destination(self) -> str:
        """全程到达机场。"""
        return self.segments[-1].instance.flight.destination

    @property
    def departure(self) -> datetime:
        """首段起飞时刻。"""
        return self.segments[0].departure

    @property
    def arrival(self) -> datetime:
        """末段落地时刻。"""
        return self.segments[-1].arrival

    @property
    def stops(self) -> int:
        """中转次数。"""
        return len(self.segments) - 1


@dataclass(frozen=True, slots=True)
class MinimumConnectionTime:
    """最短衔接时间（MCT，Minimum Connection Time）表：按机场给基准，换承运人再加一档。

    这条规则**不能**挂在 `Flight` 上：它描述的是"在这个机场，下了这班再赶下一班要走多久"，
    取决于航站楼距离、是否重新过安检、行李转运效率——同一班飞机落在浦东和落在虹桥，需要的
    衔接时间完全不同。挂在航班上就得给每条航线抄一份，改一次航站楼要改几千行。
    """

    default: timedelta
    by_airport: Mapping[str, timedelta] = field(default_factory=dict)
    carrier_change: timedelta = timedelta(0)

    def required(self, arriving: Segment, departing: Segment) -> timedelta:
        """这次中转至少需要多少时间。"""
        airport = arriving.instance.flight.destination
        base = self.by_airport.get(airport, self.default)
        if arriving.instance.flight.operated_by != departing.instance.flight.operated_by:
            base += self.carrier_change
        return base

    def connects(self, arriving: Segment, departing: Segment) -> bool:
        """前一段能不能接上后一段：机场要对得上，留出的时间要够。"""
        if arriving.instance.flight.destination != departing.instance.flight.origin:
            return False
        return departing.departure - arriving.arrival >= self.required(arriving, departing)


# --------------------------------------------------------------------------
# 订单与生命周期。

class BookingStatus(Enum):
    """订单生命周期。这里没有"已支付"——出票（TICKETED）就是钱已经落袋的那一刻。"""

    HELD = "held"
    TICKETED = "ticketed"
    CHECKED_IN = "checked_in"
    BOARDED = "boarded"
    CANCELLED = "cancelled"


ALLOWED_TRANSITIONS: Mapping[BookingStatus, frozenset[BookingStatus]] = {
    BookingStatus.HELD: frozenset({BookingStatus.TICKETED, BookingStatus.CANCELLED}),
    BookingStatus.TICKETED: frozenset({BookingStatus.CHECKED_IN, BookingStatus.CANCELLED}),
    # CHECKED_IN → TICKETED 是登机口拒载（denied boarding）：值机撤销，票还在，等改签。
    BookingStatus.CHECKED_IN: frozenset({BookingStatus.BOARDED, BookingStatus.TICKETED,
                                         BookingStatus.CANCELLED}),
    BookingStatus.BOARDED: frozenset(),
    BookingStatus.CANCELLED: frozenset(),
}


@dataclass(slots=True)
class Booking:
    """一张订单：行程、旅客、票价（整数"分"）、状态。生命周期只能沿转移表走。"""

    id: str
    itinerary: Itinerary
    passenger: str
    fare: int
    created_at: datetime
    held_until: datetime
    status: BookingStatus = BookingStatus.HELD
    checked_in_at: datetime | None = None
    # 已经登机的航段 key。多段行程要登机两次，只有一个 `status` 字段记不住"登了第一段"，
    # 再次结算同一班时旅客会被重复计入人数——这里显式记下来，登机结算就天然只算一次。
    boarded: tuple[str, ...] = ()
    refunded: int = 0

    def transition_to(self, target: BookingStatus) -> None:
        """按转移表改状态；非法迁移抛 `InvalidTransitionError`。"""
        if target not in ALLOWED_TRANSITIONS[self.status]:
            raise InvalidTransitionError(f"booking {self.id}: {self.status.name} -> {target.name}")
        self.status = target


# --------------------------------------------------------------------------
# AirlineService：门面。管目录、算钱、走生命周期；库存一个字节都不存。

class AirlineService:
    """订座服务：查行程、占座、出票、值机、登机、取消、改签，外加过期占座清扫与历史清理。

    锁纪律：它自己的锁只保护目录和订单表，**绝不**在持有它时去拿某个 `FlightInstance` 的锁。
    库存那一侧的多锁顺序由 `FlightInstance.reserve_across` 统一按 key 排序，两层永不交叉。
    """

    def __init__(self, clock: Clock, connection: MinimumConnectionTime, fare: FarePolicy,
                 refund: RefundPolicy = no_refund,
                 hold_ttl: timedelta = timedelta(minutes=20),
                 check_in_opens: timedelta = timedelta(hours=24),
                 check_in_closes: timedelta = timedelta(minutes=45)) -> None:
        self._clock = clock
        self._connection = connection
        self._fare = fare
        self._refund = refund
        self._hold_ttl = hold_ttl
        self._check_in_opens = check_in_opens
        self._check_in_closes = check_in_closes
        self._instances: dict[str, FlightInstance] = {}
        self._by_origin: dict[tuple[str, date], list[FlightInstance]] = {}
        self._bookings: dict[str, Booking] = {}
        self._lock = threading.Lock()
        self._ids = (f"PNR{n:04d}" for n in itertools.count(1))

    # ---- 目录 ------------------------------------------------------------

    def schedule(self, instance: FlightInstance) -> None:
        """把某一天的某一班上架。代码共享的市场航班号在这里登记成别名，指向同一个对象——
        共享航班只有一份库存，所以它不该产生第二个 `FlightInstance`。
        """
        with self._lock:
            self._instances[instance.key] = instance
            for number in instance.flight.marketed_as:
                self._instances[f"{number}@{instance.service_date.isoformat()}"] = instance
            self._by_origin.setdefault((instance.flight.origin, instance.service_date),
                                       []).append(instance)

    def instance(self, key: str) -> FlightInstance:
        """按 `航班号@日期` 取一班；市场航班号也能取到同一班。"""
        with self._lock:
            found = self._instances.get(key)
        if found is None:
            raise UnknownFlightError(f"unknown flight instance {key!r}")
        return found

    @property
    def instance_count(self) -> int:
        """目录里还有几班（按对象去重，别名不重复计数）。清理历史时用它验证目录真的缩了。"""
        with self._lock:
            return len({id(instance) for instance in self._instances.values()})

    @property
    def booking_count(self) -> int:
        """订单表里还有几张单。"""
        with self._lock:
            return len(self._bookings)

    @property
    def route_index_size(self) -> int:
        """`(出发机场, 日期) → 航班` 这张二级索引里还有多少个非空桶。清理历史后它必须跟着缩。"""
        with self._lock:
            return len(self._by_origin)

    def _departing(self, airport: str, day: date) -> list[FlightInstance]:
        """某机场某天出发的航班快照。"""
        with self._lock:
            return list(self._by_origin.get((airport, day), ()))

    def search(self, origin: str, destination: str, day: date, cabin: CabinClass,
               max_stops: int = 1) -> tuple[Itinerary, ...]:
        """查这一天从 `origin` 到 `destination`、这个舱位还有票的行程，按落地时间排序。

        直飞先出，再枚举一次中转：中转段可以落在当天或次日（跨零点的红眼航班），
        能不能接上一律交给 `MinimumConnectionTime`。
        """
        found: list[Itinerary] = []
        for first in self._departing(origin, day):
            if first.available(cabin) <= 0:
                continue
            head, hub = Segment(first, cabin), first.flight.destination
            if hub == destination:
                found.append(Itinerary((head,)))
                continue
            landed = first.arrival.date()
            for onward_day in ((landed, landed + timedelta(days=1)) if max_stops >= 1 else ()):
                for second in self._departing(hub, onward_day):
                    tail = Segment(second, cabin)
                    if (second.flight.destination == destination
                            and second.available(cabin) > 0
                            and self._connection.connects(head, tail)):
                        found.append(Itinerary((head, tail)))
        return tuple(sorted(found, key=lambda plan: (plan.arrival, plan.departure)))

    def purge_flown_before(self, cutoff: datetime) -> int:
        """把已经落地的航班实例从目录里摘掉，返回摘掉的班数。

        这是目录唯一会缩小的地方——没有它，每天的排班会让 `_instances` 无限增长。三个容器要一起
        缩：订单表握着 `Itinerary` 引用，不归档全程已飞完的订单，航班对象根本回收不了（真实系统
        里"归档"是写进历史库，这里就是删）；`_by_origin` 里空掉的桶也要删，留着就是另一种泄漏。
        """
        with self._lock:
            gone = {key for key, instance in self._instances.items() if instance.arrival <= cutoff}
            removed = len({id(self._instances[key]) for key in gone})
            for key in gone:
                del self._instances[key]
            for index_key, instances in list(self._by_origin.items()):
                kept = [i for i in instances if i.arrival > cutoff]
                self._by_origin[index_key] = kept
                if not kept:  # 空桶要删掉，留着就是另一种泄漏
                    del self._by_origin[index_key]
            for booking_id, booking in list(self._bookings.items()):
                if booking.itinerary.arrival <= cutoff:
                    del self._bookings[booking_id]
        return removed

    # ---- 下单 ------------------------------------------------------------

    def _validate(self, itinerary: Itinerary) -> None:
        """行程合法性：非空、前后段接得上、中转时间够。不合法就不要去碰库存。"""
        if not itinerary.segments:
            raise InvalidItineraryError("an itinerary needs at least one segment")
        for arriving, departing in itertools.pairwise(itinerary.segments):
            if not self._connection.connects(arriving, departing):
                raise InvalidItineraryError(
                    f"{arriving.instance.key} does not connect to {departing.instance.key}")

    def hold(self, itinerary: Itinerary, passenger: str) -> Booking:
        """占座：整条行程一次性占上，拿到一张有过期时间的订单（PNR）。"""
        self._validate(itinerary)
        with self._lock:
            booking_id = next(self._ids)
        FlightInstance.reserve_across([(s.instance, s.cabin) for s in itinerary.segments],
                                      booking_id)
        now = self._clock()
        booking = Booking(id=booking_id, itinerary=itinerary, passenger=passenger,
                          fare=self._fare(itinerary), created_at=now,
                          held_until=now + self._hold_ttl)
        with self._lock:
            self._bookings[booking_id] = booking
        return booking

    def booking(self, booking_id: str) -> Booking:
        """按订单号取订单。"""
        with self._lock:
            found = self._bookings.get(booking_id)
        if found is None:
            raise BookingNotFoundError(f"unknown booking {booking_id!r}")
        return found

    def ticket(self, booking_id: str) -> Booking:
        """出票：占座还没过期就把 HELD 翻成 TICKETED；过期了就当场释放并报错。"""
        booking = self.booking(booking_id)
        if self._clock() > booking.held_until:
            self._release_all(booking)
            booking.transition_to(BookingStatus.CANCELLED)
            raise HoldExpiredError(f"hold on booking {booking_id} expired")
        booking.transition_to(BookingStatus.TICKETED)
        return booking

    def release_expired_holds(self) -> int:
        """清扫所有超时未出票的占座，返回释放的订单数。先在服务锁内取快照，出锁再动库存。"""
        now = self._clock()
        with self._lock:
            stale = [b for b in self._bookings.values()
                     if b.status is BookingStatus.HELD and b.held_until <= now]
        for booking in stale:
            self._release_all(booking)
            booking.transition_to(BookingStatus.CANCELLED)
        return len(stale)

    def _release_all(self, booking: Booking) -> None:
        """把这张订单从它每一段所在的航班上摘掉。"""
        for segment in booking.itinerary.segments:
            segment.instance.release(booking.id)

    # ---- 值机与登机 ------------------------------------------------------

    def check_in(self, booking_id: str,
                 preferred: Mapping[str, str] | None = None) -> Mapping[str, str]:
        """值机：在窗口期内给每一段选座，返回 `航班key → 座位号` 的只读快照。

        超售卖出去的那张票可能一段都选不到座——那不是错误，返回的快照里就没有这一段，
        它会在登机口按公开规则被处理。旅客**点名**的座位拿不到才抛 `SeatUnavailableError`；
        那时前面几段已经选好的座位仍然记在这张订单名下（它本来就占着那几班的库存），
        选座对同一张订单是幂等的，重试一次即可，不会留下"占着座位却没值机"的孤儿。
        """
        booking = self.booking(booking_id)
        now = self._clock()
        departure = booking.itinerary.departure
        if not departure - self._check_in_opens <= now <= departure - self._check_in_closes:
            raise InvalidTransitionError(f"check-in for {booking_id} is not open at {now}")
        if BookingStatus.CHECKED_IN not in ALLOWED_TRANSITIONS[booking.status]:
            raise InvalidTransitionError(f"booking {booking_id} is {booking.status.name}")
        preferred = preferred or {}
        assigned: dict[str, str] = {}
        for segment in booking.itinerary.segments:
            label = segment.instance.assign_seat(booking.id, preferred.get(segment.instance.key))
            if label is not None:
                assigned[segment.instance.key] = label
        booking.transition_to(BookingStatus.CHECKED_IN)
        booking.checked_in_at = now
        return assigned

    def board(self, flight_key: str) -> tuple[str, ...]:
        """关舱门结算：把已值机的旅客送上飞机，卖超的按公开规则拒载，返回被拒载的订单号。

        规则（写在这里，也写给旅客看）：**逐舱**结算，舱与舱之间不互相挤占；超出实际座位数时，
        先拒载"没拿到座位号"的，同样没座位就拒载"值机时间最晚"的。被拒载的订单退回 TICKETED，
        票还在手上，由客服改签——这正是超售这条政策真正的代价落地的地方。

        多段行程要登机两次，所以登机过的航段记在 `Booking.boarded` 里，整条行程走完才是 BOARDED；
        对同一班重复调用这个方法不会把旅客算第二遍。
        """
        instance = self.instance(flight_key)
        denied: list[str] = []
        for cabin in CabinClass:
            present = [self.booking(ref) for ref in instance.refs_in(cabin)]
            present = [b for b in present if b.status is BookingStatus.CHECKED_IN
                       and instance.key not in b.boarded]
            overflow = max(len(present) - instance.capacity(cabin), 0)
            present.sort(key=lambda b: (instance.seat_of(b.id) is not None,
                                        -(b.checked_in_at or b.created_at).timestamp()))
            for booking in present[:overflow]:
                booking.transition_to(BookingStatus.TICKETED)
                instance.release(booking.id)
                denied.append(booking.id)
            for booking in present[overflow:]:
                booking.boarded += (instance.key,)
                if len(booking.boarded) == len(booking.itinerary.segments):
                    booking.transition_to(BookingStatus.BOARDED)
        return tuple(denied)

    # ---- 取消与改签 ------------------------------------------------------

    def cancel(self, booking_id: str) -> Booking:
        """取消：先在锁内把状态翻成 CANCELLED（这一步就是"认领"，两个线程只有一个能翻成功，
        所以不会退两次款），再算退款、再把库存还回去。
        """
        now = self._clock()
        with self._lock:
            booking = self._bookings.get(booking_id)
            if booking is None:
                raise BookingNotFoundError(f"unknown booking {booking_id!r}")
            booking.transition_to(BookingStatus.CANCELLED)
        booking.refunded = self._refund(booking, now)
        self._release_all(booking)
        return booking

    def change(self, booking_id: str, new_itinerary: Itinerary) -> Booking:
        """改签：换一条行程，**先占新段再放旧段**，中途一刻也不松手。

        顺序是全部：先放后占，一旦新行程占不上，旅客连原来那张票都没有了。两条行程共用的航段
        原样保留（`reserve_across` 看到舱位没变就什么也不做），所以旅客已经选好的座位不会被
        改签动作白白抹掉——这是"改签 = 取消 + 重订"这个说法在实现上唯一站不住的地方。
        """
        booking = self.booking(booking_id)
        if booking.status not in (BookingStatus.HELD, BookingStatus.TICKETED):
            raise InvalidTransitionError(f"booking {booking_id} is {booking.status.name}")
        self._validate(new_itinerary)
        old = {s.instance.key: s for s in booking.itinerary.segments}
        new = {s.instance.key: s for s in new_itinerary.segments}
        FlightInstance.reserve_across([(s.instance, s.cabin) for s in new.values()], booking.id)
        for key, segment in old.items():
            if key not in new:
                segment.instance.release(booking.id)
        booking.itinerary = new_itinerary
        booking.fare = self._fare(new_itinerary)
        return booking


if __name__ == "__main__":
    day, narrow = date(2026, 7, 1), Aircraft.layout(
        "A320", "Airbus A320", {CabinClass.BUSINESS: (2, "AF"), CabinClass.ECONOMY: (3, "ABCDEF")})
    legs = [FlightInstance(Flight("MU5100", "SHA", "PEK", time(8, 0), timedelta(hours=2),
                                  narrow, "MU", marketed_as=("CZ9001",)), day),
            FlightInstance(Flight("MU2610", "PEK", "HRB", time(12, 0), timedelta(hours=2),
                                  narrow, "MU"), day)]
    now = datetime(2026, 6, 30, 9, 0)
    service = AirlineService(
        clock=lambda: now,
        connection=MinimumConnectionTime(timedelta(minutes=60), {"PEK": timedelta(minutes=90)},
                                         carrier_change=timedelta(minutes=30)),
        fare=cabin_fare({CabinClass.ECONOMY: 89000, CabinClass.BUSINESS: 268000}),
        refund=tiered_refund([(timedelta(days=7), 100), (timedelta(hours=24), 50)]))
    for leg in legs:
        service.schedule(leg)

    plan = service.search("SHA", "HRB", day, CabinClass.ECONOMY)[0]
    pnr = service.hold(plan, passenger="chi")
    print(f"{pnr.id}: {plan.stops} stop, {pnr.fare} fen, "
          f"economy left on leg 1 = {legs[0].available(CabinClass.ECONOMY)}")
    service.ticket(pnr.id)
    print(f"codeshare CZ9001 resolves to {service.instance('CZ9001@2026-07-01').key}")
    now = datetime(2026, 7, 1, 6, 0)
    print(f"checked in: {dict(service.check_in(pnr.id, {legs[0].key: '3A'}))}")
    print(f"denied boarding: {service.board(legs[0].key) + service.board(legs[1].key)}, "
          f"status now {service.booking(pnr.id).status.name}")
    now = datetime(2026, 7, 2, 0, 0)
    print(f"purged {service.purge_flown_before(now)} flown leg(s), "
          f"catalogue now {service.instance_count}, bookings {service.booking_count}")
