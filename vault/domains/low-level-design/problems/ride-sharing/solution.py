"""网约车（Uber）——匹配、行程状态机与计价的参考实现。

核心思路：派单的中心概念不是"分配"而是**要约**（`Offer`）——同一时刻只发给一位司机、带
超时、可被拒绝；司机在要约敞开期间被 `DriverPool` **独占持有**（AVAILABLE→OFFERED 是一次
锁内的比较并交换），所以两位乘客不可能同时匹配到同一位司机。要约被拒或超时，系统立刻把这
位司机拉进该行程的排除集并顺位发给下一位；候选耗尽就把行程明确置为 CANCELLED——宁可给乘
客一个确定的失败，也不让他停在"正在找车"里。行程生命周期是一张显式的转移表加一张"谁有权
取消"的许可表，取消只从 REQUESTED/MATCHED/ARRIVED 三个点出发，上车之后无人可取消。计价
（起步价 + 里程 + 时长）与动态加价（surge）是两个注入的普通策略，倍数在**下单那一刻**锁死
写进行程；第 4 关的拼车只是往行程上追加一条 `RideLeg`，状态机一行不改。

地理刻意做到最简：`Location` 是平面坐标，距离是直线距离。真实系统要的是路网与空间索引
（geohash / 四叉树），那是另一道题，本文不做，也不假装做了。
"""

from __future__ import annotations

import itertools
import math
import threading
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import Enum
from fractions import Fraction


# --------------------------------------------------------------------------
# 失败路径：一个小的异常家族。调用方可以只 catch 基类，也可以分别处理。


class RideError(Exception):
    """本设计里所有失败路径的公共基类。"""

class UnknownDriverError(RideError):
    """司机没有注册过。"""

class UnknownTripError(RideError):
    """行程号不存在。"""

class DriverBusyError(RideError):
    """司机正被一张要约占着或正在跑车，此刻不能上下线。"""

class NoDriverAvailableError(RideError):
    """没有任何可派的司机——注册的都离线、都在跑车，或都已拒绝过这一单。"""

class OfferExpiredError(RideError):
    """要约已超时、已被拒绝，或已经被别人用掉了。"""

class IllegalTransitionError(RideError):
    """行程状态机不允许这次转移。"""

class CancellationNotAllowedError(RideError):
    """这一方此刻无权取消这趟行程。"""

class SeatUnavailableError(RideError):
    """车上剩余座位不够，或拼车绕路超过了上限。"""


# --------------------------------------------------------------------------
# 地理：全题只用到"两点之间有多远"。


@dataclass(frozen=True, slots=True)
class Location:
    """平面上的一个点，单位当作公里。真实系统这里是经纬度加路网距离；本题用直线距离，
    因为这道题考的是撮合与状态流转，不是邻近搜索。换成路网只影响这一个方法。
    """

    x: float
    y: float

    def distance_to(self, other: "Location") -> float:
        """到另一点的直线距离。"""
        return math.hypot(self.x - other.x, self.y - other.y)


# --------------------------------------------------------------------------
# 司机：不可变记录，改状态靠整条替换，所以交给调用方的永远是安全的快照。


class DriverStatus(Enum):
    """司机的四个状态。OFFERED 是本设计的关键：它表示"被一张敞开的要约独占着"，
    既不是空闲（不能再被派单）也不是在跑车（还没人接单）。少了它，派单就只能靠
    "先查后写"，两位乘客会同时匹配到同一位司机。
    """

    OFFLINE = "offline"
    AVAILABLE = "available"
    OFFERED = "offered"
    ON_TRIP = "on_trip"


@dataclass(frozen=True, slots=True)
class Driver:
    """一位司机此刻的全部状态。不可变：`DriverPool` 用 `dataclasses.replace` 整条换掉，
    因此不存在"改了一半"的中间态，也不怕把它直接交给调用方。
    """

    id: str
    rating: float = 5.0
    seats: int = 4
    location: Location | None = None
    status: DriverStatus = DriverStatus.OFFLINE
    held_by: str | None = None
    trip_id: str | None = None
    idle_since: datetime | None = None


# --------------------------------------------------------------------------
# 乘客的请求、要约、行程段。


@dataclass(frozen=True, slots=True)
class RideRequest:
    """一次叫车请求：谁、从哪到哪、几个人。不可变，可以安全地跨线程传。"""

    rider_id: str
    pickup: Location
    dropoff: Location
    seats: int = 1


@dataclass(frozen=True, slots=True)
class Offer:
    """一张要约：把某一趟行程派给某一位司机，`expires_at` 之前有效。

    它是"正在征求同意"的凭据，不是分配结果。司机只有 `accept` 之后才真正上车，
    所以要约超时不需要任何回滚——司机从没被写进行程。
    """

    id: str
    trip_id: str
    driver_id: str
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class Fare:
    """一段行程的车费明细，单位是分。`surge` 是下单那一刻锁死的倍数。"""

    base: int
    distance: int
    time: int
    surge: Fraction

    @property
    def total(self) -> int:
        """实付金额：三项相加再乘倍数，向下取整到分。"""
        return int((self.base + self.distance + self.time) * self.surge)


@dataclass(frozen=True, slots=True)
class RideLeg:
    """行程里**一位乘客**的那一段：上下车点、占几个座、什么时候上的车、锁死的倍数。

    有了它，"一个人的行程"和"拼车"就是同一种东西（一条腿 vs 两条腿），第 4 关不必
    引入第二套模型。`fare` 在行程结束时回填。
    """

    rider_id: str
    pickup: Location
    dropoff: Location
    seats: int
    joined_at: datetime
    surge: Fraction
    fare: Fare | None = None


# --------------------------------------------------------------------------
# 行程状态机：一张转移表 + 一张取消许可表。


class TripState(Enum):
    """行程的六个状态。"""

    REQUESTED = "requested"
    MATCHED = "matched"
    ARRIVED = "arrived"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Party(Enum):
    """谁在动这趟行程——取消权限按方区分，所以它必须是一个显式的参数。"""

    RIDER = "rider"
    DRIVER = "driver"
    SYSTEM = "system"


ALLOWED_TRANSITIONS: Mapping[TripState, frozenset[TripState]] = {
    TripState.REQUESTED: frozenset({TripState.MATCHED, TripState.CANCELLED}),
    TripState.MATCHED: frozenset({TripState.ARRIVED, TripState.CANCELLED}),
    TripState.ARRIVED: frozenset({TripState.IN_PROGRESS, TripState.CANCELLED}),
    TripState.IN_PROGRESS: frozenset({TripState.COMPLETED}),
    TripState.COMPLETED: frozenset(),
    TripState.CANCELLED: frozenset(),
}

CANCELLABLE_BY: Mapping[TripState, frozenset[Party]] = {
    TripState.REQUESTED: frozenset({Party.RIDER, Party.SYSTEM}),
    TripState.MATCHED: frozenset({Party.RIDER, Party.DRIVER, Party.SYSTEM}),
    TripState.ARRIVED: frozenset({Party.RIDER, Party.DRIVER, Party.SYSTEM}),
}


@dataclass(frozen=True, slots=True)
class StateChange:
    """一次转移的留痕：什么时候、从哪到哪、谁干的、为什么。客服每天都要回答"这单几点
    被谁取消的"，这个问题只能靠事中记录，不能事后推算。
    """

    at: datetime
    previous: TripState
    current: TripState
    by: Party
    reason: str | None = None


class Trip:
    """一趟行程：一位或多位乘客、一位司机、一条显式的状态轨迹。

    不变量：`state` 只能沿 `ALLOWED_TRANSITIONS` 移动，唯一的改法是 `transition_to`；
    每次转移都留一条 `StateChange`。它自己**不带锁**——行程永远在 `DispatchService`
    的锁里被改，多一把锁只会多一个锁序问题。
    """

    def __init__(self, trip_id: str, request: RideRequest, created_at: datetime,
                 surge: Fraction) -> None:
        self.id = trip_id
        self.request = request
        self.created_at = created_at
        self.driver_id: str | None = None
        self._state = TripState.REQUESTED
        self._legs = [RideLeg(request.rider_id, request.pickup, request.dropoff,
                              request.seats, created_at, surge)]
        self._history: list[StateChange] = []

    @property
    def state(self) -> TripState:
        """当前状态。只读——想改就得走一次受检的转移。"""
        return self._state

    @property
    def legs(self) -> tuple[RideLeg, ...]:
        """每位乘客那一段的不可变快照，按上车顺序。"""
        return tuple(self._legs)

    @property
    def history(self) -> tuple[StateChange, ...]:
        """状态轨迹的不可变快照。"""
        return tuple(self._history)

    @property
    def seats_taken(self) -> int:
        """车上已被占用的座位数。"""
        return sum(leg.seats for leg in self._legs)

    @property
    def started_at(self) -> datetime | None:
        """乘客上车的时刻，直接从状态轨迹里读——不另存一个字段，就不会有两份真相。"""
        return next((c.at for c in self._history if c.current is TripState.IN_PROGRESS), None)

    def transition_to(self, target: TripState, now: datetime, by: Party,
                      reason: str | None = None) -> None:
        """按转移表走一步；非法转移抛异常，**绝不静默忽略**——被吞掉的非法转移意味着
        调用方以为车已经开了，而行程其实还停在"正在找车"。
        """
        if target not in ALLOWED_TRANSITIONS[self._state]:
            raise IllegalTransitionError(
                f"trip {self.id}: {self._state.value} -> {target.value} is not allowed")
        self._history.append(StateChange(now, self._state, target, by, reason))
        self._state = target

    def add_leg(self, leg: RideLeg) -> None:
        """拼车：往行程上追加一位乘客。它**不碰状态机**——多一个人上车不是一次状态
        转移，这正是第 4 关"加需求不改老代码"的证据。
        """
        self._legs.append(leg)

    def price_legs(self, table: "FareTable", now: datetime, discount: Fraction) -> None:
        """结束时给每条腿回填车费：里程按这条腿自己的起终点，时长从**上车**那一刻算起——
        等车的那几分钟不收钱，所以计时起点是 `max(上车时刻, 发车时刻)` 而不是叫车时刻。
        """
        share = discount if len(self._legs) > 1 else Fraction(1)
        start = self.started_at or now
        self._legs = [replace(leg, fare=table.quote(
            leg.pickup.distance_to(leg.dropoff),
            (now - max(leg.joined_at, start)).total_seconds() / 60, leg.surge * share))
            for leg in self._legs]

    def fare_for(self, rider_id: str) -> Fare | None:
        """某位乘客这一趟要付多少；行程没结束就是 `None`。"""
        return next((leg.fare for leg in self._legs if leg.rider_id == rider_id), None)


# --------------------------------------------------------------------------
# 计价与动态加价：两类"会变的规则"，一张不可变的表加一个普通函数。


@dataclass(frozen=True, slots=True)
class FareTable:
    """一张价目表：起步价 + 每公里 + 每分钟，单位都是分。

    它是数据不是算法，所以是 `frozen dataclass` 而不是抽象基类——换城市就是换一张表。
    """

    base: int
    per_km: int
    per_minute: int

    def quote(self, km: float, minutes: float, surge: Fraction = Fraction(1)) -> Fare:
        """按里程与时长报一笔明细。四舍五入只发生在这里，总额靠 `Fare.total` 算。"""
        return Fare(self.base, round(self.per_km * km), round(self.per_minute * minutes), surge)


SurgePolicy = Callable[[RideRequest, int, int], Fraction]
MatchPolicy = Callable[[RideRequest, Driver, datetime], float]
Clock = Callable[[], datetime]


def no_surge(request: RideRequest, waiting: int, available: int) -> Fraction:
    """不加价——倍数策略的下界，也是测试里最省心的那一个。"""
    return Fraction(1)


def demand_surge(steps: Sequence[tuple[Fraction, Fraction]]) -> SurgePolicy:
    """按"在等的人 ÷ 可派的车"分档加价：`steps` 是 (比值门槛, 倍数)，从高到低取第一个命中的。

    用 `Fraction` 不用 `float`：倍数要乘进金额，1.2 在二进制里不是 1.2，几千万单之后
    对不上的那几分钱没人说得清是谁的。
    """
    ordered = tuple(sorted(steps, key=lambda s: s[0], reverse=True))

    def surge(request: RideRequest, waiting: int, available: int) -> Fraction:
        ratio = Fraction(waiting, max(1, available))
        return next((m for threshold, m in ordered if ratio >= threshold), Fraction(1))

    return surge


def nearest_driver(request: RideRequest, driver: Driver, now: datetime) -> float:
    """最近优先：得分就是司机到上车点的距离，越小越优先。"""
    assert driver.location is not None
    return driver.location.distance_to(request.pickup)


def weighted_score(per_km: float = 1.0, per_rating_point: float = 1.0,
                   per_idle_minute: float = 0.05) -> MatchPolicy:
    """距离、评分、空闲时长的加权打分，越小越优先。

    评分与空闲时长取**负**权重：分高的、等得久的应该被优先派单，后者是司机端公平性的
    最低限度——只按距离排，市中心那位永远抢不到单。三个权重量纲不同（公里、分、分钟），
    所以权重本身就是"一个评分点值多少公里"的换算率，面试时要把这句话说出来。
    """

    def score(request: RideRequest, driver: Driver, now: datetime) -> float:
        assert driver.location is not None
        idle = 0.0 if driver.idle_since is None else (now - driver.idle_since).total_seconds() / 60
        return (driver.location.distance_to(request.pickup) * per_km
                - driver.rating * per_rating_point - idle * per_idle_minute)

    return score


# --------------------------------------------------------------------------
# DriverPool：司机名册与"独占持有"。这道题的并发正确性全部落在这一个类里。


class DriverPool:
    """司机池：注册、上下线，以及 AVAILABLE ↔ OFFERED ↔ ON_TRIP 三态之间的受控迁移。

    不变量：一位司机任一时刻至多被一张要约或一趟行程占着。`hold` / `release` / `commit`
    都是锁内的**比较并交换**：先验证当前状态和占用者，再整条替换，中间没有缝隙，所以
    "先查空闲再写占用"那个经典竞态在这里不可能发生。

    纪律：池子从不回调 `DispatchService`。锁序因此只有一个方向（服务锁 → 池锁），
    不存在环，也就不存在锁序死锁。
    """

    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._drivers: dict[str, Driver] = {}
        self._lock = threading.Lock()

    def register(self, driver_id: str, rating: float = 5.0, seats: int = 4) -> None:
        """登记一位司机，初始离线。"""
        with self._lock:
            self._drivers[driver_id] = Driver(id=driver_id, rating=rating, seats=seats)

    def driver(self, driver_id: str) -> Driver:
        """取一位司机的只读快照。"""
        with self._lock:
            found = self._drivers.get(driver_id)
        if found is None:
            raise UnknownDriverError(f"unknown driver {driver_id!r}")
        return found

    @property
    def available_count(self) -> int:
        """此刻可派的司机数——只给计数，不把名册交出去。"""
        with self._lock:
            return sum(1 for d in self._drivers.values() if d.status is DriverStatus.AVAILABLE)

    def go_online(self, driver_id: str, location: Location) -> None:
        """司机上线并报位置；已经在跑车或被要约占着的不允许重复上线。"""
        self._set_idle(driver_id, DriverStatus.AVAILABLE, location)

    def go_offline(self, driver_id: str) -> None:
        """司机收车。跑车中或被要约占着时拒绝——否则乘客会在路上被凭空丢下。"""
        self._set_idle(driver_id, DriverStatus.OFFLINE, None)

    def candidates(self, seats: int, exclude: Iterable[str] = ()) -> tuple[Driver, ...]:
        """此刻可派、且座位够的司机快照。排除集来自"已经拒绝过这一单"的那些人。"""
        banned = frozenset(exclude)
        with self._lock:
            return tuple(d for d in self._drivers.values()
                         if d.status is DriverStatus.AVAILABLE and d.seats >= seats
                         and d.id not in banned)

    def hold(self, driver_id: str, offer_id: str) -> bool:
        """把司机从 AVAILABLE 独占到 OFFERED，成功返回 `True`。

        这是全题最关键的一处：判断"还空闲吗"和写入"被我占了"在同一把锁里完成。
        两个线程同时为不同乘客抢同一位司机，只有一个能拿到 `True`。
        """
        with self._lock:
            driver = self._drivers.get(driver_id)
            if driver is None or driver.status is not DriverStatus.AVAILABLE:
                return False
            self._drivers[driver_id] = replace(driver, status=DriverStatus.OFFERED, held_by=offer_id)
            return True

    def release(self, driver_id: str, offer_id: str) -> bool:
        """要约被拒或超时，把司机还回 AVAILABLE。只有持有者能释放，所以迟到的超时清扫
        不会把已经在跑下一单的司机打回空闲。幂等，且永不抛异常——它总跑在失败路径上。
        """
        now = self._clock()
        with self._lock:
            driver = self._drivers.get(driver_id)
            if driver is None or driver.held_by != offer_id:
                return False
            self._drivers[driver_id] = replace(driver, status=DriverStatus.AVAILABLE,
                                               held_by=None, idle_since=now)
            return True

    def commit(self, driver_id: str, offer_id: str, trip_id: str) -> bool:
        """司机接单：OFFERED → ON_TRIP，同样只认当前持有者。"""
        with self._lock:
            driver = self._drivers.get(driver_id)
            if driver is None or driver.held_by != offer_id:
                return False
            self._drivers[driver_id] = replace(driver, status=DriverStatus.ON_TRIP,
                                               held_by=None, trip_id=trip_id)
            return True

    def finish(self, driver_id: str, location: Location) -> None:
        """行程结束或中途取消：司机回到 AVAILABLE，位置更新为当前所在。"""
        now = self._clock()
        with self._lock:
            driver = self._drivers.get(driver_id)
            if driver is not None:
                self._drivers[driver_id] = replace(driver, status=DriverStatus.AVAILABLE,
                                                   location=location, held_by=None,
                                                   trip_id=None, idle_since=now)

    def _set_idle(self, driver_id: str, status: DriverStatus, location: Location | None) -> None:
        """上线与下线共用的一步：占用中的司机一律拒绝，其余整条替换。"""
        now = self._clock()
        with self._lock:
            driver = self._drivers.get(driver_id)
            if driver is None:
                raise UnknownDriverError(f"unknown driver {driver_id!r}")
            if driver.status in (DriverStatus.OFFERED, DriverStatus.ON_TRIP):
                raise DriverBusyError(f"driver {driver_id} is {driver.status.value}")
            self._drivers[driver_id] = replace(driver, status=status, held_by=None,
                                               location=location or driver.location,
                                               idle_since=now if location else None)


# --------------------------------------------------------------------------
# DispatchService：门面。管行程、发要约、推状态、结算。司机的状态它一个字节都不存。


class DispatchService:
    """派单服务：叫车 → 逐个发要约 → 接单 → 到达 → 上车 → 完成，外加取消与拼车。

    不变量（并发测试直接断言它们）：
    1. 处在 REQUESTED 的行程**必定**恰好有一张敞开的要约——没有人会停在"正在找车"里；
    2. 一位司机不会同时出现在两趟未终结的行程上；
    3. `_offers` / `_excluded` 两张表只在行程活着时有条目，行程一终结就被删干净。

    锁纪律：服务锁保护行程表与要约表，可以在持有它时去调 `DriverPool`（服务锁 → 池锁，
    方向唯一）；反向调用不存在。GIL 在这里什么都不保证——`if driver.status is AVAILABLE`
    之后紧跟一次赋值，是两段字节码，中间随时可能切线程。
    """

    def __init__(self, clock: Clock, pool: DriverPool, fares: FareTable,
                 match: MatchPolicy = nearest_driver, surge: SurgePolicy = no_surge,
                 offer_ttl: timedelta = timedelta(seconds=15),
                 pool_discount: Fraction = Fraction(4, 5),
                 max_detour_km: float = 2.0) -> None:
        self._clock, self._pool, self._fares = clock, pool, fares
        self._match, self._surge, self._offer_ttl = match, surge, offer_ttl
        self._pool_discount, self._max_detour_km = pool_discount, max_detour_km
        self._trips: dict[str, Trip] = {}
        self._offers: dict[str, Offer] = {}
        self._offer_by_trip: dict[str, str] = {}
        self._excluded: dict[str, set[str]] = {}
        self._lock = threading.RLock()
        self._ids = itertools.count(1)

    # ---- 读 ---------------------------------------------------------------

    def trip(self, trip_id: str) -> Trip:
        """按行程号取行程。"""
        with self._lock:
            found = self._trips.get(trip_id)
        if found is None:
            raise UnknownTripError(f"unknown trip {trip_id!r}")
        return found

    def open_offer(self, trip_id: str) -> Offer | None:
        """这趟行程此刻敞开的要约；没有就是 `None`。"""
        with self._lock:
            offer_id = self._offer_by_trip.get(trip_id)
            return self._offers.get(offer_id) if offer_id else None

    @property
    def open_offer_count(self) -> int:
        """敞开的要约数——用计数暴露内部表的大小，测试据此断言它确实会缩小。"""
        with self._lock:
            return len(self._offers)

    # ---- 第 1、2 关：叫车与要约 -------------------------------------------

    def request_ride(self, request: RideRequest) -> Trip:
        """乘客叫车：建行程（REQUESTED），锁死加价倍数，并立刻把要约发给最优的一位司机。

        一位候选都没有时**不建行程**、直接抛 `NoDriverAvailableError`：留下一个永远没有
        要约的 REQUESTED 行程，就是把不变量 1 破坏在了起点上。
        """
        now = self._clock()
        with self._lock:
            waiting = sum(1 for t in self._trips.values() if t.state is TripState.REQUESTED)
            multiplier = self._surge(request, waiting + 1, self._pool.available_count)
            trip = Trip(f"T{next(self._ids)}", request, now, multiplier)
            self._trips[trip.id] = trip
            self._excluded[trip.id] = set()
            if self._offer_next(trip, now) is None:
                del self._trips[trip.id], self._excluded[trip.id]
                raise NoDriverAvailableError(f"no driver can take {request.rider_id}'s ride")
            return trip

    def accept(self, offer_id: str) -> Trip:
        """司机接单：要约必须还活着、司机必须还被它占着，然后 REQUESTED → MATCHED。

        过期是**惰性**判断的：哪怕清扫还没跑，一张过了点的要约在这里也已经无效，所以
        正确性不依赖定时任务跑没跑。
        """
        now = self._clock()
        with self._lock:
            offer = self._offers.get(offer_id)
            if offer is None:
                raise OfferExpiredError(f"offer {offer_id!r} is no longer open")
            if offer.expires_at <= now:
                self._reoffer(offer, now, "offer timed out")
                raise OfferExpiredError(f"offer {offer_id} expired at {offer.expires_at:%H:%M:%S}")
            trip = self._trips[offer.trip_id]
            if not self._pool.commit(offer.driver_id, offer.id, trip.id):
                raise OfferExpiredError(f"driver {offer.driver_id} no longer holds {offer_id}")
            self._close_offer(offer)
            self._excluded.pop(trip.id, None)
            trip.driver_id = offer.driver_id
            trip.transition_to(TripState.MATCHED, now, Party.DRIVER)
            return trip

    def decline(self, offer_id: str) -> Trip:
        """司机拒单：立刻把他放回可派池、拉进这趟行程的排除集，并顺位发给下一位。"""
        now = self._clock()
        with self._lock:
            offer = self._offers.get(offer_id)
            if offer is None:
                raise OfferExpiredError(f"offer {offer_id!r} is no longer open")
            self._reoffer(offer, now, "driver declined")
            return self._trips[offer.trip_id]

    def expire_offers(self) -> int:
        """清扫超时的要约，返回清掉的张数。沉默的司机和拒单的司机走同一条路径——
        对乘客来说两者没有区别，代码里也就不该有两套。
        """
        now = self._clock()
        with self._lock:
            stale = [o for o in self._offers.values() if o.expires_at <= now]
            for offer in stale:
                self._reoffer(offer, now, "offer timed out")
            return len(stale)

    # ---- 第 1 关：行程推进 -------------------------------------------------

    def driver_arrived(self, trip_id: str) -> Trip:
        """司机到达上车点：MATCHED → ARRIVED。"""
        now = self._clock()
        with self._lock:
            trip = self.trip(trip_id)
            trip.transition_to(TripState.ARRIVED, now, Party.DRIVER)
            return trip

    def start_trip(self, trip_id: str) -> Trip:
        """乘客上车、开始计时：ARRIVED → IN_PROGRESS。"""
        now = self._clock()
        with self._lock:
            trip = self.trip(trip_id)
            trip.transition_to(TripState.IN_PROGRESS, now, Party.DRIVER)
            return trip

    def complete_trip(self, trip_id: str) -> Trip:
        """送达：IN_PROGRESS → COMPLETED，给每条腿结算，司机回到最后一个下车点待命。"""
        now = self._clock()
        with self._lock:
            trip = self.trip(trip_id)
            trip.transition_to(TripState.COMPLETED, now, Party.DRIVER)
            trip.price_legs(self._fares, now, self._pool_discount)
            if trip.driver_id is not None:
                self._pool.finish(trip.driver_id, trip.legs[-1].dropoff)
            return trip

    def cancel_trip(self, trip_id: str, by: Party, reason: str | None = None) -> Trip:
        """取消。许可表说了算：上车之后（IN_PROGRESS）谁都不能取消——车已经在路上，
        这时候要的是"提前结束并按已走里程计费"，那是另一个动作，不是取消。
        """
        now = self._clock()
        with self._lock:
            trip = self.trip(trip_id)
            if by not in CANCELLABLE_BY.get(trip.state, frozenset()):
                raise CancellationNotAllowedError(
                    f"{by.value} cannot cancel trip {trip_id} in {trip.state.value}")
            offer = self.open_offer(trip_id)
            if offer is not None:
                self._pool.release(offer.driver_id, offer.id)
                self._close_offer(offer)
            if trip.driver_id is not None:
                self._pool.finish(trip.driver_id, trip.request.pickup)
            self._excluded.pop(trip.id, None)
            trip.transition_to(TripState.CANCELLED, now, by, reason)
            return trip

    # ---- 第 4 关：拼车 -----------------------------------------------------

    def join_trip(self, trip_id: str, request: RideRequest) -> Trip:
        """第二位乘客拼上一趟已经匹配的行程。

        两道闸：车上还得有座；绕路（A→P→Q→B 的总长减去 A→B）不超过上限。通过之后
        只是 `Trip.add_leg` 一条腿——状态机、要约机制、司机池都不知道发生过拼车。
        """
        now = self._clock()
        with self._lock:
            trip = self.trip(trip_id)
            if trip.state not in (TripState.MATCHED, TripState.ARRIVED, TripState.IN_PROGRESS):
                raise IllegalTransitionError(f"trip {trip_id} in {trip.state.value} takes no rider")
            assert trip.driver_id is not None
            if trip.seats_taken + request.seats > self._pool.driver(trip.driver_id).seats:
                raise SeatUnavailableError(f"trip {trip_id} has no room for {request.seats} seat(s)")
            a, b = trip.legs[0].pickup, trip.legs[0].dropoff
            detour = (a.distance_to(request.pickup) + request.pickup.distance_to(request.dropoff)
                      + request.dropoff.distance_to(b) - a.distance_to(b))
            if detour > self._max_detour_km:
                raise SeatUnavailableError(f"joining would add {detour:.1f} km, over the limit")
            trip.add_leg(RideLeg(request.rider_id, request.pickup, request.dropoff,
                                 request.seats, now,
                                 self._surge(request, 1, self._pool.available_count)))
            return trip

    # ---- 内部 -------------------------------------------------------------

    def _offer_next(self, trip: Trip, now: datetime) -> Offer | None:
        """给这趟行程找下一位候选并独占他，发出要约。调用方须已持有服务锁。

        排序键的第二项是司机 id：打分相同时若靠字典顺序，测试会飘，线上会出现"同样的
        两位司机，这次派给了谁取决于内存布局"这种没法复现的抱怨。
        """
        excluded = self._excluded.get(trip.id, set())
        ranked = sorted(self._pool.candidates(trip.request.seats, excluded),
                        key=lambda d: (self._match(trip.request, d, now), d.id))
        for driver in ranked:
            offer_id = f"O{next(self._ids)}"
            if self._pool.hold(driver.id, offer_id):
                offer = Offer(offer_id, trip.id, driver.id, now + self._offer_ttl)
                self._offers[offer_id] = offer
                self._offer_by_trip[trip.id] = offer_id
                return offer
        return None

    def _close_offer(self, offer: Offer) -> None:
        """把一张要约从两张表里彻底摘掉。这是它们唯一会缩小的地方，所以只此一个出口。"""
        self._offers.pop(offer.id, None)
        if self._offer_by_trip.get(offer.trip_id) == offer.id:
            del self._offer_by_trip[offer.trip_id]

    def _reoffer(self, offer: Offer, now: datetime, reason: str) -> None:
        """拒单／超时的统一处理：放人、排除、顺位再发；候选耗尽就把行程明确取消掉。"""
        self._pool.release(offer.driver_id, offer.id)
        self._close_offer(offer)
        trip = self._trips[offer.trip_id]
        self._excluded.setdefault(trip.id, set()).add(offer.driver_id)
        if self._offer_next(trip, now) is None:
            trip.transition_to(TripState.CANCELLED, now, Party.SYSTEM, "no driver available")
            self._excluded.pop(trip.id, None)


if __name__ == "__main__":
    from datetime import UTC

    now = datetime(2026, 9, 20, 8, 0, tzinfo=UTC)
    pool = DriverPool(clock=lambda: now)
    for name, x in [("d1", 1.0), ("d2", 3.0), ("d3", 0.5)]:
        pool.register(name, rating=4.8)
        pool.go_online(name, Location(x, 0.0))

    service = DispatchService(clock=lambda: now, pool=pool, match=weighted_score(),
                              fares=FareTable(base=900, per_km=220, per_minute=35),
                              surge=demand_surge([(Fraction(2), Fraction(3, 2))]))
    trip = service.request_ride(RideRequest("r1", Location(0, 0), Location(6, 8)))
    print(f"{trip.id} offered to {service.open_offer(trip.id).driver_id}")
    service.decline(service.open_offer(trip.id).id)          # 拒单后自动顺位
    service.accept(service.open_offer(trip.id).id)
    service.driver_arrived(trip.id)
    service.start_trip(trip.id)
    service.join_trip(trip.id, RideRequest("r2", Location(1.0, 1.0), Location(6.5, 8.0)))
    now = now + timedelta(minutes=22)
    for leg in service.complete_trip(trip.id).legs:
        print(f"{leg.rider_id} pays {leg.fare.total} fen to {trip.driver_id}")
