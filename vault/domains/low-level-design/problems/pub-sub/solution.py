"""进程内发布订阅（Pub-Sub）：主题是一条有界的保留日志，订阅者是这条日志上的一个游标。
设计：`Broker` 只管注册表与路由，`Topic` 拥有日志和所有游标、守着唯一一把锁，`Subscription`
拥有"我读到哪了"和（push 时）一条投递线程，`Message` 是冻结的事件对象。
投递模型选的是拉（pull）——订阅者各有游标，于是可以重放、可以从任意位点开始，慢订阅者只拖慢
自己；push 只是在拉之上包一条线程。日志满时的溢出策略（丢最旧／阻塞／拒绝）是主题的属性，
写在一个地方、可观测、可测试。通配订阅与死信建在这两件事之上，没有动投递路径一行。
"""

from __future__ import annotations

import itertools
import threading
import time
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType

# 时钟从外部注入（测试里换成固定时钟）；处理器就是"收下一条消息"的函数——只有一个方法的
# 角色不值得一个抽象基类。失败策略同理：默认只计数，死信投递也只是另一个函数。
Clock = Callable[[], datetime]
Handler = Callable[["Message"], None]
FailurePolicy = Callable[["Subscription", "Message", BaseException], None]
EMPTY_HEADERS: Mapping[str, object] = MappingProxyType({})
INTERNAL_PREFIX = "$"


def utc_now() -> datetime:
    """默认时钟。带时区，消息时间因此可以跨机器比较。"""
    return datetime.now(timezone.utc)


class PubSubError(Exception):
    """本组件所有失败的共同基类，调用方可以只捕获这一个。"""


class TopicNotFoundError(PubSubError, KeyError):
    """向一个不存在的主题发布或订阅具体名字时抛出。"""


class UnknownSubscriptionError(PubSubError, KeyError):
    """用一个没有在该主题上注册过（或已经退订）的订阅去读时抛出。"""


class BackpressureError(PubSubError):
    """日志已满且溢出策略不允许丢弃：REJECT 立即抛，BLOCK 等到超时抛。"""


class BrokerClosedError(PubSubError):
    """broker 关闭之后再发布。"""


class InvalidPatternError(PubSubError, ValueError):
    """通配模式不合法（空段、`#` 不在末尾）。"""


class OverflowPolicy(Enum):
    """保留日志写满时怎么办。三种选择的代价必须当场说清，不能留成"以后再说"。"""

    DROP_OLDEST = "drop_oldest"   # 发布者永不阻塞；落后的订阅者丢掉最旧的消息，丢多少可查
    BLOCK = "block"               # 一条不丢，代价是最慢的订阅者会反压住所有发布者
    REJECT = "reject"             # 发布者立刻收到 BackpressureError，自己决定降级或重试


@dataclass(frozen=True, slots=True)
class Message:
    """一条消息的完整快照：冻结，因此可以同时交给任意多个订阅者、跨线程传递而不加锁。

    `seq` 是主题内单调递增的位点（offset），既是排序依据，也是重放的坐标。
    """

    topic: str
    seq: int
    payload: object
    key: str | None = None
    published_at: datetime | None = None
    headers: Mapping[str, object] = field(default_factory=lambda: EMPTY_HEADERS)


@dataclass(frozen=True, slots=True)
class TopicPattern:
    """订阅的主题模式：`orders.created` 精确匹配，`orders.*` 匹配一段，`orders.#` 匹配零段或多段。

    以 `$` 开头的是内部主题（死信），通配一律不匹配它——否则订了 `#` 的消费者会把自己投递
    失败产生的死信再吃一遍，失败一次就变成死循环。
    """

    pattern: str

    def __post_init__(self) -> None:
        segments = self.pattern.split(".")
        if not self.pattern or any(s == "" for s in segments):
            raise InvalidPatternError(f"empty segment in pattern {self.pattern!r}")
        if any(s == "#" for s in segments[:-1]):
            raise InvalidPatternError(f"'#' must be the last segment: {self.pattern!r}")

    @property
    def is_wildcard(self) -> bool:
        return "*" in self.pattern.split(".") or "#" in self.pattern.split(".")

    def matches(self, name: str) -> bool:
        if name == self.pattern:
            return True
        if not self.is_wildcard or name.startswith(INTERNAL_PREFIX):
            return False
        return _match(tuple(self.pattern.split(".")), tuple(name.split(".")))


def _match(pattern: tuple[str, ...], name: tuple[str, ...]) -> bool:
    """逐段匹配。`#` 只能出现在最后一段，所以递归一定收敛，不需要回溯。"""
    if not pattern:
        return not name
    if pattern[0] == "#":
        return True
    if not name:
        return False
    if pattern[0] == "*" or pattern[0] == name[0]:
        return _match(pattern[1:], name[1:])
    return False


class Topic:
    """一个主题：一条有界的保留日志，外加每个订阅在这条日志上的游标。

    它拥有两条不变量：`oldest_seq + size == next_seq`（日志是 seq 空间上的一段连续区间），
    以及 `size <= capacity`（内存有上限，这是一个进程内组件，无界增长就是事故）。
    所有游标也归它管——谁在读我的日志、读到哪了，只有日志自己知道才可能实现 BLOCK 反压。
    """

    def __init__(self, name: str, capacity: int = 1024,
                 policy: OverflowPolicy = OverflowPolicy.DROP_OLDEST, clock: Clock = utc_now) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        self._name = name
        self._capacity = capacity
        self._policy = policy
        self._clock = clock
        self._log: deque[Message] = deque()
        self._start_seq = 0
        self._next_seq = 0
        self._cursors: dict[str, int] = {}
        self._evicted = 0
        self._closed = False
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    @property
    def name(self) -> str:
        return self._name

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def policy(self) -> OverflowPolicy:
        return self._policy

    @property
    def size(self) -> int:
        """当前保留着多少条消息。公开成属性，测试才能断言"日志没有无界增长"。"""
        with self._lock:
            return len(self._log)

    @property
    def next_seq(self) -> int:
        """下一条消息将拿到的位点，也等于"至今发布过多少条"。"""
        with self._lock:
            return self._next_seq

    @property
    def oldest_seq(self) -> int:
        """仍可被读到的最小位点。它一旦超过某个游标，那个订阅者就已经掉队了。"""
        with self._lock:
            return self._start_seq

    @property
    def evicted_count(self) -> int:
        with self._lock:
            return self._evicted

    @property
    def cursor_count(self) -> int:
        """还有几个游标挂在这条日志上。退订必须让它减一，否则 BLOCK 策略会被幽灵游标永久卡死。"""
        with self._lock:
            return len(self._cursors)

    def register(self, sub_id: str, from_beginning: bool = False) -> int:
        """挂一个游标上来。默认只收新消息；`from_beginning=True` 则从保留窗口的头开始重放。"""
        with self._lock:
            start = self._start_seq if from_beginning else self._next_seq
            self._cursors[sub_id] = start
            return start

    def unregister(self, sub_id: str) -> None:
        """摘掉游标，并叫醒被它挡住的发布者——这是 BLOCK 策略下最容易漏掉的一步。"""
        with self._not_full:
            self._cursors.pop(sub_id, None)
            self._not_full.notify_all()

    def cursor(self, sub_id: str) -> int:
        with self._lock:
            try:
                return self._cursors[sub_id]
            except KeyError:
                raise UnknownSubscriptionError(f"{sub_id} is not subscribed to {self._name}") from None

    def seek(self, sub_id: str, seq: int) -> int:
        """把游标移到某个位点（夹到保留窗口内）——重放靠的就是这一个方法。"""
        with self._lock:
            if sub_id not in self._cursors:
                raise UnknownSubscriptionError(f"{sub_id} is not subscribed to {self._name}")
            target = max(self._start_seq, min(seq, self._next_seq))
            self._cursors[sub_id] = target
            return target

    def append(self, payload: object, key: str | None = None,
               headers: Mapping[str, object] | None = None, timeout: float | None = None) -> Message:
        """追加一条消息并返回它。满了怎么办完全由本主题的溢出策略决定。"""
        with self._not_full:
            if self._closed:
                raise BrokerClosedError(f"topic {self._name} is closed")
            if len(self._log) >= self._capacity:
                self._make_room(timeout)
            message = Message(topic=self._name, seq=self._next_seq, payload=payload, key=key,
                              published_at=self._clock(),
                              headers=MappingProxyType(dict(headers)) if headers else EMPTY_HEADERS)
            self._log.append(message)
            self._next_seq += 1
            self._not_empty.notify_all()
            return message

    def _make_room(self, timeout: float | None) -> None:
        """腾一个位置出来。调用时已持锁，且日志确实已满。

        BLOCK 的等待条件不是"日志变短"（没人会替它变短），而是**最慢的游标越过了队头**——
        只有队头被所有订阅者读过，淘汰它才不算丢消息。这一条是整个反压语义的定义，
        BLOCK 与 REJECT 共用它：前者等，后者立刻放弃。DROP_OLDEST 则根本不问，直接淘汰。
        """
        if self._policy is OverflowPolicy.DROP_OLDEST:
            while len(self._log) >= self._capacity:
                self._evict_head()
            return
        if self._policy is OverflowPolicy.BLOCK:
            deadline = None if timeout is None else time.monotonic() + timeout
            while self._min_cursor() <= self._start_seq:
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    raise BackpressureError(f"topic {self._name} is full ({self._capacity})")
                self._not_full.wait(remaining)
                if self._closed:
                    raise BrokerClosedError(f"topic {self._name} is closed")
        while len(self._log) >= self._capacity and self._min_cursor() > self._start_seq:
            self._evict_head()
        if len(self._log) >= self._capacity:
            raise BackpressureError(f"topic {self._name} is full ({self._capacity})")

    def _evict_head(self) -> None:
        """把队头移出保留窗口。调用时已持锁。"""
        self._log.popleft()
        self._start_seq += 1
        self._evicted += 1

    def _min_cursor(self) -> int:
        """最慢的游标。一个游标都没有时视为"全都读完了"，否则没人消费的主题会把发布者永久挂住。"""
        return min(self._cursors.values(), default=self._next_seq)

    def read(self, sub_id: str, max_items: int = 1, timeout: float = 0.0) -> tuple[tuple[Message, ...], int]:
        """读一批并推进游标，返回 `(消息, 掉队丢失条数)`。

        游标在读到的瞬间就前进（自动提交）。手动提交能做到"处理成功才前进"、从而给出至少一次
        语义，代价是要多一个 `commit(seq)` 接口和一份未提交区间——进程内组件用不到，见题解。
        """
        with self._not_empty:
            deadline = time.monotonic() + timeout if timeout > 0 else None
            while True:
                try:
                    cursor = self._cursors[sub_id]
                except KeyError:
                    raise UnknownSubscriptionError(f"{sub_id} is not subscribed to {self._name}") from None
                if cursor < self._next_seq or self._closed or deadline is None:
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not self._not_empty.wait(remaining):
                    break
            lost = 0
            if cursor < self._start_seq:
                lost = self._start_seq - cursor
                cursor = self._start_seq
            offset = cursor - self._start_seq
            batch = tuple(itertools.islice(self._log, offset, offset + max_items))
            self._cursors[sub_id] = cursor + len(batch)
            if batch:
                self._not_full.notify_all()
            return batch, lost

    def close(self) -> None:
        """叫醒所有等待者并拒绝后续写入。日志本身留着——关闭不是清空。"""
        with self._lock:
            self._closed = True
            self._not_empty.notify_all()
            self._not_full.notify_all()


class Subscription:
    """一个订阅：一个主题模式、它在每个匹配主题上的游标，以及（push 时）一条投递线程。

    它拥有的不变量是顺序：**同一主题的消息，按发布顺序、由唯一一条线程交给同一个订阅者**。
    跨主题不保证顺序，跨订阅者也不保证——这两句必须主动说出口。
    """

    def __init__(self, sub_id: str, pattern: TopicPattern, handler: Handler | None = None,
                 from_beginning: bool = False, max_attempts: int = 1, retry_delay: float = 0.0,
                 failure_policy: FailurePolicy | None = None, batch_size: int = 16,
                 sleep: Callable[[float], None] = time.sleep) -> None:
        if max_attempts < 1:
            raise ValueError(f"max_attempts must be ≥ 1, got {max_attempts}")
        self._id = sub_id
        self._pattern = pattern
        self._handler = handler
        self._from_beginning = from_beginning
        self._max_attempts = max_attempts
        self._retry_delay = retry_delay
        self._failure_policy = failure_policy
        self._batch_size = batch_size
        self._sleep = sleep
        self._topics: tuple[Topic, ...] = ()
        self._delivered = 0
        self._lagged = 0
        self._failed = 0
        self._closed = False
        self._state_lock = threading.Lock()
        self._wakeup = threading.Event()
        self._worker: threading.Thread | None = None
        if handler is not None:
            self._worker = threading.Thread(target=self._run, name=f"sub-{sub_id}", daemon=True)
            self._worker.start()

    @property
    def id(self) -> str:
        return self._id

    @property
    def pattern(self) -> TopicPattern:
        return self._pattern

    @property
    def is_push(self) -> bool:
        return self._handler is not None

    @property
    def is_closed(self) -> bool:
        return self._closed

    @property
    def topic_names(self) -> tuple[str, ...]:
        """快照，不是内部元组本身——调用方拿到手的东西不该能改写订阅的状态。"""
        return tuple(t.name for t in self._topics)

    @property
    def delivered_count(self) -> int:
        with self._state_lock:
            return self._delivered

    @property
    def lagged_count(self) -> int:
        """因为日志淘汰而**没看到**的消息条数。丢弃必须可观测，否则 DROP_OLDEST 就是静默丢数据。"""
        with self._state_lock:
            return self._lagged

    @property
    def failed_count(self) -> int:
        """重试用尽后仍然失败、交给失败策略处理的消息条数。"""
        with self._state_lock:
            return self._failed

    def attach(self, topic: Topic) -> None:
        """broker 在订阅时、以及此后每次建出匹配的新主题时调用。整体替换元组，读路径不加锁。"""
        with self._state_lock:
            if self._closed or any(t is topic for t in self._topics):
                return
            topic.register(self._id, self._from_beginning)
            self._topics = (*self._topics, topic)
        self.wake()

    def wake(self) -> None:
        """门铃：告诉投递线程"有新东西了"，免得它靠轮询发现。"""
        self._wakeup.set()

    def poll(self, max_items: int = 1, timeout: float = 0.0) -> tuple[Message, ...]:
        """拉模式的入口。轮流看每个匹配主题，返回一批消息；`timeout` 内没有就返回空。"""
        if self._handler is not None:
            raise PubSubError(f"subscription {self._id} is push-based; it has no poll()")
        batch = self._drain_once(max_items)
        if batch or timeout <= 0:
            return batch
        self._wakeup.wait(timeout)
        self._wakeup.clear()
        return self._drain_once(max_items)

    def seek(self, topic_name: str, seq: int) -> int:
        """重放：把某个主题上的游标移回去。这是拉模型白送的能力，推模型做不到。"""
        for topic in self._topics:
            if topic.name == topic_name:
                position = topic.seek(self._id, seq)
                self.wake()
                return position
        raise TopicNotFoundError(f"{self._id} is not subscribed to {topic_name}")

    def _drain_once(self, max_items: int) -> tuple[Message, ...]:
        collected: list[Message] = []
        for topic in self._topics:
            if len(collected) >= max_items:
                break
            messages, lost = topic.read(self._id, max_items - len(collected))
            with self._state_lock:
                self._lagged += lost
                self._delivered += len(messages)
            collected.extend(messages)
        return tuple(collected)

    def _run(self) -> None:
        """投递线程：读一批、逐条回调、没东西就在门铃上等一会儿。

        关闭契约与日志框架的异步 handler 一致：`close()` 之后线程会把**已经发布**的消息
        全部投完才退出，它不承诺和仍在运行的发布者赛跑。
        """
        while True:
            progressed = False
            for topic in self._topics:
                messages, lost = topic.read(self._id, self._batch_size)
                if lost:
                    with self._state_lock:
                        self._lagged += lost
                for message in messages:
                    self._deliver(message)
                    progressed = True
            if progressed:
                continue
            if self._closed:
                return
            self._wakeup.wait(0.02)
            self._wakeup.clear()

    def _deliver(self, message: Message) -> None:
        """一条消息的投递：重试若干次，仍然失败就交给失败策略。

        订阅者抛出的异常**绝不能**冒泡到这里之外——一个坏订阅者不许拖垮别人，也不许
        杀掉自己的投递线程，否则它后面的消息会永远停在游标上。
        """
        assert self._handler is not None
        last: BaseException | None = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                self._handler(message)
                with self._state_lock:
                    self._delivered += 1
                return
            except Exception as exc:  # noqa: BLE001 — 订阅者的异常是数据，不是控制流
                last = exc
                if attempt < self._max_attempts and self._retry_delay > 0:
                    self._sleep(self._retry_delay * attempt)
        with self._state_lock:
            self._failed += 1
        if self._failure_policy is not None and last is not None:
            try:
                self._failure_policy(self, message, last)
            except Exception:  # noqa: BLE001 — 死信也可能失败，同样不许炸掉投递线程
                pass

    def close(self) -> None:
        """排空已发布的消息、汇合投递线程、摘掉所有游标。摘游标这一步决定了内存不会泄漏。"""
        with self._state_lock:
            if self._closed:
                return
            self._closed = True
            topics = self._topics
        self._wakeup.set()
        if self._worker is not None:
            self._worker.join(timeout=5.0)
        for topic in topics:
            topic.unregister(self._id)
        with self._state_lock:
            self._topics = ()


class Broker:
    """进程内的消息中枢：主题注册表 + 路由 + 死信。它**不**拥有日志，也不拥有游标。

    这是一个进程内的事件总线，不是分布式消息系统——没有网络、没有副本、没有持久化，
    进程一死消息就没了。它与 Kafka 的相同之处只有"保留日志 + 消费者位点"这一个模型。
    """

    def __init__(self, capacity: int = 1024, policy: OverflowPolicy = OverflowPolicy.DROP_OLDEST,
                 clock: Clock = utc_now, auto_create: bool = True,
                 dead_letter_topic: str = "$dead-letter") -> None:
        self._capacity = capacity
        self._policy = policy
        self._clock = clock
        self._auto_create = auto_create
        self._dead_letter_topic = dead_letter_topic
        self._topics: dict[str, Topic] = {}
        self._subscriptions: dict[str, Subscription] = {}
        self._next_id = itertools.count(1)
        self._closed = False
        self._lock = threading.RLock()
        self.create_topic(dead_letter_topic)

    @property
    def topic_names(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._topics))

    @property
    def subscription_count(self) -> int:
        with self._lock:
            return len(self._subscriptions)

    @property
    def dead_letter_topic(self) -> str:
        return self._dead_letter_topic

    def create_topic(self, name: str, capacity: int | None = None,
                     policy: OverflowPolicy | None = None) -> Topic:
        """幂等：同名主题只建一次。新主题建出来时，所有匹配它的通配订阅立刻挂上游标——
        通配订阅因此对"以后才出现的主题"也有效，而这一步没有碰投递路径一行。"""
        with self._lock:
            existing = self._topics.get(name)
            if existing is not None:
                return existing
            topic = Topic(name, capacity or self._capacity, policy or self._policy, self._clock)
            self._topics[name] = topic
            waiting = [s for s in self._subscriptions.values() if s.pattern.matches(name)]
        for subscription in waiting:
            subscription.attach(topic)
        return topic

    def topic(self, name: str) -> Topic:
        with self._lock:
            try:
                return self._topics[name]
            except KeyError:
                raise TopicNotFoundError(f"no such topic: {name}") from None

    def publish(self, topic_name: str, payload: object, key: str | None = None,
                headers: Mapping[str, object] | None = None, timeout: float | None = None) -> Message:
        """发布一条消息并返回它（带上位点）。发布者不认识任何订阅者，这是 Pub-Sub 与观察者
        最实质的区别：观察者里 subject 手里攥着一份观察者名单，这里没有这份名单。"""
        with self._lock:
            if self._closed:
                raise BrokerClosedError("broker is closed")
            topic = self._topics.get(topic_name)
            if topic is None:
                if not self._auto_create:
                    raise TopicNotFoundError(f"no such topic: {topic_name}")
        if topic is None:
            topic = self.create_topic(topic_name)
        message = topic.append(payload, key, headers, timeout)
        with self._lock:
            listeners = [s for s in self._subscriptions.values() if s.pattern.matches(topic_name)]
        for subscription in listeners:
            subscription.wake()
        return message

    def subscribe(self, pattern: str, handler: Handler | None = None, from_beginning: bool = False,
                  max_attempts: int = 1, retry_delay: float = 0.0, dead_letter: bool = False,
                  name: str | None = None, batch_size: int = 16) -> Subscription:
        """订阅一个主题或一族主题。`handler=None` 就是拉模式，自己调 `poll()`。

        `dead_letter=True` 时，重试用尽的消息会被转投死信主题——而死信主题也只是一个普通
        主题，于是"订阅所有投递失败"用的还是同一套 `subscribe`，没有第二套机制。
        """
        topic_pattern = TopicPattern(pattern)
        sub_id = name or f"sub-{next(self._next_id)}"
        policy = self._dead_letter_policy if dead_letter else None
        subscription = Subscription(sub_id, topic_pattern, handler, from_beginning, max_attempts,
                                    retry_delay, policy, batch_size)
        with self._lock:
            if self._closed:
                subscription.close()
                raise BrokerClosedError("broker is closed")
            if sub_id in self._subscriptions:
                subscription.close()
                raise PubSubError(f"duplicate subscription id: {sub_id}")
            self._subscriptions[sub_id] = subscription
            matched = [t for n, t in self._topics.items() if topic_pattern.matches(n)]
            if not matched and not topic_pattern.is_wildcard and not self._auto_create:
                del self._subscriptions[sub_id]
                subscription.close()
                raise TopicNotFoundError(f"no such topic: {pattern}")
        if not matched and not topic_pattern.is_wildcard:
            matched = [self.create_topic(pattern)]
        for topic in matched:
            subscription.attach(topic)
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """退订：先从注册表摘掉（不再被唤醒），再关订阅（排空、汇合、摘游标）。"""
        with self._lock:
            self._subscriptions.pop(subscription.id, None)
        subscription.close()

    def _dead_letter_policy(self, subscription: Subscription, message: Message,
                            exc: BaseException) -> None:
        """失败策略之一：原样转投死信主题，并在消息头里留下"从哪来、为什么死"。"""
        self.publish(self._dead_letter_topic, message.payload, key=message.key,
                     headers={"origin_topic": message.topic, "origin_seq": message.seq,
                              "subscription": subscription.id, "error": repr(exc)})

    def close(self) -> None:
        """先关订阅（每条投递线程把已发布的消息投完），再关主题，最后拒绝新的发布。"""
        with self._lock:
            if self._closed:
                return
            self._closed = True
            subscriptions = tuple(self._subscriptions.values())
            self._subscriptions.clear()
            topics = tuple(self._topics.values())
        for subscription in subscriptions:
            subscription.close()
        for topic in topics:
            topic.close()


def _demo() -> None:
    broker = Broker(capacity=8)
    seen: list[str] = []
    broker.subscribe("orders.*", lambda m: seen.append(f"{m.topic}#{m.seq}"), name="audit")
    puller = broker.subscribe("orders.created", name="reporting")
    broker.publish("orders.created", {"id": 1})
    broker.publish("orders.shipped", {"id": 1})
    print("pull:", [m.seq for m in puller.poll(max_items=10, timeout=0.5)])
    broker.close()
    print("push:", seen)


if __name__ == "__main__":
    _demo()
