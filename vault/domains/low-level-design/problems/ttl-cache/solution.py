"""带过期时间的缓存（TTL Cache）：每条数据各自的存活时间 + 容量满时的淘汰策略。
设计：`_Entry` 存值和它的绝对截止时刻；`ExpiryIndex` 是一个带惰性删除与压实的到期小顶堆，
让"清掉所有到期条目"的代价与到期条目数成正比，而不是与缓存大小成正比；
"容量满了淘汰谁"是可替换的 `EvictionPolicy`（LRU 或"最近就要过期的先走"）；
`TTLCache` 只负责把这三者缝起来：一把锁、一份统计、一组淘汰事件监听者，
外加一个单飞（single-flight）加载入口，让一百个线程同时缓存未命中时只回源一次。
"""

from __future__ import annotations

import heapq
import itertools
import math
import threading
import time
from collections import OrderedDict
from collections.abc import Callable, Hashable, Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Generic, Protocol, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

Clock = Callable[[], float]
"""时钟：返回单调秒数的无参函数，永远从外部注入。"""

_REMOVED = object()
"""堆里的墓碑（tombstone）标记：条目还在堆里，但已经不作数了。"""

_COMPACT_FLOOR = 32
"""墓碑少于这个数时不值得为压实重建整个堆。"""


class CacheError(Exception):
    """本模块所有异常的根。"""


class InvalidConfiguration(CacheError, ValueError):
    """参数本身就不成立：非正的容量、非正的存活时间。"""


class EvictionReason(Enum):
    """一条数据离开缓存的原因——监听者几乎总是要按原因分别处理。"""

    EXPIRED = "expired"      # 活到期了
    CAPACITY = "capacity"    # 容量满，被淘汰策略选中
    REPLACED = "replaced"    # 同一个 key 被写了新值
    REMOVED = "removed"      # 调用方主动删除


@dataclass(frozen=True, slots=True)
class EvictionEvent(Generic[K, V]):
    """一条数据离开缓存这件事本身。

    事件带着值，监听者因此能直接释放它持有的资源（关连接、删临时文件），
    而不必回头去缓存里查——那时它已经查不到了，并且回查会绕过缓存的锁。
    """

    key: K
    value: V
    reason: EvictionReason


@dataclass(frozen=True, slots=True)
class CacheStats:
    """某一瞬间的统计快照。不可变，所以拿到它之后读到的数字不会自己变。"""

    hits: int
    misses: int
    expirations: int
    evictions: int
    loads: int

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


@dataclass(frozen=True, slots=True)
class _Entry(Generic[V]):
    """一条数据：值、绝对截止时刻（None 表示永不过期）、以及原始的存活时间。

    存**绝对时刻**而不是"还剩多久"，是因为后者需要有人定期去减，那又要一个后台线程。
    保留 `ttl` 只为了支持"读一次就续一次命"。
    """

    value: V
    expires_at: float | None
    ttl: float | None

    def is_expired(self, now: float) -> bool:
        return self.expires_at is not None and now >= self.expires_at


class ExpiryIndex(Generic[K]):
    """按截止时刻排序的小顶堆，支持"改期"和"撤销"——用惰性删除加压实实现。

    堆没有"删掉中间某个元素"的操作，标准做法（`heapq` 文档里的配方）是把旧条目标成墓碑，
    弹出时跳过。代价是墓碑会堆积：一个被反复覆写的 key 能在堆里留下几十万个死条目，
    于是"缓存只有 1000 条"的承诺被一个内部结构悄悄毁掉。所以墓碑超过一半时必须**压实**。

    元组的第二项是一个自增序号：它保证比较永远不会落到第三项的 key 上（key 可能不可比较），
    同时给同一时刻到期的条目一个稳定的先后顺序。
    """

    def __init__(self) -> None:
        self._heap: list[list[object]] = []
        self._entries: dict[K, list[object]] = {}
        self._counter = itertools.count()
        self._stale = 0

    def __len__(self) -> int:
        """还有效的条目数。"""
        return len(self._entries)

    @property
    def heap_size(self) -> int:
        """堆里实际占着内存的元素数（含墓碑）——压实做得对，它不会无限增长。"""
        return len(self._heap)

    def push(self, key: K, deadline: float) -> None:
        """登记（或改期）一个 key 的截止时刻。"""
        self.discard(key)
        entry: list[object] = [deadline, next(self._counter), key]
        self._entries[key] = entry
        heapq.heappush(self._heap, entry)

    def discard(self, key: K) -> None:
        """撤销一个 key 的登记。key 不在索引里时什么都不做。"""
        entry = self._entries.pop(key, None)
        if entry is None:
            return
        entry[2] = _REMOVED
        self._stale += 1
        if self._stale > _COMPACT_FLOOR and self._stale * 2 > len(self._heap):
            self._compact()

    def pop_due(self, now: float) -> K | None:
        """弹出一个在 `now` 之前（含）到期的 key；没有就返回 None，堆顶原样留着。"""
        while self._heap:
            deadline, _, key = self._heap[0]
            if key is _REMOVED:
                heapq.heappop(self._heap)
                self._stale -= 1
                continue
            if deadline > now:  # type: ignore[operator]
                return None
            heapq.heappop(self._heap)
            del self._entries[key]  # type: ignore[arg-type]
            return key  # type: ignore[return-value]
        return None

    def _compact(self) -> None:
        """把墓碑一次性清出去并重建堆。O(n)，但摊到制造这些墓碑的 n/2 次操作上是 O(1)。"""
        self._heap = [entry for entry in self._heap if entry[2] is not _REMOVED]
        heapq.heapify(self._heap)
        self._stale = 0


class EvictionPolicy(Protocol[K]):
    """容量满时"淘汰谁"的规则。缓存只依赖这四个方法，不关心它内部怎么记账。

    `record_insert` 收下截止时刻，是因为"什么时候会死"本就是"该让谁先走"的合法输入；
    LRU 选择无视它，那是 LRU 的决定，不是接口的泄漏。
    """

    def record_insert(self, key: K, expires_at: float | None) -> None: ...

    def record_access(self, key: K) -> None: ...

    def remove(self, key: K) -> None: ...

    def evict(self) -> K:
        """选出并移除一个受害者。调用前必须保证非空。"""
        ...


class LRUPolicy(Generic[K]):
    """最近最少使用。顺序用 `OrderedDict` 维护——本题要考的是 TTL，不是手写双向链表。"""

    def __init__(self) -> None:
        self._order: OrderedDict[K, None] = OrderedDict()

    def record_insert(self, key: K, expires_at: float | None) -> None:
        self._order[key] = None

    def record_access(self, key: K) -> None:
        self._order.move_to_end(key)

    def remove(self, key: K) -> None:
        self._order.pop(key, None)

    def evict(self) -> K:
        key, _ = self._order.popitem(last=False)
        return key


class NearestDeadlinePolicy(Generic[K]):
    """先赶走"本来就快过期"的那条：反正它马上要死，淘汰它损失的未来命中最少。

    没有设置存活时间的 key 不在堆里，它们之间退回 LRU——一条永不过期的数据没有
    "快死了"这个属性，硬给它编一个截止时刻只会把策略变得难以解释。
    """

    def __init__(self) -> None:
        self._deadlines: ExpiryIndex[K] = ExpiryIndex()
        self._eternal: LRUPolicy[K] = LRUPolicy()

    def record_insert(self, key: K, expires_at: float | None) -> None:
        if expires_at is None:
            self._eternal.record_insert(key, None)
        else:
            self._deadlines.push(key, expires_at)

    def record_access(self, key: K) -> None:
        """读一次不改变"谁先死"——这正是它和 LRU 的根本区别。"""

    def remove(self, key: K) -> None:
        self._deadlines.discard(key)
        self._eternal.remove(key)

    def evict(self) -> K:
        key = self._deadlines.pop_due(math.inf)
        return key if key is not None else self._eternal.evict()


class TTLCache(Generic[K, V]):
    """固定容量 + 每条数据各自存活时间的缓存。

    过期是**惰性 + 索引驱动**的：任何一次操作都先把到期堆顶所有该死的条目清掉，
    代价只和"这段时间里到期了几条"成正比。于是一条写进来就再没人读过的数据，
    同样会在到期后被回收——这是纯惰性方案做不到、而定时全表扫描要 O(n) 才能做到的事。
    `__len__` 和 `keys()` 因此永远看不到"过期但还没被删"的条目。
    """

    def __init__(self, capacity: int, *, default_ttl: float | None = None,
                 clock: Clock = time.monotonic, policy: EvictionPolicy[K] | None = None,
                 refresh_on_access: bool = False) -> None:
        if capacity <= 0:
            raise InvalidConfiguration(f"capacity must be positive, got {capacity}")
        if default_ttl is not None and default_ttl <= 0:
            raise InvalidConfiguration(f"default_ttl must be positive, got {default_ttl}")
        self._capacity = capacity
        self._default_ttl = default_ttl
        self._clock = clock
        self._refresh_on_access = refresh_on_access
        self._policy: EvictionPolicy[K] = policy if policy is not None else LRUPolicy()
        self._store: dict[K, _Entry[V]] = {}
        self._expiry: ExpiryIndex[K] = ExpiryIndex()
        self._lock = threading.Lock()
        self._inflight: dict[K, threading.Event] = {}
        self._listeners: list[Callable[[EvictionEvent[K, V]], None]] = []
        self._hits = self._misses = self._expirations = self._evictions = self._loads = 0

    # ---------- 只读视图 ----------

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def stats(self) -> CacheStats:
        """统计快照。返回不可变对象，而不是内部计数器字典。"""
        with self._lock:
            return CacheStats(self._hits, self._misses, self._expirations,
                              self._evictions, self._loads)

    @property
    def expiry_heap_size(self) -> int:
        """到期索引实际占着的元素数——用来断言墓碑没有无限堆积。"""
        with self._lock:
            return self._expiry.heap_size

    @property
    def inflight_count(self) -> int:
        """正在回源的 key 数。加载结束后必须归零，否则这也是一处泄漏。"""
        with self._lock:
            return len(self._inflight)

    def __len__(self) -> int:
        events = self._sweep()
        self._publish(events)
        with self._lock:
            return len(self._store)

    def keys(self) -> tuple[K, ...]:
        """当前存活 key 的**快照**（不是内部视图），顺序不保证。"""
        self._publish(self._sweep())
        with self._lock:
            return tuple(self._store)

    def __contains__(self, key: K) -> bool:
        self._publish(self._sweep())
        with self._lock:
            return key in self._store

    def add_listener(self, listener: Callable[[EvictionEvent[K, V]], None]) -> None:
        """注册淘汰监听者。它在锁**之外**被调用，所以慢回调不会堵住整个缓存。"""
        with self._lock:
            self._listeners.append(listener)

    # ---------- 核心操作 ----------

    def get(self, key: K) -> V:
        """取值。key 不存在或已过期一律抛 `KeyError`——语义对齐 `dict`。"""
        now = self._clock()
        with self._lock:
            events = self._purge_locked(now)
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
            else:
                self._hits += 1
                self._policy.record_access(key)
                if self._refresh_on_access and entry.ttl is not None:
                    self._store[key] = _Entry(entry.value, now + entry.ttl, entry.ttl)
                    self._expiry.push(key, now + entry.ttl)
        self._publish(events)
        if entry is None:
            raise KeyError(key)
        return entry.value

    def put(self, key: K, value: V, ttl: float | None = None) -> None:
        """写入。`ttl` 省略时用构造时的默认值；默认值也是 None 就永不过期。"""
        now = self._clock()
        ttl = self._default_ttl if ttl is None else ttl
        if ttl is not None and ttl <= 0:
            raise InvalidConfiguration(f"ttl must be positive, got {ttl}")
        expires_at = None if ttl is None else now + ttl
        with self._lock:
            events = self._purge_locked(now)
            if key in self._store:
                events.append(self._drop_locked(key, EvictionReason.REPLACED))
            elif len(self._store) >= self._capacity:
                events.append(self._drop_locked(self._policy.evict(), EvictionReason.CAPACITY))
                self._evictions += 1
            self._store[key] = _Entry(value, expires_at, ttl)
            self._policy.record_insert(key, expires_at)
            if expires_at is not None:
                self._expiry.push(key, expires_at)
        self._publish(events)

    def delete(self, key: K) -> None:
        """主动删除。key 不存在（或已过期）时抛 `KeyError`。"""
        now = self._clock()
        with self._lock:
            events = self._purge_locked(now)
            missing = key not in self._store
            if not missing:
                events.append(self._drop_locked(key, EvictionReason.REMOVED))
        self._publish(events)
        if missing:
            raise KeyError(key)

    def purge_expired(self) -> int:
        """显式清一遍到期条目，返回清掉的条数。给"定时主动清理"那条路径用。"""
        events = self._sweep()
        self._publish(events)
        return len(events)

    def get_or_load(self, key: K, loader: Callable[[], V], ttl: float | None = None) -> V:
        """取值；没有就调用 `loader` 回源。同一个 key 同时只有一个线程在回源（单飞）。

        没有这道闸，热点 key 一过期，所有在读它的线程会同时打到后端——这就是缓存踩踏
        （cache stampede）。后到的线程在 `Event` 上等，领跑者**先写进缓存再唤醒**他们，
        于是他们醒来就是命中，不会第二次回源。
        """
        while True:
            try:
                return self.get(key)
            except KeyError:
                pass
            with self._lock:
                waiter = self._inflight.get(key)
                leader = waiter is None
                if leader:
                    waiter = self._inflight[key] = threading.Event()
            if not leader:
                waiter.wait()
                continue
            try:
                value = loader()
                self.put(key, value, ttl)
                with self._lock:
                    self._loads += 1
                return value
            finally:
                with self._lock:
                    done = self._inflight.pop(key)  # 无论成败都要移交，否则后来者永远等下去
                done.set()

    # ---------- 内部：过期与移除 ----------

    def _sweep(self) -> list[EvictionEvent[K, V]]:
        now = self._clock()
        with self._lock:
            return self._purge_locked(now)

    def _purge_locked(self, now: float) -> list[EvictionEvent[K, V]]:
        """（持锁）把所有到期条目摘掉，返回待广播的事件。"""
        events: list[EvictionEvent[K, V]] = []
        while (key := self._expiry.pop_due(now)) is not None:
            events.append(self._drop_locked(key, EvictionReason.EXPIRED))
            self._expirations += 1
        return events

    def _drop_locked(self, key: K, reason: EvictionReason) -> EvictionEvent[K, V]:
        """（持锁）把一个 key 从存储、策略、到期索引里一并摘掉，并造出事件。"""
        entry = self._store.pop(key)
        self._policy.remove(key)
        self._expiry.discard(key)
        return EvictionEvent(key, entry.value, reason)

    def _publish(self, events: list[EvictionEvent[K, V]]) -> None:
        """在锁外广播。监听者是外部代码，持锁回调它等于把锁交给不认识的人。"""
        if not events:
            return
        with self._lock:
            listeners = tuple(self._listeners)
        for event in events:
            for listener in listeners:
                listener(event)

    # ---------- 语法糖 ----------

    def __getitem__(self, key: K) -> V:
        return self.get(key)

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def __iter__(self) -> Iterator[K]:
        return iter(self.keys())

    def __repr__(self) -> str:
        return f"{type(self).__name__}(capacity={self._capacity}, size={len(self._store)})"


def _demo() -> None:
    now = [0.0]
    clock: Clock = lambda: now[0]
    cache: TTLCache[str, int] = TTLCache(capacity=3, default_ttl=10.0, clock=clock)
    cache.add_listener(lambda event: print(f"  ← {event.key} 离开，原因 {event.reason.value}"))

    cache.put("a", 1)
    cache.put("b", 2, ttl=2.0)
    cache.put("c", 3)
    now[0] = 3.0
    print("b 还在吗:", "b" in cache, "／存活条数:", len(cache))

    cache.put("d", 4)
    cache.put("e", 5)          # 容量 3，最久未用的被淘汰
    print("剩下:", sorted(cache.keys()))

    hits = TTLCache[str, int](capacity=2, clock=clock)
    hits.put("x", 1)
    hits.get("x")
    try:
        hits.get("y")
    except KeyError:
        pass
    print("命中率:", hits.stats.hit_rate)


if __name__ == "__main__":
    _demo()
