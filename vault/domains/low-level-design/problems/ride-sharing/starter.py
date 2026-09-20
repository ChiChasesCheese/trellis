"""网约车（Uber）——起始模板。

公开的类名、方法签名、`Enum`、`dataclass`、转移表和异常都和 `solution.py` 一致；把标了
`raise NotImplementedError` 的方法体一个个填上，就是完整的参考实现。运行：

    IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/ride-sharing -q
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
        raise NotImplementedError


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
        raise NotImplementedError


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
        raise NotImplementedError

    @property
    def state(self) -> TripState:
        """当前状态。只读——想改就得走一次受检的转移。"""
        raise NotImplementedError

    @property
    def legs(self) -> tuple[RideLeg, ...]:
        """每位乘客那一段的不可变快照，按上车顺序。"""
        raise NotImplementedError

    @property
    def history(self) -> tuple[StateChange, ...]:
        """状态轨迹的不可变快照。"""
        raise NotImplementedError

    @property
    def seats_taken(self) -> int:
        """车上已被占用的座位数。"""
        raise NotImplementedError

    @property
    def started_at(self) -> datetime | None:
        """乘客上车的时刻，直接从状态轨迹里读——不另存一个字段，就不会有两份真相。"""
        raise NotImplementedError

    def transition_to(self, target: TripState, now: datetime, by: Party,
                      reason: str | None = None) -> None:
        """按转移表走一步；非法转移抛异常，**绝不静默忽略**——被吞掉的非法转移意味着
        调用方以为车已经开了，而行程其实还停在"正在找车"。
        """
        raise NotImplementedError

    def add_leg(self, leg: RideLeg) -> None:
        """拼车：往行程上追加一位乘客。它**不碰状态机**——多一个人上车不是一次状态
        转移，这正是第 4 关"加需求不改老代码"的证据。
        """
        raise NotImplementedError

    def price_legs(self, table: "FareTable", now: datetime, discount: Fraction) -> None:
        """结束时给每条腿回填车费：里程按这条腿自己的起终点，时长从**上车**那一刻算起——
        等车的那几分钟不收钱，所以计时起点是 `max(上车时刻, 发车时刻)` 而不是叫车时刻。
        """
        raise NotImplementedError

    def fare_for(self, rider_id: str) -> Fare | None:
        """某位乘客这一趟要付多少；行程没结束就是 `None`。"""
        raise NotImplementedError


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
        raise NotImplementedError


SurgePolicy = Callable[[RideRequest, int, int], Fraction]
MatchPolicy = Callable[[RideRequest, Driver, datetime], float]
Clock = Callable[[], datetime]


def no_surge(request: RideRequest, waiting: int, available: int) -> Fraction:
    """不加价——倍数策略的下界，也是测试里最省心的那一个。"""
    raise NotImplementedError


def demand_surge(steps: Sequence[tuple[Fraction, Fraction]]) -> SurgePolicy:
    """按"在等的人 ÷ 可派的车"分档加价：`steps` 是 (比值门槛, 倍数)，从高到低取第一个命中的。

    用 `Fraction` 不用 `float`：倍数要乘进金额，1.2 在二进制里不是 1.2，几千万单之后
    对不上的那几分钱没人说得清是谁的。
    """
    raise NotImplementedError


def nearest_driver(request: RideRequest, driver: Driver, now: datetime) -> float:
    """最近优先：得分就是司机到上车点的距离，越小越优先。"""
    raise NotImplementedError


def weighted_score(per_km: float = 1.0, per_rating_point: float = 1.0,
                   per_idle_minute: float = 0.05) -> MatchPolicy:
    """距离、评分、空闲时长的加权打分，越小越优先。

    评分与空闲时长取**负**权重：分高的、等得久的应该被优先派单，后者是司机端公平性的
    最低限度——只按距离排，市中心那位永远抢不到单。三个权重量纲不同（公里、分、分钟），
    所以权重本身就是"一个评分点值多少公里"的换算率，面试时要把这句话说出来。
    """
    raise NotImplementedError


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
        raise NotImplementedError

    def register(self, driver_id: str, rating: float = 5.0, seats: int = 4) -> None:
        """登记一位司机，初始离线。"""
        raise NotImplementedError

    def driver(self, driver_id: str) -> Driver:
        """取一位司机的只读快照。"""
        raise NotImplementedError

    @property
    def available_count(self) -> int:
        """此刻可派的司机数——只给计数，不把名册交出去。"""
        raise NotImplementedError

    def go_online(self, driver_id: str, location: Location) -> None:
        """司机上线并报位置；已经在跑车或被要约占着的不允许重复上线。"""
        raise NotImplementedError

    def go_offline(self, driver_id: str) -> None:
        """司机收车。跑车中或被要约占着时拒绝——否则乘客会在路上被凭空丢下。"""
        raise NotImplementedError

    def candidates(self, seats: int, exclude: Iterable[str] = ()) -> tuple[Driver, ...]:
        """此刻可派、且座位够的司机快照。排除集来自"已经拒绝过这一单"的那些人。"""
        raise NotImplementedError

    def hold(self, driver_id: str, offer_id: str) -> bool:
        """把司机从 AVAILABLE 独占到 OFFERED，成功返回 `True`。

        这是全题最关键的一处：判断"还空闲吗"和写入"被我占了"在同一把锁里完成。
        两个线程同时为不同乘客抢同一位司机，只有一个能拿到 `True`。
        """
        raise NotImplementedError

    def release(self, driver_id: str, offer_id: str) -> bool:
        """要约被拒或超时，把司机还回 AVAILABLE。只有持有者能释放，所以迟到的超时清扫
        不会把已经在跑下一单的司机打回空闲。幂等，且永不抛异常——它总跑在失败路径上。
        """
        raise NotImplementedError

    def commit(self, driver_id: str, offer_id: str, trip_id: str) -> bool:
        """司机接单：OFFERED → ON_TRIP，同样只认当前持有者。"""
        raise NotImplementedError

    def finish(self, driver_id: str, location: Location) -> None:
        """行程结束或中途取消：司机回到 AVAILABLE，位置更新为当前所在。"""
        raise NotImplementedError

    def _set_idle(self, driver_id: str, status: DriverStatus, location: Location | None) -> None:
        """上线与下线共用的一步：占用中的司机一律拒绝，其余整条替换。"""
        raise NotImplementedError


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
        raise NotImplementedError

    # ---- 读 ---------------------------------------------------------------

    def trip(self, trip_id: str) -> Trip:
        """按行程号取行程。"""
        raise NotImplementedError

    def open_offer(self, trip_id: str) -> Offer | None:
        """这趟行程此刻敞开的要约；没有就是 `None`。"""
        raise NotImplementedError

    @property
    def open_offer_count(self) -> int:
        """敞开的要约数——用计数暴露内部表的大小，测试据此断言它确实会缩小。"""
        raise NotImplementedError

    # ---- 第 1、2 关：叫车与要约 -------------------------------------------

    def request_ride(self, request: RideRequest) -> Trip:
        """乘客叫车：建行程（REQUESTED），锁死加价倍数，并立刻把要约发给最优的一位司机。

        一位候选都没有时**不建行程**、直接抛 `NoDriverAvailableError`：留下一个永远没有
        要约的 REQUESTED 行程，就是把不变量 1 破坏在了起点上。
        """
        raise NotImplementedError

    def accept(self, offer_id: str) -> Trip:
        """司机接单：要约必须还活着、司机必须还被它占着，然后 REQUESTED → MATCHED。

        过期是**惰性**判断的：哪怕清扫还没跑，一张过了点的要约在这里也已经无效，所以
        正确性不依赖定时任务跑没跑。
        """
        raise NotImplementedError

    def decline(self, offer_id: str) -> Trip:
        """司机拒单：立刻把他放回可派池、拉进这趟行程的排除集，并顺位发给下一位。"""
        raise NotImplementedError

    def expire_offers(self) -> int:
        """清扫超时的要约，返回清掉的张数。沉默的司机和拒单的司机走同一条路径——
        对乘客来说两者没有区别，代码里也就不该有两套。
        """
        raise NotImplementedError

    # ---- 第 1 关：行程推进 -------------------------------------------------

    def driver_arrived(self, trip_id: str) -> Trip:
        """司机到达上车点：MATCHED → ARRIVED。"""
        raise NotImplementedError

    def start_trip(self, trip_id: str) -> Trip:
        """乘客上车、开始计时：ARRIVED → IN_PROGRESS。"""
        raise NotImplementedError

    def complete_trip(self, trip_id: str) -> Trip:
        """送达：IN_PROGRESS → COMPLETED，给每条腿结算，司机回到最后一个下车点待命。"""
        raise NotImplementedError

    def cancel_trip(self, trip_id: str, by: Party, reason: str | None = None) -> Trip:
        """取消。许可表说了算：上车之后（IN_PROGRESS）谁都不能取消——车已经在路上，
        这时候要的是"提前结束并按已走里程计费"，那是另一个动作，不是取消。
        """
        raise NotImplementedError

    # ---- 第 4 关：拼车 -----------------------------------------------------

    def join_trip(self, trip_id: str, request: RideRequest) -> Trip:
        """第二位乘客拼上一趟已经匹配的行程。

        两道闸：车上还得有座；绕路（A→P→Q→B 的总长减去 A→B）不超过上限。通过之后
        只是 `Trip.add_leg` 一条腿——状态机、要约机制、司机池都不知道发生过拼车。
        """
        raise NotImplementedError

    # ---- 内部 -------------------------------------------------------------

    def _offer_next(self, trip: Trip, now: datetime) -> Offer | None:
        """给这趟行程找下一位候选并独占他，发出要约。调用方须已持有服务锁。

        排序键的第二项是司机 id：打分相同时若靠字典顺序，测试会飘，线上会出现"同样的
        两位司机，这次派给了谁取决于内存布局"这种没法复现的抱怨。
        """
        raise NotImplementedError

    def _close_offer(self, offer: Offer) -> None:
        """把一张要约从两张表里彻底摘掉。这是它们唯一会缩小的地方，所以只此一个出口。"""
        raise NotImplementedError

    def _reoffer(self, offer: Offer, now: datetime, reason: str) -> None:
        """拒单／超时的统一处理：放人、排除、顺位再发；候选耗尽就把行程明确取消掉。"""
        raise NotImplementedError
