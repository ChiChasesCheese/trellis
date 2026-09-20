"""限流器（Rate Limiter）：进程内的库级组件，不是分布式限流架构。
设计：一次判定的结果是 `Decision`（准不准、还剩多少、多久后再来），不是裸 bool；
"怎么记住最近的流量"整体做成可替换的 `RateLimitAlgorithm`（固定窗口／令牌桶／滑动日志／滑动计数），
四种算法共用基类里同一套"用掉多少 / 还能不能过 / 多久才行"的判定骨架；
`RateLimiter` 只负责"按 key 隔离状态 + 分片加锁 + 让闲置 key 的状态被回收"，
`CompositeLimiter` 把多条规则（按用户、按接口）组合成"先全查、全过才全扣"的两阶段判定。
"""

from __future__ import annotations

import math
import threading
import time
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable, Hashable, Iterator, Sequence
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, replace
from typing import Generic, TypeVar

T = TypeVar("T")

Clock = Callable[[], float]
"""时钟：一个返回单调秒数的无参函数。永远从外部注入，便于测试与回放。"""

AlgorithmFactory = Callable[[], "RateLimitAlgorithm"]
"""造一份"某个 key 的限流状态"的工厂——每个 key 第一次出现时调用一次。"""

_PURGE_FLOOR = 64
"""分片至少累计这么多次操作才值得扫一遍自己，避免小流量下反复空扫。"""


class RateLimiterError(Exception):
    """本模块所有异常的根。"""


class InvalidConfiguration(RateLimiterError, ValueError):
    """参数本身就不成立：非正的限额、非正的窗口、重复的限流器、非正的开销。

    注意"被限流"不在这里——被拒绝是正常的业务结果，用返回值表达，不是异常。
    """


@dataclass(frozen=True, slots=True)
class Decision:
    """一次判定的结果：准不准（allowed）、还剩多少额度（remaining）、多久后重试（retry_after）。

    `remaining` 的口径和 HTTP 响应头 `X-RateLimit-Remaining` 一致：**服务完这次请求之后**
    还剩多少。被拒时这次请求没被服务，所以它就是当前剩余量（通常是 0）。
    `rule` 是做出这个判定的规则名，只有组合限流器才用得上——被拒时调用方要能说出
    "是按用户拒的还是按接口拒的"。`__bool__` 让 `if limiter.allow(key):` 照样能写，
    于是从裸 bool 升级成结构化结果不需要调用方改一行既有代码。
    """

    allowed: bool
    remaining: int
    retry_after: float
    rule: str = ""

    def __bool__(self) -> bool:
        return self.allowed


class RateLimitAlgorithm(ABC):
    """一个 key 的限流状态。子类只回答三件事，判定骨架写在基类里不重复。

    - `_used(now)`：此刻这个 key 已经占掉多少额度（可以是小数）。
    - `_retry_after(now, cost)`：在额度不够时，还要等多久才够。
    - `commit(now, cost)`：真正扣掉额度——只有在 `check` 说准了之后才调用。

    `limit` 是一个窗口内的持续额度，`capacity` 是某一瞬间最多能占掉多少（默认等于 limit，
    只有令牌桶会把它抬高来表达"允许攒多大的突发"）。
    """

    def __init__(self, limit: int, window: float, capacity: float | None = None) -> None:
        if limit <= 0:
            raise InvalidConfiguration(f"limit must be positive, got {limit}")
        if window <= 0:
            raise InvalidConfiguration(f"window must be positive, got {window}")
        self.limit = limit
        self.window = float(window)
        self.capacity = float(limit if capacity is None else capacity)
        if self.capacity < 1:
            raise InvalidConfiguration(f"capacity must be at least 1, got {self.capacity}")

    @abstractmethod
    def _used(self, now: float) -> float:
        """此刻已占用的额度。它同时定义了"闲置"：占用为 0 的状态和新建的状态无法区分。"""

    @abstractmethod
    def _retry_after(self, now: float, cost: int) -> float:
        """额度不够时，距离够用还要等多少秒。只在 `check` 判定为拒绝时被调用。"""

    @abstractmethod
    def commit(self, now: float, cost: int) -> None:
        """扣掉 cost 份额度。调用方必须先 `check` 且拿到 allowed=True。"""

    def check(self, now: float, cost: int = 1) -> Decision:
        """只判定、不扣额度（纯查询）。两阶段判定的第一阶段，组合限流器依赖它。"""
        if cost <= 0:
            raise InvalidConfiguration(f"cost must be positive, got {cost}")
        used = self._used(now)
        remaining = max(0, int(self.capacity - used))
        if used + cost <= self.capacity:
            return Decision(True, remaining - cost, 0.0)
        if cost > self.capacity:
            # 单次开销就超过上限：等到天荒地老也不会通过，别给调用方一个会骗它的重试时间。
            return Decision(False, remaining, math.inf)
        return Decision(False, remaining, self._retry_after(now, cost))

    def try_acquire(self, now: float, cost: int = 1) -> Decision:
        """check + commit 的合体。被拒绝时**一份额度都不扣**，也不把重试时间往后推。"""
        decision = self.check(now, cost)
        if decision.allowed:
            self.commit(now, cost)
        return decision

    def is_idle(self, now: float) -> bool:
        """这份状态是否已经和"刚 new 出来的状态"完全等价——等价就可以安全地丢掉。

        这条判据对四种算法都成立，因为它就是 `_used(now) == 0` 的另一种说法：
        一个什么都没占的状态，留着和删掉对任何后续判定的结果都没有区别。
        """
        return self._used(now) <= 0.0


class FixedWindowCounter(RateLimitAlgorithm):
    """固定窗口计数：把时间切成对齐的格子，每格一个计数器。两个 int，最省内存。

    代价是边界突发——见 `SlidingWindowCounter` 的注释。它留在这里不是为了被用，
    而是为了让"边界突发"这件事在测试里能被断言出来。
    """

    def __init__(self, limit: int, window: float) -> None:
        super().__init__(limit, window)
        self._index = -1
        self._used_in_window = 0

    def _used(self, now: float) -> float:
        return float(self._used_in_window) if int(now // self.window) == self._index else 0.0

    def _retry_after(self, now: float, cost: int) -> float:
        return (int(now // self.window) + 1) * self.window - now

    def commit(self, now: float, cost: int) -> None:
        index = int(now // self.window)
        if index != self._index:
            self._index, self._used_in_window = index, 0
        self._used_in_window += cost


class TokenBucket(RateLimitAlgorithm):
    """令牌桶：桶里的令牌按固定速率补充，一次请求拿走 cost 个。两个浮点数。

    补令牌是**惰性**的：不起后台线程、不挂定时器，每次判定时用"距上次记账过了多久"
    现算。一百万个闲置 key 因此一分钱 CPU 都不花——这正是它能撑住海量 key 的原因。
    `burst` 把瞬时容量和持续速率解耦：每分钟 60 次，但一口气最多 5 次。
    """

    def __init__(self, limit: int, window: float, burst: float | None = None) -> None:
        super().__init__(limit, window, capacity=burst)
        self._rate = limit / self.window
        self._tokens = self.capacity
        self._stamp: float | None = None

    @property
    def refill_rate(self) -> float:
        """每秒补充的令牌数，只读——测试和读者都需要它，但没人该改它。"""
        return self._rate

    def _tokens_at(self, now: float) -> float:
        if self._stamp is None:
            return self.capacity
        # 时钟倒退时 elapsed 会是负数，凭空造出令牌；夹到 0 是唯一安全的处理。
        elapsed = max(0.0, now - self._stamp)
        return min(self.capacity, self._tokens + elapsed * self._rate)

    def _used(self, now: float) -> float:
        return self.capacity - self._tokens_at(now)

    def _retry_after(self, now: float, cost: int) -> float:
        return (cost - self._tokens_at(now)) / self._rate

    def commit(self, now: float, cost: int) -> None:
        self._tokens = self._tokens_at(now) - cost
        self._stamp = now


class SlidingWindowLog(RateLimitAlgorithm):
    """滑动窗口日志：记下每次放行的时刻，窗口外的丢掉。**精确**，没有任何边界效应。

    代价是内存与 limit 成正比：limit=10000 的 key 就要存一万个时间戳。只在限额小、
    精度要求高的地方用（比如"每分钟 5 条短信"）。
    """

    def __init__(self, limit: int, window: float) -> None:
        super().__init__(limit, window)
        self._log: deque[float] = deque()

    @property
    def logged(self) -> int:
        """日志里还留着多少条时间戳——用来断言"窗口滑过去之后内存确实降下来了"。"""
        return len(self._log)

    def _live(self, now: float) -> list[float]:
        """还落在窗口内的时间戳，从旧到新。不修改内部状态，`check` 必须保持纯粹。"""
        cutoff = now - self.window
        return [stamp for stamp in self._log if stamp > cutoff]

    def _used(self, now: float) -> float:
        return float(len(self._live(now)))

    def _retry_after(self, now: float, cost: int) -> float:
        live = self._live(now)
        # 要腾出 cost 份额度，就得等最早的 (len(live) + cost - capacity) 条记录滑出窗口。
        need = len(live) + cost - int(self.capacity)
        return live[need - 1] + self.window - now

    def commit(self, now: float, cost: int) -> None:
        cutoff = now - self.window
        while self._log and self._log[0] <= cutoff:
            self._log.popleft()
        self._log.extend([now] * cost)


class SlidingWindowCounter(RateLimitAlgorithm):
    """滑动窗口计数：当前格 + 上一格按重叠比例加权。三个数字，近似但够用。

    估算式是 `上一格计数 × 重叠比例 + 当前格计数`。它假设上一格的请求在格内**均匀**分布，
    所以真实流量集中在上一格开头时会高估、集中在结尾时会低估；高估意味着提前拒绝，
    对限流器而言这是安全的一侧。这是生产环境最常见的默认选择。
    """

    def __init__(self, limit: int, window: float) -> None:
        super().__init__(limit, window)
        self._index = -1
        self._current = 0
        self._previous = 0

    def _counts(self, now: float) -> tuple[float, float, float]:
        """返回 (上一格计数, 当前格计数, 当前格起点)，按 now 所在的格子重新对齐。"""
        index = int(now // self.window)
        start = index * self.window
        if index == self._index:
            return float(self._previous), float(self._current), start
        if index == self._index + 1:
            return float(self._current), 0.0, start
        return 0.0, 0.0, start

    def _used(self, now: float) -> float:
        previous, current, start = self._counts(now)
        overlap = 1.0 - (now - start) / self.window
        return previous * overlap + current

    def _retry_after(self, now: float, cost: int) -> float:
        previous, current, start = self._counts(now)
        budget = self.capacity - cost - current
        if budget >= 0:
            # 还能在本格内熬出来：等上一格的权重衰减到 budget 以下。
            return max(0.0, start + (1.0 - budget / previous) * self.window - now)
        # 光当前格就吃满了，只能等进入下一格——注意那时当前格会变成"上一格"，
        # 它的计数仍按重叠比例记着，所以答案不是"下一格开头"，而要继续解一次同样的不等式。
        # （早期版本在这里直接返回下一格开头，于是 retry_after 到点了还是被拒，是在骗调用方。）
        return start + self.window + (1.0 - (self.capacity - cost) / current) * self.window - now

    def commit(self, now: float, cost: int) -> None:
        index = int(now // self.window)
        if index == self._index + 1:
            self._previous, self._current = self._current, 0
        elif index != self._index:
            self._previous, self._current = 0, 0
        self._index = index
        self._current += cost


class _Shard:
    """一个分片：一把锁，外加归这把锁管的那部分 key→状态。

    分片是"每个 key 一把锁"和"全局一把锁"之间的中间答案：锁的数量是常数（不随 key 增长，
    也就不需要再为锁本身设计回收），而竞争只发生在同一分片内，大约是全局锁的 1/N。
    """

    __slots__ = ("lock", "states", "ops", "purge_at")

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.states: dict[Hashable, RateLimitAlgorithm] = {}
        self.ops = 0
        self.purge_at = _PURGE_FLOOR


class RateLimiter:
    """按 key 隔离的限流器：算法怎么算它不管，它管的是隔离、加锁和**状态回收**。

    每个 key 第一次出现时用 `factory` 造一份状态。这个字典是本设计里唯一会无限增长的
    容器，所以它必须会缩：每个分片累计的操作数超过它自己装的条目数时，顺手把
    `is_idle` 的状态删掉（摊还 O(1)）；也可以随时显式调用 `sweep()`。
    """

    def __init__(self, factory: AlgorithmFactory, *, clock: Clock = time.monotonic,
                 name: str = "", shards: int = 16) -> None:
        if shards <= 0:
            raise InvalidConfiguration(f"shards must be positive, got {shards}")
        self._factory = factory
        self._clock = clock
        self._name = name
        self._shards = tuple(_Shard() for _ in range(shards))

    @property
    def name(self) -> str:
        return self._name

    @property
    def tracked_keys(self) -> int:
        """当前占着内存的 key 数。回收做得对，它就不会随"见过多少 key"单调增长。"""
        return sum(self._sized(shard) for shard in self._shards)

    @staticmethod
    def _sized(shard: _Shard) -> int:
        with shard.lock:
            return len(shard.states)

    def _shard_of(self, key: Hashable) -> _Shard:
        return self._shards[hash(key) % len(self._shards)]

    @contextmanager
    def reserve(self, key: Hashable, now: float) -> Iterator[RateLimitAlgorithm]:
        """持锁取出某个 key 的状态，供两阶段判定使用；退出时顺手做摊还回收。

        它是公开的，因为 `CompositeLimiter` 需要"先把几条规则的状态都锁住，再统一决定
        扣不扣"。直接调用它的人必须在 with 块内完成 check 与 commit，不要把状态带出去。
        """
        shard = self._shard_of(key)
        with shard.lock:
            state = shard.states.get(key)
            if state is None:
                state = shard.states[key] = self._factory()
            shard.ops += 1
            try:
                yield state
            finally:
                if shard.ops >= shard.purge_at:
                    self._purge(shard, now)

    @staticmethod
    def _purge(shard: _Shard, now: float) -> None:
        """丢掉这个分片里所有"和新建状态等价"的条目。调用方必须已经持有分片锁。

        下一次扫描的门槛在这里**定死**为"扫完之后还剩多少条"，而不是每次去和当前条目数
        比较。差别是致命的：当每一次操作都带来一个新 key 时，条目数和操作数同速增长，
        "ops >= len(states)" 永远追不上，扫描只会在最开始触发一次，之后内存一路涨到天上。
        与"上次整理后的规模"比较，才真的是摊还 O(1)。
        """
        for key in [k for k, state in shard.states.items() if state.is_idle(now)]:
            del shard.states[key]
        shard.ops = 0
        shard.purge_at = max(_PURGE_FLOOR, len(shard.states))

    def allow(self, key: Hashable, cost: int = 1) -> Decision:
        """判定并（在通过时）扣额度。被拒时不消耗任何额度。"""
        now = self._clock()
        with self.reserve(key, now) as state:
            decision = state.try_acquire(now, cost)
        return replace(decision, rule=self._name) if self._name else decision

    def peek(self, key: Hashable, cost: int = 1) -> Decision:
        """只看不扣：仪表盘和响应头需要它，业务路径不该用它做"检查再动作"。"""
        now = self._clock()
        with self.reserve(key, now) as state:
            return state.check(now, cost)

    def reset(self, key: Hashable) -> None:
        """清掉一个 key 的全部状态（人工解封）。key 不存在也不报错。"""
        shard = self._shard_of(key)
        with shard.lock:
            shard.states.pop(key, None)

    def sweep(self) -> int:
        """显式扫一遍全部分片，返回回收掉的 key 数。一次只锁一个分片。"""
        now = self._clock()
        reclaimed = 0
        for shard in self._shards:
            with shard.lock:
                before = len(shard.states)
                self._purge(shard, now)
                reclaimed += before - len(shard.states)
        return reclaimed

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self._name!r}, tracked_keys={self.tracked_keys})"


@dataclass(frozen=True, slots=True)
class Rule(Generic[T]):
    """一条限流规则：给这个限流器喂哪个 key。`key_of` 从请求对象里抽出 key。"""

    name: str
    limiter: RateLimiter
    key_of: Callable[[T], Hashable]


class CompositeLimiter(Generic[T]):
    """多条规则同时生效（按用户 + 按接口 + 按 IP），任一条拒绝即整体拒绝。

    关键在于**两阶段**：先把所有规则的状态锁住并各自 `check`，全过才逐个 `commit`。
    否则一次被接口规则拒掉的请求，仍然白白扣掉了用户的额度——用户会发现自己没发出去的
    请求也在耗配额。规则顺序固定，因此所有线程按同一顺序拿锁，不会互相死锁；
    构造时拒绝同一个 `RateLimiter` 出现两次，正是为了守住这个顺序前提。
    """

    def __init__(self, rules: Sequence[Rule[T]], *, clock: Clock = time.monotonic) -> None:
        if not rules:
            raise InvalidConfiguration("a composite limiter needs at least one rule")
        if len({id(rule.limiter) for rule in rules}) != len(rules):
            raise InvalidConfiguration("each rule needs its own RateLimiter: lock order would depend on the key")
        self._rules = tuple(rules)
        self._clock = clock

    @property
    def rule_names(self) -> tuple[str, ...]:
        return tuple(rule.name for rule in self._rules)

    def allow(self, subject: T, cost: int = 1) -> Decision:
        """所有规则都放行才放行，并返回"最紧"的那条规则的结果。"""
        now = self._clock()
        with ExitStack() as stack:
            reserved: list[tuple[Rule[T], RateLimitAlgorithm, Decision]] = []
            for rule in self._rules:
                state = stack.enter_context(rule.limiter.reserve(rule.key_of(subject), now))
                decision = state.check(now, cost)
                if not decision.allowed:
                    return replace(decision, rule=rule.name)
                reserved.append((rule, state, decision))
            for _, state, _decision in reserved:
                state.commit(now, cost)
        tightest_rule, _, tightest = min(reserved, key=lambda item: item[2].remaining)
        return replace(tightest, rule=tightest_rule.name)


def _demo() -> None:
    now = [0.0]
    clock: Clock = lambda: now[0]

    # 边界突发：固定窗口在 t=9.9 和 t=10.1 各放 5 次，10 秒内实际放行 10 次 = 2 倍限额。
    fixed = RateLimiter(lambda: FixedWindowCounter(5, 10.0), clock=clock, name="fixed")
    sliding = RateLimiter(lambda: SlidingWindowCounter(5, 10.0), clock=clock, name="sliding")
    for limiter in (fixed, sliding):
        passed = 0
        for now[0] in (9.9,) * 5 + (10.1,) * 5:
            passed += bool(limiter.allow("alice"))
        print(f"{limiter.name:>8}: 10 次请求放行 {passed} 次")

    now[0] = 100.0
    bucket = RateLimiter(lambda: TokenBucket(60, 60.0, burst=5), clock=clock, name="bucket")
    for _ in range(5):
        bucket.allow("bob")
    print("令牌桶被拒时的 retry_after:", round(bucket.allow("bob").retry_after, 3), "秒")
    print("闲置前:", bucket.tracked_keys, end=" ")
    now[0] = 400.0
    print("→ 扫描回收:", bucket.sweep(), "→ 闲置后:", bucket.tracked_keys)


if __name__ == "__main__":
    _demo()
