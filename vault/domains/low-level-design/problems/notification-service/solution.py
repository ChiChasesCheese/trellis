"""通知服务（Notification Service）：一次请求扇出到多个渠道，中间隔着偏好、限额、优先级与重试。
设计：`Provider` 是渠道的唯一抽象（一个 `channel` 名加一个会失败的 `send`），`UserPreferences`
回答"这个人此刻愿不愿意从这个渠道收"，`RateLimiter` 和 `IdempotencyStore` 各守一条不变量，
`LaneQueue` 把"优先级"落实成分道 FIFO 加配额，`NotificationService` 只负责把这些串起来。
可靠性（重试、退避、死信、幂等）写在派发器里一份，不按渠道复制；渠道只管怎么发，不管发几次。
时钟一律注入，于是静默时段、限流窗口和退避全都可测而不必 sleep。
"""

from __future__ import annotations

import heapq
import itertools
import threading
import time
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import Enum, IntEnum
from types import MappingProxyType
from typing import Protocol

Clock = Callable[[], datetime]
EMPTY_PARAMS: Mapping[str, object] = MappingProxyType({})
UNLIMITED = 1 << 30


def utc_now() -> datetime:
    """默认时钟。带时区，静默时段才可能跨时区算对。"""
    return datetime.now(timezone.utc)


class NotificationError(Exception):
    """本服务所有失败的共同基类。"""


class TransientDeliveryError(NotificationError):
    """可重试的失败：超时、502、对端限流。渠道实现应当抛它来表示"再试一次也许就好"。"""


class PermanentDeliveryError(NotificationError):
    """不可重试的失败：地址非法、用户已注销、内容被拒。重试一百次也是同一个结果。"""


class UnknownTemplateError(NotificationError, KeyError):
    """请求里引用了一个没有注册过的模板。"""


class Priority(IntEnum):
    """优先级。用 `IntEnum` 是因为偏好里要写"这个渠道至少多重要我才收"，需要比大小。"""

    MARKETING = 10        # 营销、周报：可以被静默时段和限额挡掉
    TRANSACTIONAL = 20    # 订单已发货、密码已修改：业务事实，尽量送到
    URGENT = 30           # 一次性验证码（OTP）、安全告警：穿透静默时段，永不被营销拖慢


class DeliveryStatus(Enum):
    """一次投递尝试的终局。每一种"没发出去"都必须有自己的名字——合成一句
    "发送失败"，调用方既不知道要不要重试，也不知道要不要告诉用户。"""

    SENT = "sent"
    QUEUED = "queued"                              # 已通过全部策略、排进队列，等待派发
    DUPLICATE = "duplicate"                       # 幂等键重复，这次是空操作
    RETRY_SCHEDULED = "retry_scheduled"           # 瞬时失败，已排进重试
    DEAD_LETTERED = "dead_lettered"               # 永久失败或重试用尽
    SUPPRESSED_CHANNEL_OFF = "channel_off"        # 用户关掉了这个渠道
    SUPPRESSED_PRIORITY = "below_min_priority"    # 没到用户为该渠道设的重要性门槛
    SUPPRESSED_QUIET_HOURS = "quiet_hours"        # 处于静默时段，且不是 URGENT
    SUPPRESSED_RATE_LIMIT = "rate_limited"        # 触到该用户该渠道的频次上限
    SUPPRESSED_NO_ADDRESS = "no_address"          # 用户没留这个渠道的地址
    SUPPRESSED_NO_PROVIDER = "no_provider"        # 没有注册这个渠道的 provider


@dataclass(frozen=True, slots=True)
class Notification:
    """调用方交给服务的一次请求：给谁、用哪个模板、有多重要、幂等键是什么。

    `notification_id` **由调用方提供**：只有调用方知道"这两次调用是不是同一件事"。
    服务自己生成 UUID 的话，重发就永远是一条新消息，幂等无从谈起。
    """

    notification_id: str
    user_id: str
    template: str
    params: Mapping[str, object] = field(default_factory=lambda: EMPTY_PARAMS)
    priority: Priority = Priority.TRANSACTIONAL
    channels: tuple[str, ...] | None = None       # None = 听用户偏好的


@dataclass(frozen=True, slots=True)
class Envelope:
    """一次请求在某个渠道上物化出来的东西：真正要交给 provider 的那封信。

    冻结的事件对象：它带齐了渠道需要的一切（地址、标题、正文），于是 provider 永远不必
    回头去问服务任何事，也就不必和服务争锁。重试时用 `replace(envelope, attempt=n)` 造新的。
    """

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
        """幂等的粒度是"一次请求 × 一个渠道"：邮件发成功、短信失败重发，两者互不影响。"""
        return f"{self.notification_id}|{self.channel}"


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    """一次投递的结果。冻结，可以直接进历史、进死信、返回给调用方。"""

    notification_id: str
    user_id: str
    channel: str
    status: DeliveryStatus
    attempts: int = 0
    detail: str = ""

    @property
    def delivered(self) -> bool:
        return self.status is DeliveryStatus.SENT


class Provider(Protocol):
    """渠道的唯一抽象：一个名字，一个会失败的 `send`。

    它**不**知道重试、限流、幂等、优先级——那些是派发器的事，写在一处。渠道只回答
    "这封信怎么发出去"，失败时用异常区分可重试与不可重试。
    """

    channel: str

    def send(self, envelope: Envelope) -> str: ...


@dataclass(frozen=True, slots=True)
class UserPreferences:
    """一个用户的收信意愿。冻结：改偏好是换一个对象，不是就地改字段，于是读它永远不用加锁。

    它拥有一条不变量：**URGENT 穿透静默时段**。一次性验证码不会因为用户设了"晚上十点后免打扰"
    而发不出去——这条规则写在这里，而不是散在调用方的 `if` 里。
    """

    user_id: str
    addresses: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    enabled_channels: frozenset[str] = frozenset()
    min_priority: Mapping[str, Priority] = field(default_factory=lambda: MappingProxyType({}))
    quiet_hours: tuple[int, int] | None = None     # (起始小时, 结束小时)，本地时间，可跨午夜
    utc_offset_minutes: int = 0

    def local_hour(self, now: datetime) -> int:
        return (now + timedelta(minutes=self.utc_offset_minutes)).hour

    def in_quiet_hours(self, now: datetime) -> bool:
        """静默时段可以跨午夜（22 点到次日 7 点），所以不能只写一个 `start <= h < end`。"""
        if self.quiet_hours is None:
            return False
        start, end = self.quiet_hours
        hour = self.local_hour(now)
        return start <= hour < end if start < end else (hour >= start or hour < end)

    def decide(self, channel: str, priority: Priority, now: datetime) -> DeliveryStatus | None:
        """返回抑制原因，或者 `None` 表示放行。顺序是刻意的：先问"你要不要"，再问"你在不在"。"""
        if channel not in self.enabled_channels:
            return DeliveryStatus.SUPPRESSED_CHANNEL_OFF
        if priority < self.min_priority.get(channel, Priority.MARKETING):
            return DeliveryStatus.SUPPRESSED_PRIORITY
        if priority is not Priority.URGENT and self.in_quiet_hours(now):
            return DeliveryStatus.SUPPRESSED_QUIET_HOURS
        if channel not in self.addresses:
            return DeliveryStatus.SUPPRESSED_NO_ADDRESS
        return None

    @property
    def target_channels(self) -> tuple[str, ...]:
        """按名字排序，让扇出的顺序可预测——测试因此不必迁就 set 的迭代顺序。"""
        return tuple(sorted(self.enabled_channels))


class TemplateLibrary:
    """模板库：`(模板名, 渠道) -> (标题, 正文)`，渠道没有专属版本就退回到默认版本。

    模板是**数据**不是代码：加一个模板、给短信加一个短版本，都只是往字典里塞一条，
    派发器、渠道、偏好一行不用动。`str.format` 足够——为一个通知服务塞进 Jinja 是过度设计。
    """

    def __init__(self) -> None:
        self._templates: dict[tuple[str, str | None], tuple[str, str]] = {}
        self._lock = threading.Lock()

    @property
    def template_count(self) -> int:
        with self._lock:
            return len(self._templates)

    def register(self, name: str, title: str, body: str, channel: str | None = None) -> None:
        """`channel=None` 注册默认版本；给某个渠道单独注册就覆盖它（短信的 140 字版）。"""
        with self._lock:
            self._templates[(name, channel)] = (title, body)

    def knows(self, name: str) -> bool:
        """这个模板名存在吗（任意渠道版本都算）。派发器用它在产生任何副作用之前挡住笔误。"""
        with self._lock:
            return any(key[0] == name for key in self._templates)

    def render(self, name: str, channel: str, params: Mapping[str, object]) -> tuple[str, str]:
        with self._lock:
            entry = self._templates.get((name, channel)) or self._templates.get((name, None))
        if entry is None:
            raise UnknownTemplateError(f"no template {name!r} for channel {channel!r}")
        title, body = entry
        return title.format(**params), body.format(**params)


class RateLimiter:
    """按 key 的滑动窗口计数：注入时钟，所以测试推时钟而不是 sleep。

    它拥有的不变量是**不泄漏**：窗口内没有记录的 key 会被删掉。一个 `dict[user, deque]`
    只涨不落，是这类组件里最常见的内存事故——限流器本该是有界的。
    """

    def __init__(self, limit: int, window_seconds: float, clock: Clock = utc_now) -> None:
        if limit < 0:
            raise ValueError(f"limit must not be negative, got {limit}")
        self._limit = limit
        self._window = timedelta(seconds=window_seconds)
        self._clock = clock
        self._hits: dict[str, deque[datetime]] = {}
        self._lock = threading.Lock()

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def tracked_keys(self) -> int:
        """还在被跟踪的 key 数。测试用它断言"窗口过去之后这里是空的"。"""
        with self._lock:
            return len(self._hits)

    def allow(self, key: str) -> bool:
        """放行就记一笔并返回 True；超限返回 False 且**不**记账（否则被限流的请求会自我延长窗口）。"""
        now = self._clock()
        with self._lock:
            hits = self._trim(key, now)
            if len(hits) >= self._limit:
                if not hits:
                    self._hits.pop(key, None)
                return False
            hits.append(now)
            self._hits[key] = hits
            return True

    def _trim(self, key: str, now: datetime) -> deque[datetime]:
        hits = self._hits.get(key)
        if hits is None:
            return deque()
        cutoff = now - self._window
        while hits and hits[0] <= cutoff:
            hits.popleft()
        if not hits:
            self._hits.pop(key, None)
        return hits

    def purge(self) -> int:
        """把所有已经空掉的窗口清出去，返回清掉的 key 数。派发器定期调用它。"""
        now = self._clock()
        with self._lock:
            stale = [k for k, hits in self._hits.items() if not hits or hits[-1] <= now - self._window]
            for key in stale:
                del self._hits[key]
            return len(stale)


class IdempotencyStore:
    """带过期时间的"这件事做过没有"。`claim` 是原子的检查加占坑，不是先查后写。

    有 TTL，并且有 `purge()`：一个只写不删的去重表，就是一个保证会 OOM 的组件。
    """

    def __init__(self, ttl_seconds: float = 3600.0, clock: Clock = utc_now, capacity: int = 100_000) -> None:
        self._ttl = timedelta(seconds=ttl_seconds)
        self._clock = clock
        self._capacity = capacity
        self._entries: dict[str, tuple[datetime, DeliveryResult | None]] = {}
        self._lock = threading.Lock()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._entries)

    def claim(self, key: str) -> DeliveryResult | None:
        """第一次见到这个 key 返回 `None`（占坑成功）；重复则返回上一次记下的结果。

        "先 `if key in store` 再 `store[key] = ...`"是典型的检查—然后—行动（check-then-act）
        竞态：两个线程可以同时通过检查，同一封信就发了两遍。所以整段在同一把锁里。
        """
        now = self._clock()
        with self._lock:
            entry = self._entries.get(key)
            if entry is not None and now - entry[0] <= self._ttl:
                return entry[1] if entry[1] is not None else _PENDING
            if len(self._entries) >= self._capacity:
                self._purge_locked(now)
            self._entries[key] = (now, None)
            return None

    def record(self, key: str, result: DeliveryResult) -> None:
        with self._lock:
            if key in self._entries:
                self._entries[key] = (self._entries[key][0], result)

    def purge(self) -> int:
        with self._lock:
            return self._purge_locked(self._clock())

    def _purge_locked(self, now: datetime) -> int:
        stale = [k for k, (stamp, _) in self._entries.items() if now - stamp > self._ttl]
        for key in stale:
            del self._entries[key]
        return len(stale)


_PENDING = DeliveryResult("", "", "", DeliveryStatus.DUPLICATE, 0, "in flight")


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """指数退避。`jitter` 留成参数而不是内部随机：测试要可重复，生产要防惊群。"""

    max_attempts: int = 3
    base_delay: float = 1.0
    multiplier: float = 2.0
    max_delay: float = 60.0

    def delay_for(self, attempt: int) -> float:
        """第 `attempt` 次失败之后等多久。attempt 从 1 起算。"""
        return min(self.base_delay * (self.multiplier ** (attempt - 1)), self.max_delay)


class LaneQueue:
    """分道队列：每个优先级一条 FIFO，取的时候从高到低，但**每条道有连续服务配额**。

    这就是"优先级"在排队上的具体含义。严格优先级（高的取空才轮到低的）会把低优先级饿死；
    配额让高优先级连续取 `quota` 条之后必须让位一次，于是营销不会拖慢验证码，验证码的洪峰
    也不会让营销永远发不出去。配额默认极大，即退化成严格优先级。
    """

    def __init__(self, quota: Mapping[Priority, int] | None = None) -> None:
        self._lanes: dict[Priority, deque] = {p: deque() for p in Priority}
        self._quota = dict(quota or {})
        self._served = {p: 0 for p in Priority}
        self._lock = threading.Lock()

    @property
    def size(self) -> int:
        with self._lock:
            return sum(len(lane) for lane in self._lanes.values())

    def depth(self, priority: Priority) -> int:
        """某一条道上堆了多少——把"营销积压了两千条"变成一个可以打印的数字。"""
        with self._lock:
            return len(self._lanes[priority])

    def put(self, priority: Priority, item: object) -> None:
        with self._lock:
            self._lanes[priority].append(item)

    def get(self) -> object | None:
        """取一条；空就返回 `None`（不阻塞——等待归派发器管，队列只管顺序）。"""
        with self._lock:
            lanes = sorted(Priority, reverse=True)
            for index, priority in enumerate(lanes):
                lane = self._lanes[priority]
                if not lane:
                    continue
                quota = self._quota.get(priority, UNLIMITED)
                lower_waiting = any(self._lanes[p] for p in lanes[index + 1:])
                if self._served[priority] >= quota and lower_waiting:
                    self._served[priority] = 0        # 让位一次，下一轮重新计数
                    continue
                self._served[priority] += 1
                return lane.popleft()
            return None


class NotificationService:
    """派发器：把请求物化成信封、过一遍策略、排进分道队列、按时重试、失败进死信。

    可靠性只在这里写一份。渠道不知道重试，偏好不知道队列，限流器不知道渠道——每个零件
    只认识自己那条不变量，加一个渠道或一个模板都不会碰到这个类。
    """

    def __init__(self, clock: Clock = utc_now, retry: RetryPolicy | None = None,
                 rate_limit: tuple[int, float] | None = None, idempotency_ttl: float = 3600.0,
                 lane_quota: Mapping[Priority, int] | None = None, history: int = 1024) -> None:
        self._clock = clock
        self._retry = retry or RetryPolicy()
        self._templates = TemplateLibrary()
        self._providers: dict[str, Provider] = {}
        self._preferences: dict[str, UserPreferences] = {}
        self._limiter = RateLimiter(*rate_limit, clock=clock) if rate_limit else None
        self._idempotency = IdempotencyStore(idempotency_ttl, clock)
        self._queue = LaneQueue(lane_quota)
        self._delayed: list[tuple[datetime, int, Envelope]] = []
        self._tick = itertools.count(1)
        self._history: deque[DeliveryResult] = deque(maxlen=history)
        self._dead_letters: deque[DeliveryResult] = deque(maxlen=history)
        self._sent = 0
        self._dispatched = 0
        self._stopped = threading.Event()
        self._workers: tuple[threading.Thread, ...] = ()
        self._lock = threading.RLock()

    # ---- 配置 ---------------------------------------------------------

    @property
    def templates(self) -> TemplateLibrary:
        return self._templates

    @property
    def channels(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._providers))

    def register_provider(self, provider: Provider) -> None:
        """加一个渠道 = 注册一个 provider。**渠道名是开放的字符串，不是 `Enum`**——
        用 `Enum` 的话，加 in-app 或 webhook 就得改这个类，正好违背第 4 关的要求。"""
        with self._lock:
            self._providers[provider.channel] = provider

    def set_preferences(self, preferences: UserPreferences) -> None:
        with self._lock:
            self._preferences[preferences.user_id] = preferences

    def preferences_for(self, user_id: str) -> UserPreferences:
        with self._lock:
            return self._preferences.get(user_id) or UserPreferences(user_id)

    # ---- 可观测状态 ---------------------------------------------------

    @property
    def sent_count(self) -> int:
        with self._lock:
            return self._sent

    @property
    def pending_count(self) -> int:
        """排队中 + 等待重试的信封数。两者都要算，否则"已经清空了吗"会答错。"""
        with self._lock:
            return self._queue.size + len(self._delayed)

    @property
    def dead_letters(self) -> tuple[DeliveryResult, ...]:
        """快照，不是内部队列本身。它有上限（`maxlen`），死信不会把内存吃光。"""
        with self._lock:
            return tuple(self._dead_letters)

    @property
    def history(self) -> tuple[DeliveryResult, ...]:
        with self._lock:
            return tuple(self._history)

    def queue_depth(self, priority: Priority) -> int:
        return self._queue.depth(priority)

    # ---- 提交 ---------------------------------------------------------

    def submit(self, notification: Notification) -> tuple[DeliveryResult, ...]:
        """把一次请求扇出到各个渠道。抑制与重复**当场**返回结果，其余排队。

        策略全部在这里判完再入队，而不是在发送时判：调用方立刻知道"这条为什么没发"，
        队列里躺着的也就全是"确定要发"的信封，重试路径因此不必再走一遍偏好与限额。
        """
        now = self._clock()
        preferences = self.preferences_for(notification.user_id)
        targets = notification.channels if notification.channels is not None else preferences.target_channels
        if targets and not self._templates.knows(notification.template):
            raise UnknownTemplateError(f"no template {notification.template!r}")   # 先于一切副作用
        results: list[DeliveryResult] = []
        for channel in targets:
            results.append(self._admit(notification, preferences, channel, now))
        return tuple(results)

    def _admit(self, notification: Notification, preferences: UserPreferences,
               channel: str, now: datetime) -> DeliveryResult:
        key = f"{notification.notification_id}|{channel}"
        previous = self._idempotency.claim(key)
        if previous is not None:
            return self._record(DeliveryResult(notification.notification_id, notification.user_id,
                                               channel, DeliveryStatus.DUPLICATE, 0,
                                               f"already {previous.status.value}"), key=None)
        with self._lock:
            provider = self._providers.get(channel)
        if provider is None:
            return self._settle(key, notification, channel, DeliveryStatus.SUPPRESSED_NO_PROVIDER)
        suppressed = preferences.decide(channel, notification.priority, now)
        if suppressed is not None:
            return self._settle(key, notification, channel, suppressed)
        if self._limiter is not None and not self._limiter.allow(f"{notification.user_id}|{channel}"):
            return self._settle(key, notification, channel, DeliveryStatus.SUPPRESSED_RATE_LIMIT)
        title, body = self._templates.render(notification.template, channel, notification.params)
        envelope = Envelope(notification.notification_id, notification.user_id, channel,
                            preferences.addresses[channel], title, body, notification.priority)
        self._queue.put(notification.priority, envelope)
        return DeliveryResult(notification.notification_id, notification.user_id, channel,
                              DeliveryStatus.QUEUED, 0, f"queued in the {notification.priority.name} lane")

    # ---- 派发 ---------------------------------------------------------

    def run_pending(self, max_items: int = 1) -> int:
        """处理最多 `max_items` 件可运行的事，返回实际处理数。到点的重试先放回队列。

        注入时钟之后，"到点了没有"是一次比较而不是一次 sleep，所以整条重试路径在测试里
        完全确定：推时钟、再 `drain()`，退避多久、第几次进死信都能断言。
        """
        self._promote_due()
        done = 0
        while done < max_items:
            envelope = self._queue.get()
            if envelope is None:
                break
            self._attempt(envelope)          # type: ignore[arg-type]
            done += 1
        return done

    def drain(self, limit: int = 10_000) -> int:
        """把此刻所有可运行的事做完（不等未来到期的重试）。返回处理条数。"""
        total = 0
        while total < limit:
            done = self.run_pending(max_items=64)
            if done == 0:
                return total
            total += done
        return total

    def _promote_due(self) -> None:
        now = self._clock()
        with self._lock:
            while self._delayed and self._delayed[0][0] <= now:
                _, _, envelope = heapq.heappop(self._delayed)
                self._queue.put(envelope.priority, envelope)

    def _attempt(self, envelope: Envelope) -> None:
        """真正调 provider 的地方。**调用时不持有本服务的任何锁**——渠道是外部代码，
        它可能很慢、可能回调回来，持锁调外部代码是死锁的标准配方。"""
        with self._lock:
            provider = self._providers.get(envelope.channel)
            self._dispatched += 1
            housekeeping = self._dispatched % 128 == 0
        if housekeeping:
            self._idempotency.purge()
            if self._limiter is not None:
                self._limiter.purge()
        if provider is None:
            self._finish(envelope, DeliveryStatus.SUPPRESSED_NO_PROVIDER, "provider went away")
            return
        try:
            detail = provider.send(envelope)
        except TransientDeliveryError as exc:
            self._on_transient(envelope, exc)
        except Exception as exc:  # noqa: BLE001 — 渠道抛什么都不许打断派发线程
            self._finish(envelope, DeliveryStatus.DEAD_LETTERED, f"permanent: {exc!r}")
        else:
            with self._lock:
                self._sent += 1
            self._finish(envelope, DeliveryStatus.SENT, detail or "")

    def _on_transient(self, envelope: Envelope, exc: BaseException) -> None:
        if envelope.attempt >= self._retry.max_attempts:
            self._finish(envelope, DeliveryStatus.DEAD_LETTERED,
                         f"gave up after {envelope.attempt} attempt(s): {exc!r}")
            return
        delay = self._retry.delay_for(envelope.attempt)
        nxt = replace(envelope, attempt=envelope.attempt + 1)
        with self._lock:
            heapq.heappush(self._delayed, (self._clock() + timedelta(seconds=delay), next(self._tick), nxt))
            self._history.append(DeliveryResult(envelope.notification_id, envelope.user_id,
                                                envelope.channel, DeliveryStatus.RETRY_SCHEDULED,
                                                envelope.attempt, f"retry in {delay:g}s: {exc!r}"))

    def _finish(self, envelope: Envelope, status: DeliveryStatus, detail: str) -> None:
        result = DeliveryResult(envelope.notification_id, envelope.user_id, envelope.channel,
                                status, envelope.attempt, detail)
        self._record(result, key=envelope.idempotency_key)

    def _settle(self, key: str, notification: Notification, channel: str,
                status: DeliveryStatus) -> DeliveryResult:
        result = DeliveryResult(notification.notification_id, notification.user_id, channel, status, 0,
                                status.value)
        return self._record(result, key=key)

    def _record(self, result: DeliveryResult, key: str | None) -> DeliveryResult:
        if key is not None:
            self._idempotency.record(key, result)
        with self._lock:
            self._history.append(result)
            if result.status is DeliveryStatus.DEAD_LETTERED:
                self._dead_letters.append(result)
        return result

    # ---- 线程 ---------------------------------------------------------

    def start(self, workers: int = 1, idle_sleep: float = 0.005) -> None:
        """起若干条派发线程。它们只是反复调 `run_pending()`——测试里可以完全不起线程。"""
        with self._lock:
            if self._workers:
                return
            self._stopped.clear()
            self._workers = tuple(
                threading.Thread(target=self._loop, args=(idle_sleep,), name=f"notify-{i}", daemon=True)
                for i in range(workers))
        for worker in self._workers:
            worker.start()

    def _loop(self, idle_sleep: float) -> None:
        while not self._stopped.is_set():
            if self.run_pending(max_items=16) == 0:
                self._stopped.wait(idle_sleep)

    def stop(self, drain: bool = True, timeout: float = 5.0) -> None:
        """停线程。`drain=True` 时先把队列里已经排好的信封发完——重试是排到未来的，不等。"""
        if drain:
            deadline = time.monotonic() + timeout
            while self._queue.size and time.monotonic() < deadline:
                self.run_pending(max_items=64)
        self._stopped.set()
        with self._lock:
            workers, self._workers = self._workers, ()
        for worker in workers:
            worker.join(timeout)


class CollectingProvider:
    """一个把信封收进列表的 provider，给演示和冒烟用。真正的渠道在测试里由调用方注入。"""

    def __init__(self, channel: str) -> None:
        self.channel = channel
        self.sent: list[Envelope] = []
        self._lock = threading.Lock()

    def send(self, envelope: Envelope) -> str:
        with self._lock:
            self.sent.append(envelope)
            return f"{self.channel}:{len(self.sent)}"


def _demo() -> None:
    noon = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    service = NotificationService(clock=lambda: noon, rate_limit=(5, 60.0),
                                  lane_quota={Priority.URGENT: 2})
    email, sms = CollectingProvider("email"), CollectingProvider("sms")
    service.register_provider(email)
    service.register_provider(sms)
    service.templates.register("otp", "验证码", "您的验证码是 {code}，五分钟内有效。")
    service.templates.register("sale", "促销", "{name} 正在打折。")
    service.set_preferences(UserPreferences(
        "u1", addresses={"email": "u1@example.com", "sms": "+8613800000000"},
        enabled_channels=frozenset({"email", "sms"}),
        min_priority={"sms": Priority.URGENT}, quiet_hours=(22, 7)))
    service.submit(Notification("n-1", "u1", "sale", {"name": "耳机"}, Priority.MARKETING))
    service.submit(Notification("n-2", "u1", "otp", {"code": "482913"}, Priority.URGENT))
    service.submit(Notification("n-2", "u1", "otp", {"code": "482913"}, Priority.URGENT))  # 重发
    service.drain()
    print("email:", [e.title for e in email.sent])
    print("sms:", [e.title for e in sms.sent], "sent =", service.sent_count)


if __name__ == "__main__":
    _demo()
