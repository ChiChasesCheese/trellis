"""快递柜（Amazon Locker）——练习骨架：公开 API 与参考解一致，方法体全部待补。

把每个 `raise NotImplementedError` 换成你自己的实现即可；内部表示随你选（码表用什么结构、
到期怎么扫），测试只断言公开行为与只读计数（`code_count`、`pending_expiry_count`、
`free_count`），不会碰任何私有属性。
"""

from __future__ import annotations

import secrets
import threading
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

Clock = Callable[[], datetime]
CodeFactory = Callable[[], str]

_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
_CODE_LENGTH = 8
_UNIQUE_TRIES = 16


def default_code_factory() -> str:
    """默认取件码生成器：密码学随机源，不用 `random`。"""
    raise NotImplementedError


class LockerError(Exception):
    """本设计全部失败路径的公共基类。"""


class NoLockerAvailableError(LockerError):
    """这个网点没有装得下该包裹的空柜格。"""


class UnknownCodeError(LockerError):
    """码表里没有这个码。"""


class ExpiredCodeError(LockerError):
    """码签发过，但已经过期。"""


class WrongPurposeError(LockerError):
    """码是真的，但用错了门。"""


class TerminalLockedError(LockerError):
    """柜机连续被输错太多次，进入冷却期。"""


class LockerStateError(LockerError):
    """柜格状态不允许这个动作。"""


@dataclass(frozen=True, slots=True)
class Size:
    """一个尺寸类：名字加三维内空；值对象，可哈希。"""

    name: str
    width: int
    depth: int
    height: int

    @property
    def volume(self) -> int:
        raise NotImplementedError

    @property
    def sort_key(self) -> tuple[int, str]:
        """把"装得下"这个偏序补成全序。"""
        raise NotImplementedError

    def accommodates(self, other: Size) -> bool:
        """本尺寸的柜格能不能装下 `other` 尺寸的包裹。"""
        raise NotImplementedError


SMALL = Size("small", 30, 40, 15)
MEDIUM = Size("medium", 45, 60, 30)
LARGE = Size("large", 60, 80, 45)


class PackageStatus(Enum):
    PENDING = "pending"
    IN_LOCKER = "in_locker"
    COLLECTED = "collected"
    RETURN_TO_SENDER = "return_to_sender"


@dataclass(slots=True)
class Package:
    """一件包裹：有身份、有状态迁移，所以不是 frozen。"""

    package_id: str
    size: Size
    recipient: str = ""
    status: PackageStatus = PackageStatus.PENDING


class LockerState(Enum):
    FREE = "free"
    RESERVED = "reserved"
    OCCUPIED = "occupied"


class GrantPurpose(Enum):
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
    """一次性开门授权。`subject` 是包裹号或退货单号。"""

    code: str
    locker_id: str
    purpose: GrantPurpose
    subject: str
    issued_at: datetime
    expires_at: datetime

    def is_expired(self, now: datetime) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class LockerEvent:
    """柜机上发生的一件事；刻意不带取件码。"""

    kind: EventKind
    location_id: str
    locker_id: str
    subject: str
    at: datetime


Observer = Callable[[LockerEvent], None]


class Locker:
    """一个柜格：尺寸固定，状态三选一，里面最多一件包裹。"""

    def __init__(self, locker_id: str, size: Size) -> None:
        raise NotImplementedError

    @property
    def locker_id(self) -> str:
        raise NotImplementedError

    @property
    def size(self) -> Size:
        raise NotImplementedError

    @property
    def state(self) -> LockerState:
        raise NotImplementedError

    @property
    def package(self) -> Package | None:
        """当前占用者；空柜或仅被预留时是 `None`。"""
        raise NotImplementedError

    def reserve(self) -> None:
        """留给一次还没发生的投件：离开可用池，里面仍是空的。"""
        raise NotImplementedError

    def store(self, package: Package) -> None:
        raise NotImplementedError

    def release(self) -> Package | None:
        """清空柜格并交还占用者。"""
        raise NotImplementedError


class LockerLocation:
    """一个网点：一组柜格、一张码表、一台键盘的失败计数。"""

    def __init__(self, location_id: str, lockers: Iterable[Locker], clock: Clock, *,
                 position: tuple[float, float] = (0.0, 0.0),
                 ttl: timedelta = timedelta(days=3),
                 code_factory: CodeFactory = default_code_factory,
                 max_failed_attempts: int = 5,
                 lockout: timedelta = timedelta(minutes=10)) -> None:
        raise NotImplementedError

    @property
    def location_id(self) -> str:
        raise NotImplementedError

    @property
    def position(self) -> tuple[float, float]:
        raise NotImplementedError

    @property
    def locker_count(self) -> int:
        raise NotImplementedError

    @property
    def code_count(self) -> int:
        """码表里还有多少个有效码。"""
        raise NotImplementedError

    @property
    def pending_expiry_count(self) -> int:
        """到期索引里还剩多少条目；扫过最后一个到期时间之后必须归零。"""
        raise NotImplementedError

    def free_count(self, size: Size | None = None) -> int:
        """空柜数；给了尺寸就只数装得下它的那些。"""
        raise NotImplementedError

    def state_of(self, locker_id: str) -> LockerState:
        raise NotImplementedError

    def subscribe(self, observer: Observer) -> None:
        raise NotImplementedError

    def add_locker(self, locker: Locker) -> None:
        """装一个新柜格，尺寸可以是系统此前没见过的。"""
        raise NotImplementedError

    def deposit(self, package: Package) -> AccessGrant:
        """快递员投件：分配最小的能装下的空柜，签发一次性取件码。"""
        raise NotImplementedError

    def reserve_return(self, return_id: str, size: Size) -> AccessGrant:
        """逆向流程：为一次退货留一个空柜，签发一次性投件码。"""
        raise NotImplementedError

    def collect(self, code: str) -> Package:
        """用取件码开门取走包裹。"""
        raise NotImplementedError

    def drop_off(self, code: str, package: Package) -> AccessGrant:
        """顾客用投件码把退货放进预留的柜格，随即签发给快递员的取件码。"""
        raise NotImplementedError

    def expire_due(self) -> tuple[LockerEvent, ...]:
        """按注入的时钟回收所有已过期的授权。"""
        raise NotImplementedError


class LockerNetwork:
    """一批网点：把一次投件送到装得下且还有空位的最近网点。"""

    def __init__(self, locations: Iterable[LockerLocation]) -> None:
        raise NotImplementedError

    @property
    def location_ids(self) -> tuple[str, ...]:
        raise NotImplementedError

    def add_location(self, location: LockerLocation) -> None:
        raise NotImplementedError

    def location(self, location_id: str) -> LockerLocation:
        raise NotImplementedError

    def by_distance(self, position: tuple[float, float]) -> tuple[LockerLocation, ...]:
        """全部网点，按离 `position` 由近及远。"""
        raise NotImplementedError

    def nearest_with_space(self, position: tuple[float, float], size: Size) -> LockerLocation | None:
        raise NotImplementedError

    def deposit_nearest(self, position: tuple[float, float], package: Package) -> tuple[str, AccessGrant]:
        """就近投件；逐个网点真的去投，不先查后投。"""
        raise NotImplementedError

    def expire_due(self) -> tuple[LockerEvent, ...]:
        raise NotImplementedError
