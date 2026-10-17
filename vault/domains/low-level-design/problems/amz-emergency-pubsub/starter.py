"""应急事件发布订阅：组件订阅应急事件，另一些组件发布；一个订阅者出事不能拖累其他人。
设计：`EmergencyBus` 只管注册表与路由（谁订了什么、给事件编号、记死信）；`Subscription` 拥有"我怎么接收"
——过滤条件、重试次数、计数，一次 `deliver` 把重试和失败都吞在自己里面；`Mailbox` 只在异步订阅者身上出现，
拥有"我什么时候接收"——一条有界优先队列加一个工作线程，严重度高的先出队，慢订阅者只堵自己的信箱。
同步与异步是同一个 `Subscription` 的两种送法，发布路径一行没变；通用的主题日志 / 游标见 [[solution-pub-sub]]。
"""

from __future__ import annotations

import heapq
import threading
from collections import deque
from collections.abc import Callable, Collection
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, IntEnum

Clock = Callable[[], datetime]


def utc_now() -> datetime:
    """默认时钟，带时区；测试里换成固定时钟。"""
    raise NotImplementedError


class EmergencyError(Exception):
    """本组件所有失败的共同基类。"""


class BusClosedError(EmergencyError):
    """总线关闭之后再发布或订阅。"""


class Severity(IntEnum):
    """严重度。用 IntEnum 是因为"至少 WARNING"要能直接比较，这也是优先队列的排序依据。"""

    INFO = 1
    WARNING = 2
    CRITICAL = 3


@dataclass(frozen=True, slots=True)
class EmergencyEvent:
    """发生了什么：冻结的快照，可以同时交给任意多个订阅者、跨线程传递而不加锁。`seq` 由总线编号。"""

    seq: int
    topic: str
    severity: Severity
    message: str
    location: str
    published_at: datetime


Handler = Callable[[EmergencyEvent], None]


class DeadReason(Enum):
    HANDLER_FAILED = "handler_failed"   # 重试用完仍然抛异常
    QUEUE_FULL = "queue_full"           # 异步信箱满了，这条事件被挤掉


@dataclass(frozen=True, slots=True)
class DeadLetter:
    """一次没送到的记录：谁、哪条事件、为什么。运维靠它回看，而不是靠订阅者自己吞掉异常。"""

    subscriber: str
    event: EmergencyEvent
    reason: DeadReason
    attempts: int
    error: str = ""


@dataclass(frozen=True, slots=True)
class SubscriptionStats:
    delivered: int = 0
    failed: int = 0
    dropped: int = 0


class Subscription:
    """一个订阅者：处理函数 + 过滤条件 + 重试次数 + 计数。

    它拥有"一次投递"的全部语义：`deliver` 最多尝试 `max_attempts` 次，任何 `Exception` 都被吞下并
    换成一条 DeadLetter 返回——调用方（发布线程或信箱线程）因此永远不会被订阅者的 bug 打断。
    """

    def __init__(self, name: str, handler: Handler, topics: Collection[str] | None,
                 min_severity: Severity, max_attempts: int) -> None:
        raise NotImplementedError

    def accepts(self, event: EmergencyEvent) -> bool:
        """主题在订阅列表里（None 表示全部），且严重度不低于下限。"""
        raise NotImplementedError

    @property
    def stats(self) -> SubscriptionStats:
        raise NotImplementedError

    def deliver(self, event: EmergencyEvent) -> DeadLetter | None:
        raise NotImplementedError

    def note_dropped(self, event: EmergencyEvent) -> DeadLetter:
        raise NotImplementedError


class Mailbox:
    """异步订阅者的信箱：有界优先队列 + 一个工作线程。

    出队顺序是 (严重度高者优先, 先发布者优先)。满了就挤掉"最不重要且最旧"的那条——可能是新来的
    那条自己；所以 CRITICAL 只会被更晚到的 CRITICAL 挤掉，且只有信箱里全是 CRITICAL 时才会发生。
    `pending` = 排队中 + 正在处理的 1 条，`wait_idle` 靠它回答"现在送完了吗"。
    """

    def __init__(self, sub: Subscription, capacity: int, on_dead: Callable[[DeadLetter], None]) -> None:
        raise NotImplementedError

    @property
    def pending(self) -> int:
        raise NotImplementedError

    def offer(self, event: EmergencyEvent) -> DeadLetter | None:
        """入队；信箱已满时返回被挤掉那条事件的 DeadLetter。"""
        raise NotImplementedError

    def _run(self) -> None:
        raise NotImplementedError

    def wait_idle(self, timeout: float) -> bool:
        raise NotImplementedError

    def close(self, drain: bool) -> None:
        raise NotImplementedError


class EmergencyBus:
    """总线：注册表、事件编号、路由、死信。它不知道处理函数做什么，也不关心送得多快。

    不变量：`publish` 不持锁调用任何订阅者代码（处理函数可以在里面再发布、订阅或退订而不死锁）；
    路由用的是持锁时拍下的订阅快照，所以并发订阅 / 退订不会让一次发布看到半个列表。
    """

    def __init__(self, clock: Clock = utc_now, dead_letter_limit: int = 1000) -> None:
        raise NotImplementedError

    def subscribe(self, handler: Handler, *, topics: Collection[str] | None = None,
                  min_severity: Severity = Severity.INFO, name: str | None = None,
                  max_attempts: int = 1, queue_size: int | None = None) -> Subscription:
        """订阅。`queue_size` 给了就是异步订阅者（自带信箱和线程），不给就在发布线程里同步送。"""
        raise NotImplementedError

    def unsubscribe(self, sub: Subscription) -> bool:
        """退订。信箱里还没送的事件被丢弃（要送完请先 `flush`）。返回之前是否订着。"""
        raise NotImplementedError

    def publish(self, topic: str, severity: Severity, message: str, location: str = "") -> EmergencyEvent:
        """编号、拍快照、路由。返回发布出去的事件；订阅者的失败不会变成这里的异常。"""
        raise NotImplementedError

    def _record_dead(self, dead: DeadLetter) -> None:
        raise NotImplementedError

    @property
    def dead_letters(self) -> tuple[DeadLetter, ...]:
        """死信快照（元组）；只保留最近 `dead_letter_limit` 条，内存有上界。"""
        raise NotImplementedError

    @property
    def subscriber_count(self) -> int:
        raise NotImplementedError

    def flush(self, timeout: float = 5.0) -> bool:
        """等所有异步信箱送完；超时返回 False。同步订阅者在 publish 返回时已经送完。"""
        raise NotImplementedError

    def close(self, drain: bool = True) -> None:
        """关闭：之后不能再发布 / 订阅；`drain=True` 先把信箱里的送完。可重复调用。"""
        raise NotImplementedError
