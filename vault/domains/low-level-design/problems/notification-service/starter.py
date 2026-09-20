"""通知服务（Notification Service）练习骨架：公开 API 与参考解一模一样，方法体留空。

把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/notification-service -q`。
内部表示随你选：测试只看公开属性（`sent_count`、`pending_count`、`dead_letters`、`history`、
`tracked_keys`、`size` 等），不碰任何下划线开头的东西。
"""

from __future__ import annotations

import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Protocol

Clock = Callable[[], datetime]
EMPTY_PARAMS: Mapping[str, object] = MappingProxyType({})
UNLIMITED = 1 << 30


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


class NotificationError(Exception):
    """本服务所有失败的共同基类。"""


class TransientDeliveryError(NotificationError):
    """可重试的失败：超时、502、对端限流。"""


class PermanentDeliveryError(NotificationError):
    """不可重试的失败：地址非法、用户已注销、内容被拒。"""


class UnknownTemplateError(NotificationError, KeyError):
    """请求里引用了一个没有注册过的模板。"""


class Priority(IntEnum):
    """优先级。要能比大小，所以是 `IntEnum`。"""

    MARKETING = 10
    TRANSACTIONAL = 20
    URGENT = 30


class DeliveryStatus(Enum):
    """一次投递尝试的终局。"""

    SENT = "sent"
    QUEUED = "queued"
    DUPLICATE = "duplicate"
    RETRY_SCHEDULED = "retry_scheduled"
    DEAD_LETTERED = "dead_lettered"
    SUPPRESSED_CHANNEL_OFF = "channel_off"
    SUPPRESSED_PRIORITY = "below_min_priority"
    SUPPRESSED_QUIET_HOURS = "quiet_hours"
    SUPPRESSED_RATE_LIMIT = "rate_limited"
    SUPPRESSED_NO_ADDRESS = "no_address"
    SUPPRESSED_NO_PROVIDER = "no_provider"


@dataclass(frozen=True, slots=True)
class Notification:
    """调用方交给服务的一次请求。`notification_id` 由调用方提供，就是幂等键。"""

    notification_id: str
    user_id: str
    template: str
    params: Mapping[str, object] = field(default_factory=lambda: EMPTY_PARAMS)
    priority: Priority = Priority.TRANSACTIONAL
    channels: tuple[str, ...] | None = None


@dataclass(frozen=True, slots=True)
class Envelope:
    """一次请求在某个渠道上物化出来的那封信。"""

    notification_id: str
    user_id: str
    channel: str
    address: str
    title: str
    body: str
    priority: Priority
    attempt: int = 1

    @property
    def idempotency_key(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    """一次投递的结果。"""

    notification_id: str
    user_id: str
    channel: str
    status: DeliveryStatus
    attempts: int = 0
    detail: str = ""

    @property
    def delivered(self) -> bool:
        raise NotImplementedError


class Provider(Protocol):
    """渠道的唯一抽象：一个名字，一个会失败的 `send`。"""

    channel: str

    def send(self, envelope: Envelope) -> str: ...


@dataclass(frozen=True, slots=True)
class UserPreferences:
    """一个用户的收信意愿。"""

    user_id: str
    addresses: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    enabled_channels: frozenset[str] = frozenset()
    min_priority: Mapping[str, Priority] = field(default_factory=lambda: MappingProxyType({}))
    quiet_hours: tuple[int, int] | None = None
    utc_offset_minutes: int = 0

    def local_hour(self, now: datetime) -> int:
        raise NotImplementedError

    def in_quiet_hours(self, now: datetime) -> bool:
        raise NotImplementedError

    def decide(self, channel: str, priority: Priority, now: datetime) -> DeliveryStatus | None:
        """返回抑制原因，或者 `None` 表示放行。"""
        raise NotImplementedError

    @property
    def target_channels(self) -> tuple[str, ...]:
        raise NotImplementedError


class TemplateLibrary:
    """模板库：`(模板名, 渠道) -> (标题, 正文)`，渠道没有专属版本就退回默认版本。"""

    def __init__(self) -> None:
        raise NotImplementedError

    @property
    def template_count(self) -> int:
        raise NotImplementedError

    def register(self, name: str, title: str, body: str, channel: str | None = None) -> None:
        raise NotImplementedError

    def knows(self, name: str) -> bool:
        raise NotImplementedError

    def render(self, name: str, channel: str, params: Mapping[str, object]) -> tuple[str, str]:
        raise NotImplementedError


class RateLimiter:
    """按 key 的滑动窗口计数。窗口空掉的 key 必须被删掉。"""

    def __init__(self, limit: int, window_seconds: float, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    @property
    def limit(self) -> int:
        raise NotImplementedError

    @property
    def tracked_keys(self) -> int:
        raise NotImplementedError

    def allow(self, key: str) -> bool:
        raise NotImplementedError

    def purge(self) -> int:
        raise NotImplementedError


class IdempotencyStore:
    """带过期时间的"这件事做过没有"。`claim` 必须是原子的检查加占坑。"""

    def __init__(self, ttl_seconds: float = 3600.0, clock: Clock = utc_now,
                 capacity: int = 100_000) -> None:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    def claim(self, key: str) -> DeliveryResult | None:
        raise NotImplementedError

    def record(self, key: str, result: DeliveryResult) -> None:
        raise NotImplementedError

    def purge(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """指数退避。"""

    max_attempts: int = 3
    base_delay: float = 1.0
    multiplier: float = 2.0
    max_delay: float = 60.0

    def delay_for(self, attempt: int) -> float:
        raise NotImplementedError


class LaneQueue:
    """分道队列：每个优先级一条 FIFO，从高到低取，但每条道有连续服务配额。"""

    def __init__(self, quota: Mapping[Priority, int] | None = None) -> None:
        raise NotImplementedError

    @property
    def size(self) -> int:
        raise NotImplementedError

    def depth(self, priority: Priority) -> int:
        raise NotImplementedError

    def put(self, priority: Priority, item: object) -> None:
        raise NotImplementedError

    def get(self) -> object | None:
        raise NotImplementedError


class NotificationService:
    """派发器：物化信封 → 过策略 → 排进分道队列 → 按时重试 → 失败进死信。"""

    def __init__(self, clock: Clock = utc_now, retry: RetryPolicy | None = None,
                 rate_limit: tuple[int, float] | None = None, idempotency_ttl: float = 3600.0,
                 lane_quota: Mapping[Priority, int] | None = None, history: int = 1024) -> None:
        raise NotImplementedError

    @property
    def templates(self) -> TemplateLibrary:
        raise NotImplementedError

    @property
    def channels(self) -> tuple[str, ...]:
        raise NotImplementedError

    def register_provider(self, provider: Provider) -> None:
        raise NotImplementedError

    def set_preferences(self, preferences: UserPreferences) -> None:
        raise NotImplementedError

    def preferences_for(self, user_id: str) -> UserPreferences:
        raise NotImplementedError

    @property
    def sent_count(self) -> int:
        raise NotImplementedError

    @property
    def pending_count(self) -> int:
        raise NotImplementedError

    @property
    def dead_letters(self) -> tuple[DeliveryResult, ...]:
        raise NotImplementedError

    @property
    def history(self) -> tuple[DeliveryResult, ...]:
        raise NotImplementedError

    def queue_depth(self, priority: Priority) -> int:
        raise NotImplementedError

    def submit(self, notification: Notification) -> tuple[DeliveryResult, ...]:
        """把一次请求扇出到各个渠道。抑制与重复当场返回结果，其余排队。"""
        raise NotImplementedError

    def run_pending(self, max_items: int = 1) -> int:
        """处理最多 `max_items` 件可运行的事，返回实际处理数。到点的重试先放回队列。"""
        raise NotImplementedError

    def drain(self, limit: int = 10_000) -> int:
        raise NotImplementedError

    def start(self, workers: int = 1, idle_sleep: float = 0.005) -> None:
        raise NotImplementedError

    def stop(self, drain: bool = True, timeout: float = 5.0) -> None:
        raise NotImplementedError


class CollectingProvider:
    """一个把信封收进列表的 provider，给演示和冒烟用。"""

    def __init__(self, channel: str) -> None:
        raise NotImplementedError

    def send(self, envelope: Envelope) -> str:
        raise NotImplementedError


_ = threading  # 实现线程安全时你会用到它
