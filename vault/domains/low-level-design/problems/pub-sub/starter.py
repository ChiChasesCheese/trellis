"""进程内发布订阅（Pub-Sub）练习骨架：公开 API 与参考解一模一样，方法体留空。

把每个 `raise NotImplementedError` 换成你自己的实现，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/pub-sub -q`。
内部表示随你选：测试只看公开属性（`size`、`oldest_seq`、`cursor_count`、`lagged_count` 等），
不碰任何下划线开头的东西。
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType

Clock = Callable[[], datetime]
Handler = Callable[["Message"], None]
FailurePolicy = Callable[["Subscription", "Message", BaseException], None]
EMPTY_HEADERS: Mapping[str, object] = MappingProxyType({})
INTERNAL_PREFIX = "$"


def utc_now() -> datetime:
    """默认时钟。"""
    return datetime.now(timezone.utc)


class PubSubError(Exception):
    """本组件所有失败的共同基类。"""


class TopicNotFoundError(PubSubError, KeyError):
    """向一个不存在的主题发布或订阅具体名字时抛出。"""


class UnknownSubscriptionError(PubSubError, KeyError):
    """用一个没有注册过（或已退订）的订阅去读时抛出。"""


class BackpressureError(PubSubError):
    """日志已满且溢出策略不允许丢弃。"""


class BrokerClosedError(PubSubError):
    """broker 关闭之后再发布。"""


class InvalidPatternError(PubSubError, ValueError):
    """通配模式不合法。"""


class OverflowPolicy(Enum):
    """保留日志写满时怎么办。"""

    DROP_OLDEST = "drop_oldest"
    BLOCK = "block"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class Message:
    """一条消息的完整快照。`seq` 是主题内单调递增的位点。"""

    topic: str
    seq: int
    payload: object
    key: str | None = None
    published_at: datetime | None = None
    headers: Mapping[str, object] = field(default_factory=lambda: EMPTY_HEADERS)


@dataclass(frozen=True, slots=True)
class TopicPattern:
    """订阅的主题模式：精确名、`*`（一段）、`#`（零段或多段，只能在末尾）。"""

    pattern: str

    def __post_init__(self) -> None:
        raise NotImplementedError

    @property
    def is_wildcard(self) -> bool:
        raise NotImplementedError

    def matches(self, name: str) -> bool:
        raise NotImplementedError


class Topic:
    """一个主题：一条有界的保留日志，外加每个订阅在这条日志上的游标。"""

    def __init__(self, name: str, capacity: int = 1024,
                 policy: OverflowPolicy = OverflowPolicy.DROP_OLDEST, clock: Clock = utc_now) -> None:
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        raise NotImplementedError

    @property
    def policy(self) -> OverflowPolicy:
        raise NotImplementedError

    @property
    def size(self) -> int:
        """当前保留着多少条消息。"""
        raise NotImplementedError

    @property
    def next_seq(self) -> int:
        """下一条消息将拿到的位点。"""
        raise NotImplementedError

    @property
    def oldest_seq(self) -> int:
        """仍可被读到的最小位点。"""
        raise NotImplementedError

    @property
    def evicted_count(self) -> int:
        raise NotImplementedError

    @property
    def cursor_count(self) -> int:
        """还有几个游标挂在这条日志上。"""
        raise NotImplementedError

    def register(self, sub_id: str, from_beginning: bool = False) -> int:
        raise NotImplementedError

    def unregister(self, sub_id: str) -> None:
        raise NotImplementedError

    def cursor(self, sub_id: str) -> int:
        raise NotImplementedError

    def seek(self, sub_id: str, seq: int) -> int:
        raise NotImplementedError

    def append(self, payload: object, key: str | None = None,
               headers: Mapping[str, object] | None = None, timeout: float | None = None) -> Message:
        raise NotImplementedError

    def read(self, sub_id: str, max_items: int = 1, timeout: float = 0.0) -> tuple[tuple[Message, ...], int]:
        """读一批并推进游标，返回 `(消息, 掉队丢失条数)`。"""
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class Subscription:
    """一个订阅：一个主题模式、每个匹配主题上的游标，以及（push 时）一条投递线程。"""

    def __init__(self, sub_id: str, pattern: TopicPattern, handler: Handler | None = None,
                 from_beginning: bool = False, max_attempts: int = 1, retry_delay: float = 0.0,
                 failure_policy: FailurePolicy | None = None, batch_size: int = 16,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        raise NotImplementedError

    @property
    def id(self) -> str:
        raise NotImplementedError

    @property
    def pattern(self) -> TopicPattern:
        raise NotImplementedError

    @property
    def is_push(self) -> bool:
        raise NotImplementedError

    @property
    def is_closed(self) -> bool:
        raise NotImplementedError

    @property
    def topic_names(self) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def delivered_count(self) -> int:
        raise NotImplementedError

    @property
    def lagged_count(self) -> int:
        """因为日志淘汰而没看到的消息条数。"""
        raise NotImplementedError

    @property
    def failed_count(self) -> int:
        raise NotImplementedError

    def attach(self, topic: Topic) -> None:
        raise NotImplementedError

    def wake(self) -> None:
        raise NotImplementedError

    def poll(self, max_items: int = 1, timeout: float = 0.0) -> tuple[Message, ...]:
        raise NotImplementedError

    def seek(self, topic_name: str, seq: int) -> int:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class Broker:
    """进程内的消息中枢：主题注册表 + 路由 + 死信。"""

    def __init__(self, capacity: int = 1024, policy: OverflowPolicy = OverflowPolicy.DROP_OLDEST,
                 clock: Clock = utc_now, auto_create: bool = True,
                 dead_letter_topic: str = "$dead-letter") -> None:
        raise NotImplementedError

    @property
    def topic_names(self) -> tuple[str, ...]:
        raise NotImplementedError

    @property
    def subscription_count(self) -> int:
        raise NotImplementedError

    @property
    def dead_letter_topic(self) -> str:
        raise NotImplementedError

    def create_topic(self, name: str, capacity: int | None = None,
                     policy: OverflowPolicy | None = None) -> Topic:
        raise NotImplementedError

    def topic(self, name: str) -> Topic:
        raise NotImplementedError

    def publish(self, topic_name: str, payload: object, key: str | None = None,
                headers: Mapping[str, object] | None = None, timeout: float | None = None) -> Message:
        raise NotImplementedError

    def subscribe(self, pattern: str, handler: Handler | None = None, from_beginning: bool = False,
                  max_attempts: int = 1, retry_delay: float = 0.0, dead_letter: bool = False,
                  name: str | None = None, batch_size: int = 16) -> Subscription:
        raise NotImplementedError

    def unsubscribe(self, subscription: Subscription) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


_ = threading  # 实现线程安全时你会用到它
