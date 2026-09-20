"""快递柜（Amazon Locker）——按尺寸分配柜格、一次性取件码、过期回收、多网点就近投递。

核心思路：尺寸不是枚举而是带三维的值对象 `Size`，"装得下"是偏序比较，"最小的空柜"= 在
装得下的尺寸类里按体积取最小——所以第 4 关新增一种尺寸只是多造一个 `Size`，分配逻辑一行不改。
取件码是**持有即凭证**（bearer token）而不是密码：它不绑定任何身份，所以错误尝试只能按
**终端**限流，不能按包裹或账号锁定。`code -> AccessGrant` 这张码表是全系统唯一的索引，取走、
过期、改派三条路径都必须让它变小；到期时间另存一个小顶堆，扫描只看堆顶，弹出时丢弃陈旧条目，
堆同样缩得回去。时间只从注入的 `clock` 进来；`LockerNetwork` 的"就近"是刻意的线性扫描。
"""

from __future__ import annotations

import heapq
import math
import secrets
import threading
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

Clock = Callable[[], datetime]
CodeFactory = Callable[[], str]

# 去掉了 0/O/1/I/L 等易混字符：取件码要在柜机小键盘上被人手输入，可读性是安全性的一部分。
_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
_CODE_LENGTH = 8          # 31**8 ≈ 8.5e11，配合分钟级封锁足以让在线穷举失去意义
_UNIQUE_TRIES = 16        # 生成器重复时的重试次数；撞满说明码空间或生成器有问题


def default_code_factory() -> str:
    """默认取件码生成器：`secrets` 的密码学随机源，不是 `random`。

    做成一个普通可调用对象而不是抽象基类：它只有一个方法、没有状态，测试里换成
    `iter(["AAA", "BBB"]).__next__` 这样的桩即可，"为了扩展"先写一个接口是 Java 习惯。
    """
    return "".join(secrets.choice(_ALPHABET) for _ in range(_CODE_LENGTH))


class LockerError(Exception):
    """本设计全部失败路径的公共基类，调用方可以一次性捕获。"""


class NoLockerAvailableError(LockerError):
    """这个网点没有装得下该包裹的空柜格。"""


class UnknownCodeError(LockerError):
    """码表里没有这个码：输错了、已经用过了，或者有人在猜。"""


class ExpiredCodeError(LockerError):
    """码确实签发过，但已经过了有效期；柜格此刻已经被回收。"""


class WrongPurposeError(LockerError):
    """码是真的，但用错了门：投件码不能用来取件，反之亦然。"""


class TerminalLockedError(LockerError):
    """这台柜机连续被输错太多次，进入冷却期。"""


class LockerStateError(LockerError):
    """柜格状态不允许这个动作（例如往已占用的柜格里再放一件）。"""


@dataclass(frozen=True, slots=True)
class Size:
    """一个尺寸类：名字加三维内空。不可变、可哈希，是值对象（value object）不是实体。

    做成值对象而不是 `Enum`，是因为第 4 关要求"系统没见过的尺寸"能加进来而不动分配逻辑；
    枚举的成员集合在导入时就封死了。
    """

    name: str
    width: int
    depth: int
    height: int

    @property
    def volume(self) -> int:
        return self.width * self.depth * self.height

    @property
    def sort_key(self) -> tuple[int, str]:
        """把"装得下"这个偏序补成全序：先比体积，再比名字保证确定性。"""
        return (self.volume, self.name)

    def accommodates(self, other: Size) -> bool:
        """本尺寸的柜格能不能装下 `other` 尺寸的包裹——三维都不小于才算数。"""
        return (self.width >= other.width and self.depth >= other.depth
                and self.height >= other.height)


SMALL = Size("small", 30, 40, 15)
MEDIUM = Size("medium", 45, 60, 30)
LARGE = Size("large", 60, 80, 45)


class PackageStatus(Enum):
    """包裹在这套系统里的生命周期。`RETURN_TO_SENDER` 是超时回收打的标。"""

    PENDING = "pending"
    IN_LOCKER = "in_locker"
    COLLECTED = "collected"
    RETURN_TO_SENDER = "return_to_sender"


@dataclass(slots=True)
class Package:
    """一件包裹。**故意不是 frozen**：它有身份、有状态迁移，是实体（entity）而不是值对象。

    `Size` 与之相反——两个三维相同的尺寸就是同一个尺寸，所以它 frozen 且可哈希。
    """

    package_id: str
    size: Size
    recipient: str = ""
    status: PackageStatus = PackageStatus.PENDING


class LockerState(Enum):
    """柜格的三种状态。`RESERVED` 是"已留给某次投件、但里面还是空的"——退货流程要用它。"""

    FREE = "free"
    RESERVED = "reserved"
    OCCUPIED = "occupied"


class GrantPurpose(Enum):
    """一个码开门之后允许做什么：取走里面的东西，还是放一件进去。"""

    COLLECT = "collect"
    DROP_OFF = "drop_off"


class EventKind(Enum):
    DEPOSITED = "deposited"
    RESERVED = "reserved"
    COLLECTED = "collected"
    DROPPED_OFF = "dropped_off"
    EXPIRED = "expired"
    CODE_REJECTED = "code_rejected"


@dataclass(frozen=True, slots=True)
class AccessGrant:
    """一次性开门授权：某个码，在到期之前，能把某个柜格打开做某件事。

    `subject` 是包裹号或退货单号——事件与日志用它定位业务对象，不必回头查码表。
    """

    code: str
    locker_id: str
    purpose: GrantPurpose
    subject: str
    issued_at: datetime
    expires_at: datetime

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at


@dataclass(frozen=True, slots=True)
class LockerEvent:
    """柜机上发生的一件事，自带全部上下文，订阅者据此更新自己，不回头读网点的内部字典。

    **不带取件码**：事件会流进日志、监控和推送，凭证跟着走一路就等于把码印在日志里。
    """

    kind: EventKind
    location_id: str
    locker_id: str
    subject: str
    at: datetime


Observer = Callable[[LockerEvent], None]


class Locker:
    """一个柜格：尺寸固定，状态三选一，里面最多一件包裹。

    不变式：`state is OCCUPIED` 当且仅当 `package is not None`；非法迁移一律抛异常而不是
    静默覆盖——"往已占用的柜格再塞一件"在现实里意味着上一件被压在下面永远取不出来。
    """

    def __init__(self, locker_id: str, size: Size) -> None:
        self._locker_id = locker_id
        self._size = size
        self._state = LockerState.FREE
        self._package: Package | None = None

    @property
    def locker_id(self) -> str:
        return self._locker_id

    @property
    def size(self) -> Size:
        return self._size

    @property
    def state(self) -> LockerState:
        return self._state

    @property
    def package(self) -> Package | None:
        """当前占用者；空柜或仅被预留时是 `None`。"""
        return self._package

    def reserve(self) -> None:
        """留给一次还没发生的投件（退货流程）：柜格离开可用池，但里面仍是空的。"""
        if self._state is not LockerState.FREE:
            raise LockerStateError(f"locker {self._locker_id!r} is {self._state.value}")
        self._state = LockerState.RESERVED

    def store(self, package: Package) -> None:
        if self._state is LockerState.OCCUPIED:
            raise LockerStateError(f"locker {self._locker_id!r} already holds a package")
        if not self._size.accommodates(package.size):
            raise LockerStateError(f"package {package.package_id!r} does not fit locker {self._locker_id!r}")
        self._package = package
        self._state = LockerState.OCCUPIED

    def release(self) -> Package | None:
        """清空柜格并交还占用者（预留态的柜格交还 `None`）。"""
        package, self._package = self._package, None
        self._state = LockerState.FREE
        return package


class LockerLocation:
    """一个网点：一组柜格、一张码表、一台键盘的失败计数。所有对外动作都在这里发生。

    不变式：
    1. 码表 `_grants` 只随未完成的授权增长——取走、过期、拒收之后立刻删除，永不积压。
    2. `_free` 是按尺寸类分桶的可用索引，桶空了就把键删掉，不留计数为 0 的幽灵尺寸；
       柜格的真源永远是 `_lockers`，`_free` 只是它的派生视图。
    3. 到期堆 `_deadlines` 只在堆顶到期时被弹；弹出时若码表里已经没有这个码，说明包裹
       已被取走，条目直接丢弃——惰性删除必须有人真的删，否则"到期堆"就成了内存泄漏。
    """

    def __init__(self, location_id: str, lockers: Iterable[Locker], clock: Clock, *,
                 position: tuple[float, float] = (0.0, 0.0),
                 ttl: timedelta = timedelta(days=3),
                 code_factory: CodeFactory = default_code_factory,
                 max_failed_attempts: int = 5,
                 lockout: timedelta = timedelta(minutes=10)) -> None:
        self._location_id = location_id
        self._clock = clock
        self._position = position
        self._ttl = ttl
        self._code_factory = code_factory
        self._max_failed_attempts = max_failed_attempts
        self._lockout = lockout
        self._lock = threading.Lock()
        self._lockers: dict[str, Locker] = {}
        self._free: dict[Size, set[str]] = {}
        self._grants: dict[str, AccessGrant] = {}
        self._deadlines: list[tuple[datetime, str]] = []
        self._failures = 0
        self._locked_until: datetime | None = None
        self._observers: list[Observer] = []
        for locker in lockers:
            self.add_locker(locker)

    # ---- 只读视图：外界看到的一切都是快照或计数，内部集合从不交出去 ----------------

    @property
    def location_id(self) -> str:
        return self._location_id

    @property
    def position(self) -> tuple[float, float]:
        return self._position

    @property
    def locker_count(self) -> int:
        return len(self._lockers)

    @property
    def code_count(self) -> int:
        """码表里还有多少个有效码。测试靠它断言"码用完就消失"，不必去读私有字典。"""
        with self._lock:
            return len(self._grants)

    @property
    def pending_expiry_count(self) -> int:
        """到期堆里还剩多少条目；扫过最后一个到期时间之后必须归零。"""
        with self._lock:
            return len(self._deadlines)

    def free_count(self, size: Size | None = None) -> int:
        """空柜数；给了尺寸就只数装得下它的那些。"""
        with self._lock:
            return sum(len(ids) for s, ids in self._free.items()
                       if size is None or s.accommodates(size))

    def state_of(self, locker_id: str) -> LockerState:
        with self._lock:
            return self._require(locker_id).state

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)

    # ---- 投件与取件 -------------------------------------------------------------

    def add_locker(self, locker: Locker) -> None:
        """装一个新柜格。第 4 关的新尺寸就是从这里进来的：分配逻辑不认识具体尺寸名。"""
        with self._lock:
            if locker.locker_id in self._lockers:
                raise LockerStateError(f"duplicate locker id {locker.locker_id!r}")
            self._lockers[locker.locker_id] = locker
            if locker.state is LockerState.FREE:
                self._mark_free(locker)

    def deposit(self, package: Package) -> AccessGrant:
        """快递员投件：分配最小的能装下的空柜，签发给收件人的一次性取件码。"""
        now = self._clock()
        events: list[LockerEvent] = []
        try:
            with self._lock:
                locker = self._allocate(package.size)
                # 先发码再放件：发码失败时柜格必须回到可用池，否则它会永远占着且没有码能开。
                grant = self._issue_or_release(locker, GrantPurpose.COLLECT, package.package_id, now)
                locker.store(package)
                package.status = PackageStatus.IN_LOCKER
                events.append(self._event(EventKind.DEPOSITED, locker.locker_id, package.package_id, now))
        finally:
            self._publish(events)
        return grant

    def reserve_return(self, return_id: str, size: Size) -> AccessGrant:
        """逆向流程：为一次退货留一个空柜，签发给顾客的一次性**投件**码。

        和 `deposit` 共用同一套分配、同一张码表、同一个到期堆——这正是第 4 关"加退货不动
        原有代码"的兑现方式：只多了一个 `GrantPurpose` 成员和这一个方法。
        """
        now = self._clock()
        events: list[LockerEvent] = []
        try:
            with self._lock:
                locker = self._allocate(size)
                grant = self._issue_or_release(locker, GrantPurpose.DROP_OFF, return_id, now)
                locker.reserve()
                events.append(self._event(EventKind.RESERVED, locker.locker_id, return_id, now))
        finally:
            self._publish(events)
        return grant

    def collect(self, code: str) -> Package:
        """用取件码开门取走包裹。码在这一刻从码表里消失，柜格回到可用池。"""
        now = self._clock()
        events: list[LockerEvent] = []
        try:
            with self._lock:
                grant = self._validate(code, GrantPurpose.COLLECT, now, events)
                locker = self._lockers[grant.locker_id]
                if locker.package is None:  # 不变式被破坏才会走到这里，宁可炸也不要静默返回 None
                    raise LockerStateError(f"locker {locker.locker_id!r} was empty under a COLLECT grant")
                package = locker.release()
                self._burn(grant)
                self._mark_free(locker)
                package.status = PackageStatus.COLLECTED
                events.append(self._event(EventKind.COLLECTED, locker.locker_id, grant.subject, now))
        finally:
            self._publish(events)
        return package

    def drop_off(self, code: str, package: Package) -> AccessGrant:
        """顾客用投件码把退货放进预留的柜格，系统随即签发给快递员的取件码。"""
        now = self._clock()
        events: list[LockerEvent] = []
        try:
            with self._lock:
                grant = self._validate(code, GrantPurpose.DROP_OFF, now, events)
                locker = self._lockers[grant.locker_id]
                # 放不进去（退货比预留的柜格大）时先抛：投件码还没作废，顾客可以换个柜子再来。
                locker.store(package)
                self._burn(grant)
                package.status = PackageStatus.IN_LOCKER
                pickup = self._issue(locker, GrantPurpose.COLLECT, package.package_id, now)
                events.append(self._event(EventKind.DROPPED_OFF, locker.locker_id, package.package_id, now))
        finally:
            self._publish(events)
        return pickup

    def expire_due(self) -> tuple[LockerEvent, ...]:
        """按注入的时钟回收所有已过期的授权：码作废、柜格回池、包裹标为退回寄件人。

        只看堆顶，所以代价是 O(k log n) 而不是 O(码表大小)——一个大网点几千个码，
        每分钟全表扫一遍是典型的"能跑但不该写"的答案。
        """
        now = self._clock()
        events: list[LockerEvent] = []
        try:
            with self._lock:
                while self._deadlines and self._deadlines[0][0] <= now:
                    _, code = heapq.heappop(self._deadlines)
                    grant = self._grants.get(code)
                    if grant is None or not grant.is_expired(now):
                        continue  # 陈旧条目：码已经被取走或被拒收，丢掉即可
                    events.append(self._expire(grant, now))
        finally:
            self._publish(events)
        return tuple(events)

    # ---- 内部：以下方法都假定调用方已持有 `self._lock` ---------------------------

    def _require(self, locker_id: str) -> Locker:
        locker = self._lockers.get(locker_id)
        if locker is None:
            raise LockerStateError(f"unknown locker {locker_id!r}")
        return locker

    def _mark_free(self, locker: Locker) -> None:
        self._free.setdefault(locker.size, set()).add(locker.locker_id)

    def _take_free(self, locker: Locker) -> None:
        bucket = self._free[locker.size]
        bucket.discard(locker.locker_id)
        if not bucket:
            del self._free[locker.size]  # 桶空了就删键，不留计数为 0 的幽灵尺寸

    def _allocate(self, size: Size) -> Locker:
        """最小可容纳优先：在装得下的尺寸类里按 `sort_key` 取最小，再取该类中 id 最小的柜格。

        循环跑的是**尺寸类**（一个网点撑死五六种），不是柜格，所以和柜格总数无关；
        也因此新增一种尺寸不需要改这里的任何一行。
        """
        fitting = [s for s in self._free if s.accommodates(size)]
        if not fitting:
            raise NoLockerAvailableError(
                f"location {self._location_id!r} has no free locker for size {size.name!r}")
        best = min(fitting, key=lambda s: s.sort_key)
        locker = self._lockers[min(self._free[best])]
        self._take_free(locker)
        return locker

    def _issue_or_release(self, locker: Locker, purpose: GrantPurpose, subject: str,
                          now: datetime) -> AccessGrant:
        """发码；发不出来就把柜格还回可用池，绝不留下一个没有码能打开的占用柜格。"""
        try:
            return self._issue(locker, purpose, subject, now)
        except LockerError:
            self._mark_free(locker)
            raise

    def _issue(self, locker: Locker, purpose: GrantPurpose, subject: str,
               now: datetime) -> AccessGrant:
        for _ in range(_UNIQUE_TRIES):
            code = self._code_factory()
            if code not in self._grants:
                break
        else:
            raise LockerError("could not generate a unique code")
        grant = AccessGrant(code=code, locker_id=locker.locker_id, purpose=purpose,
                            subject=subject, issued_at=now, expires_at=now + self._ttl)
        self._grants[code] = grant
        heapq.heappush(self._deadlines, (grant.expires_at, code))
        return grant

    def _validate(self, code: str, purpose: GrantPurpose, now: datetime,
                  events: list[LockerEvent]) -> AccessGrant:
        """校验一个码，但**不**作废它。三种失败只有一种算"可疑"，这是本题最容易写错的地方。

        作废推迟到 `_burn`，由调用方在动作真的成功之后执行：否则一次"退货塞不进柜格"
        就会白白烧掉顾客手里的投件码。
        """
        if self._locked_until is not None:
            if now < self._locked_until:
                raise TerminalLockedError(
                    f"terminal at {self._location_id!r} is locked until {self._locked_until.isoformat()}")
            self._locked_until = None
            self._failures = 0
        grant = self._grants.get(code)
        if grant is None:
            # 唯一可能是"有人在猜"的情况：码表里根本没有它。
            self._failures += 1
            if self._failures >= self._max_failed_attempts:
                self._locked_until = now + self._lockout
            events.append(self._event(EventKind.CODE_REJECTED, "", "", now))
            raise UnknownCodeError("no such pickup code")
        if grant.is_expired(now):
            # 码是真的，只是来晚了——是本人，不是攻击者，不计入失败计数。
            events.append(self._expire(grant, now))
            raise ExpiredCodeError(f"code for {grant.subject!r} expired at {grant.expires_at.isoformat()}")
        if grant.purpose is not purpose:
            raise WrongPurposeError(f"code for {grant.subject!r} is a {grant.purpose.value} code")
        self._failures = 0  # 出示了一个真码就不算可疑，哪怕接下来的动作会失败
        return grant

    def _burn(self, grant: AccessGrant) -> None:
        """动作成功，码就地作废。码表必须在这一刻变小。"""
        del self._grants[grant.code]

    def _expire(self, grant: AccessGrant, now: datetime) -> LockerEvent:
        del self._grants[grant.code]
        locker = self._lockers[grant.locker_id]
        package = locker.release()
        if package is not None:
            package.status = PackageStatus.RETURN_TO_SENDER
        self._mark_free(locker)
        return self._event(EventKind.EXPIRED, locker.locker_id, grant.subject, now)

    def _event(self, kind: EventKind, locker_id: str, subject: str, at: datetime) -> LockerEvent:
        return LockerEvent(kind=kind, location_id=self._location_id, locker_id=locker_id,
                           subject=subject, at=at)

    def _publish(self, events: list[LockerEvent]) -> None:
        """在**锁外**通知订阅者：一个慢订阅者（推送短信、写审计日志）不该把整排柜子堵住。"""
        for event in events:
            for observer in self._observers:
                observer(event)


class LockerNetwork:
    """一批网点。它的职责只有一个：把一次投件送到**装得下且还有空位**的最近网点。

    这里的"最近"是刻意做成朴素的欧氏距离线性扫描：网点数量是几百到几千，一次投件排一次序
    完全够用，而真正的邻近搜索（geohash、R 树、PostGIS）是另一道系统设计题，不是本题的题眼。
    """

    def __init__(self, locations: Iterable[LockerLocation]) -> None:
        self._locations: dict[str, LockerLocation] = {l.location_id: l for l in locations}

    @property
    def location_ids(self) -> tuple[str, ...]:
        return tuple(self._locations)

    def add_location(self, location: LockerLocation) -> None:
        self._locations[location.location_id] = location

    def location(self, location_id: str) -> LockerLocation:
        location = self._locations.get(location_id)
        if location is None:
            raise LockerStateError(f"unknown location {location_id!r}")
        return location

    def by_distance(self, position: tuple[float, float]) -> tuple[LockerLocation, ...]:
        """全部网点，按离 `position` 由近及远；同距离时按 id 保证确定性。"""
        return tuple(sorted(self._locations.values(),
                            key=lambda loc: (math.dist(position, loc.position), loc.location_id)))

    def nearest_with_space(self, position: tuple[float, float], size: Size) -> LockerLocation | None:
        for location in self.by_distance(position):
            if location.free_count(size) > 0:
                return location
        return None

    def deposit_nearest(self, position: tuple[float, float], package: Package) -> tuple[str, AccessGrant]:
        """就近投件。逐个网点真的去 `deposit`，**不**先查后投。

        "有空位"和"投进去"之间隔着别的快递员：先 `free_count` 再 `deposit` 是典型的
        检查与使用竞态（TOCTOU）。这里把 `NoLockerAvailableError` 当成"这家满了，换下一家"，
        原子性留在网点内部的那把锁里，网络层不需要任何跨网点的锁。
        """
        for location in self.by_distance(position):
            try:
                return location.location_id, location.deposit(package)
            except NoLockerAvailableError:
                continue
        raise NoLockerAvailableError(f"no location can take a {package.size.name!r} package")

    def expire_due(self) -> tuple[LockerEvent, ...]:
        events: list[LockerEvent] = []
        for location in self._locations.values():
            events.extend(location.expire_due())
        return tuple(events)


if __name__ == "__main__":
    now = datetime(2026, 3, 1, 9, 0)

    def clock() -> datetime:
        return now

    site = LockerLocation("beijing-01", [Locker("A1", SMALL), Locker("B1", MEDIUM)],
                          clock, position=(0.0, 0.0), ttl=timedelta(days=1))
    site.subscribe(lambda e: print(f"  [{e.kind.value}] {e.locker_id or '-'} {e.subject}"))

    parcel = Package("PKG-1", SMALL, recipient="chi")
    grant = site.deposit(parcel)
    print("deposited into", grant.locker_id, "code length", len(grant.code))
    print("free small lockers:", site.free_count(SMALL), "codes:", site.code_count)

    now = now + timedelta(days=2)
    print("expired:", [e.subject for e in site.expire_due()], "->", parcel.status.value)
    print("codes after sweep:", site.code_count, "heap:", site.pending_expiry_count)
