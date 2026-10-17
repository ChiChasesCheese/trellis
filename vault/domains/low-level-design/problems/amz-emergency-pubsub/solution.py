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
    return datetime.now(timezone.utc)


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
        self.name = name
        self._handler = handler
        self._topics = None if topics is None else frozenset(topics)
        self._min_severity = min_severity
        self._max_attempts = max_attempts
        self._delivered = self._failed = self._dropped = 0
        self._lock = threading.Lock()

    def accepts(self, event: EmergencyEvent) -> bool:
        """主题在订阅列表里（None 表示全部），且严重度不低于下限。"""
        return event.severity >= self._min_severity and (self._topics is None or event.topic in self._topics)

    @property
    def stats(self) -> SubscriptionStats:
        with self._lock:
            return SubscriptionStats(self._delivered, self._failed, self._dropped)

    def deliver(self, event: EmergencyEvent) -> DeadLetter | None:
        error = ""
        for _ in range(self._max_attempts):
            try:
                self._handler(event)
            except Exception as exc:          # 订阅者的任何异常都不许逃出去；BaseException 仍然放行
                error = f"{type(exc).__name__}: {exc}"
                continue
            with self._lock:
                self._delivered += 1
            return None
        with self._lock:
            self._failed += 1
        return DeadLetter(self.name, event, DeadReason.HANDLER_FAILED, self._max_attempts, error)

    def note_dropped(self, event: EmergencyEvent) -> DeadLetter:
        with self._lock:
            self._dropped += 1
        return DeadLetter(self.name, event, DeadReason.QUEUE_FULL, 0)


class Mailbox:
    """异步订阅者的信箱：有界优先队列 + 一个工作线程。

    出队顺序是 (严重度高者优先, 先发布者优先)。满了就挤掉"最不重要且最旧"的那条——可能是新来的
    那条自己；所以 CRITICAL 只会被更晚到的 CRITICAL 挤掉，且只有信箱里全是 CRITICAL 时才会发生。
    `pending` = 排队中 + 正在处理的 1 条，`wait_idle` 靠它回答"现在送完了吗"。
    """

    def __init__(self, sub: Subscription, capacity: int, on_dead: Callable[[DeadLetter], None]) -> None:
        self._sub = sub
        self._capacity = capacity
        self._on_dead = on_dead
        self._heap: list[tuple[int, int, EmergencyEvent]] = []   # (-severity, seq, event)
        self._in_flight = 0
        self._closed = False
        self._cond = threading.Condition()
        self._thread = threading.Thread(target=self._run, name=f"mailbox-{sub.name}", daemon=True)
        self._thread.start()

    @property
    def pending(self) -> int:
        with self._cond:
            return len(self._heap) + self._in_flight

    def offer(self, event: EmergencyEvent) -> DeadLetter | None:
        """入队；信箱已满时返回被挤掉那条事件的 DeadLetter。"""
        with self._cond:
            if self._closed:
                return None
            dead: DeadLetter | None = None
            if len(self._heap) >= self._capacity:
                worst = max(self._heap, key=lambda item: (item[0], -item[1]))
                if (worst[0], -worst[1]) < (-event.severity, -event.seq):
                    return self._sub.note_dropped(event)         # 新来的就是最不重要的
                self._heap.remove(worst)
                heapq.heapify(self._heap)
                dead = self._sub.note_dropped(worst[2])
            heapq.heappush(self._heap, (-event.severity, event.seq, event))
            self._cond.notify_all()
            return dead

    def _run(self) -> None:
        while True:
            with self._cond:
                while not self._heap and not self._closed:
                    self._cond.wait()
                if not self._heap:
                    return
                _, _, event = heapq.heappop(self._heap)
                self._in_flight = 1
            dead = self._sub.deliver(event)                      # 在锁外：慢处理不挡 offer
            if dead is not None:
                self._on_dead(dead)
            with self._cond:
                self._in_flight = 0
                self._cond.notify_all()

    def wait_idle(self, timeout: float) -> bool:
        with self._cond:
            return self._cond.wait_for(lambda: not self._heap and not self._in_flight, timeout)

    def close(self, drain: bool) -> None:
        with self._cond:
            self._closed = True
            if not drain:
                self._heap.clear()
            self._cond.notify_all()
        if drain and threading.current_thread() is not self._thread:
            self._thread.join(timeout=5)         # 只有"送完再关"才值得等；丢弃式关闭立即返回


class EmergencyBus:
    """总线：注册表、事件编号、路由、死信。它不知道处理函数做什么，也不关心送得多快。

    不变量：`publish` 不持锁调用任何订阅者代码（处理函数可以在里面再发布、订阅或退订而不死锁）；
    路由用的是持锁时拍下的订阅快照，所以并发订阅 / 退订不会让一次发布看到半个列表。
    """

    def __init__(self, clock: Clock = utc_now, dead_letter_limit: int = 1000) -> None:
        self._clock = clock
        self._subs: dict[Subscription, Mailbox | None] = {}
        self._dead: deque[DeadLetter] = deque(maxlen=dead_letter_limit)
        self._seq = 0
        self._counter = 0
        self._closed = False
        self._lock = threading.Lock()

    def subscribe(self, handler: Handler, *, topics: Collection[str] | None = None,
                  min_severity: Severity = Severity.INFO, name: str | None = None,
                  max_attempts: int = 1, queue_size: int | None = None) -> Subscription:
        """订阅。`queue_size` 给了就是异步订阅者（自带信箱和线程），不给就在发布线程里同步送。"""
        if max_attempts < 1 or (queue_size is not None and queue_size < 1):
            raise ValueError("max_attempts and queue_size must be at least 1")
        with self._lock:
            if self._closed:
                raise BusClosedError("bus is closed")
            self._counter += 1
            sub = Subscription(name or f"sub-{self._counter}", handler, topics, min_severity, max_attempts)
            self._subs[sub] = None if queue_size is None else Mailbox(sub, queue_size, self._record_dead)
            return sub

    def unsubscribe(self, sub: Subscription) -> bool:
        """退订。信箱里还没送的事件被丢弃（要送完请先 `flush`）。返回之前是否订着。"""
        with self._lock:
            if sub not in self._subs:
                return False
            box = self._subs.pop(sub)
        if box is not None:
            box.close(drain=False)
        return True

    def publish(self, topic: str, severity: Severity, message: str, location: str = "") -> EmergencyEvent:
        """编号、拍快照、路由。返回发布出去的事件；订阅者的失败不会变成这里的异常。"""
        if not topic:
            raise ValueError("topic must not be empty")
        with self._lock:
            if self._closed:
                raise BusClosedError("bus is closed")
            self._seq += 1
            event = EmergencyEvent(self._seq, topic, severity, message, location, self._clock())
            targets = [(sub, box) for sub, box in self._subs.items() if sub.accepts(event)]
        for sub, box in targets:
            dead = sub.deliver(event) if box is None else box.offer(event)
            if dead is not None:
                self._record_dead(dead)
        return event

    def _record_dead(self, dead: DeadLetter) -> None:
        with self._lock:
            self._dead.append(dead)

    @property
    def dead_letters(self) -> tuple[DeadLetter, ...]:
        """死信快照（元组）；只保留最近 `dead_letter_limit` 条，内存有上界。"""
        with self._lock:
            return tuple(self._dead)

    @property
    def subscriber_count(self) -> int:
        with self._lock:
            return len(self._subs)

    def flush(self, timeout: float = 5.0) -> bool:
        """等所有异步信箱送完；超时返回 False。同步订阅者在 publish 返回时已经送完。"""
        with self._lock:
            boxes = [box for box in self._subs.values() if box is not None]
        return all(box.wait_idle(timeout) for box in boxes)

    def close(self, drain: bool = True) -> None:
        """关闭：之后不能再发布 / 订阅；`drain=True` 先把信箱里的送完。可重复调用。"""
        with self._lock:
            self._closed = True
            boxes = [box for box in self._subs.values() if box is not None]
        for box in boxes:
            box.close(drain)


if __name__ == "__main__":
    bus = EmergencyBus()
    bus.subscribe(lambda e: print("消防队收到", e.topic, e.severity.name), topics={"fire"}, name="fire-dept")
    bus.subscribe(lambda e: 1 / 0, name="buggy")                       # 它出错，不影响别人
    bus.subscribe(lambda e: print("指挥中心收到", e.message), min_severity=Severity.CRITICAL, name="hq")
    bus.publish("fire", Severity.CRITICAL, "三号楼起火", "B3")
    print([d.subscriber for d in bus.dead_letters])
