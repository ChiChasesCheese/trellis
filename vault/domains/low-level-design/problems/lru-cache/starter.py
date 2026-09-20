"""LRU / LFU 缓存：固定容量、O(1) 的 get/put。
设计：`Cache` 只管"key -> value"的存储与容量上限，把"淘汰哪个 key"整体委托给一个
可替换的 `EvictionPolicy`（LRU 与 LFU 各是一种实现，内部都基于手写的双向链表）。
线程安全与过期时间（TTL）各自是一层包装（装饰器），不改动 `Cache` 或策略的代码。
"""

from __future__ import annotations

import threading
import time
from collections.abc import Hashable
from typing import Callable, Generic, Protocol, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

Clock = Callable[[], float]


class _Node(Generic[K]):
    """双向链表节点，只存 key——值另外存在 `Cache._store` 里，链表只负责顺序。"""

    __slots__ = ("key", "prev", "next")

    def __init__(self, key: K | None = None) -> None:
        self.key = key
        self.prev: _Node[K] | None = None
        self.next: _Node[K] | None = None


class _DoublyLinkedList(Generic[K]):
    """带头尾哨兵节点的双向链表：append/remove/move_to_end/pop_front 都是 O(1)。

    这是 LRU 与 LFU 共用的底层积木——LRU 只用一条这样的链表；LFU 给每个频率各配一条。
    """

    def __init__(self) -> None:
        self._head: _Node[K] = _Node()
        self._tail: _Node[K] = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._nodes: dict[K, _Node[K]] = {}

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, key: K) -> bool:
        return key in self._nodes

    def append(self, key: K) -> None:
        """把 key 插到尾部（最近使用的一端）。key 必须尚不在链表里。"""
        raise NotImplementedError

    def remove(self, key: K) -> None:
        raise NotImplementedError

    def move_to_end(self, key: K) -> None:
        """把已经在链表里的 key 挪到尾部——用于"标记为最近使用"。"""
        raise NotImplementedError

    def pop_front(self) -> K:
        """弹出并返回头部（最久未使用的一端）的 key。链表为空时抛 IndexError。"""
        raise NotImplementedError


class EvictionPolicy(Protocol[K]):
    """淘汰策略的接口：`Cache` 只依赖这四个方法，不关心策略内部怎么记账。"""

    def record_insert(self, key: K) -> None:
        """记录一个新 key 被插入。"""
        ...

    def record_access(self, key: K) -> None:
        """记录一个已存在的 key 被访问（get 命中，或 put 更新了已有的 key）。"""
        ...

    def evict(self) -> K:
        """选出并移除一个受害者 key，返回它。调用前必须保证策略非空。"""
        ...

    def remove(self, key: K) -> None:
        """显式移除一个 key（不是通过淘汰——比如 TTL 层主动删除过期项）。"""
        ...

    def __len__(self) -> int:
        ...


class LRUPolicy(Generic[K]):
    """最近最少使用：一条双向链表，头部最旧、尾部最新，get/put 都把 key 挪到尾部。"""

    def __init__(self) -> None:
        self._order: _DoublyLinkedList[K] = _DoublyLinkedList()

    def record_insert(self, key: K) -> None:
        raise NotImplementedError

    def record_access(self, key: K) -> None:
        raise NotImplementedError

    def evict(self) -> K:
        raise NotImplementedError

    def remove(self, key: K) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._order)


class LFUPolicy(Generic[K]):
    """最不经常使用：频率 -> 该频率下的双向链表（桶内部按 LRU 排序，同频率淘汰最久未用的）。

    不变量：`_min_freq` 是当前非空桶中最小的那个频率，策略为空时为 0；`_buckets` 中只保留
    非空的桶——一个桶被搬空的瞬间就从字典里删除，绝不会常驻内存（否则一个被反复读的热 key
    会在自己身后留下成千上万个空链表对象）。`bucket_count` 把这条不变量暴露成一个可以在
    测试里断言的公开属性。
    """

    def __init__(self) -> None:
        self._freq_of: dict[K, int] = {}
        self._buckets: dict[int, _DoublyLinkedList[K]] = {}
        self._min_freq = 0

    @property
    def bucket_count(self) -> int:
        """当前存活（非空）的频率桶数量——只应等于当前有 key 存在的不同频率的个数。"""
        return len(self._buckets)

    def _detach(self, freq: int, key: K) -> None:
        """把 key 从它当前所在的桶里摘掉；桶因此变空时立刻删除该桶，并在它正是
        `_min_freq` 所在的桶时，把 `_min_freq` 重新算成"现存桶里最小的那个频率"。
        """
        raise NotImplementedError

    def record_insert(self, key: K) -> None:
        raise NotImplementedError

    def record_access(self, key: K) -> None:
        raise NotImplementedError

    def evict(self) -> K:
        raise NotImplementedError

    def remove(self, key: K) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._freq_of)


class Cache(Generic[K, V]):
    """固定容量的缓存：值存在 `dict` 里，淘汰顺序完全交给 `policy`。

    默认策略是 LRU——这是绝大多数场景的合理默认；传入 `LFUPolicy()` 就得到 LFU 缓存，
    `Cache` 本身一行都不用改，这正是"策略可插拔"要验证的地方。
    """

    def __init__(self, capacity: int, policy: EvictionPolicy[K] | None = None) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        self._capacity = capacity
        self._policy: EvictionPolicy[K] = policy if policy is not None else LRUPolicy()
        self._store: dict[K, V] = {}

    @property
    def capacity(self) -> int:
        return self._capacity

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: K) -> bool:
        """只探测是否存在，不算一次"使用"——否则连 `in` 都会改变淘汰顺序，太反直觉。"""
        return key in self._store

    def get(self, key: K) -> V:
        raise NotImplementedError

    def put(self, key: K, value: V) -> None:
        raise NotImplementedError

    def discard(self, key: K) -> None:
        """主动移除一个 key（不算淘汰）。key 不存在时抛 KeyError，语义对齐 dict 的 `del`。"""
        raise NotImplementedError

    def __getitem__(self, key: K) -> V:
        return self.get(key)

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        self.discard(key)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(capacity={self._capacity}, size={len(self._store)})"


class SynchronizedCache(Generic[K, V]):
    """给任意 `Cache` 包一层锁，不改动 `Cache` 或策略的任何代码。

    注意 `get` 在这里也要拿写锁：它会调用 `policy.record_access`，改写内部的链表/频率桶，
    所以对这个缓存而言 get 是一次"写"。读写锁在这里帮不上忙——几乎所有操作都要写内部结构，
    区分"读者"和"写者"没有意义，只会多一层管理读写锁本身的开销。
    """

    def __init__(self, cache: Cache[K, V]) -> None:
        self._cache = cache
        self._lock = threading.Lock()

    @property
    def capacity(self) -> int:
        return self._cache.capacity

    def get(self, key: K) -> V:
        raise NotImplementedError

    def put(self, key: K, value: V) -> None:
        raise NotImplementedError

    def discard(self, key: K) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, key: K) -> bool:
        raise NotImplementedError


class ExpiringCache(Generic[K, V]):
    """给任意 `Cache` 包一层按 key 的存活时间（TTL），时钟从外部注入以便测试可控可重放。

    每个 key 的过期时间单独存放在这一层（`_expires_at`），`Cache` 和 `EvictionPolicy`
    对 TTL 一无所知——过期只是"读到时发现太旧就当作不存在，并顺手删掉"。
    """

    def __init__(self, cache: Cache[K, V], ttl_seconds: float, clock: Clock = time.monotonic) -> None:
        if ttl_seconds <= 0:
            raise ValueError(f"ttl_seconds must be positive, got {ttl_seconds}")
        self._cache = cache
        self._ttl = ttl_seconds
        self._clock = clock
        self._expires_at: dict[K, float] = {}

    def _is_expired(self, key: K) -> bool:
        deadline = self._expires_at.get(key)
        return deadline is not None and self._clock() >= deadline

    def _expire_now(self, key: K) -> None:
        self._cache.discard(key)
        del self._expires_at[key]

    def get(self, key: K) -> V:
        raise NotImplementedError

    def put(self, key: K, value: V) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key: K) -> bool:
        return key in self._cache and not self._is_expired(key)


def _demo() -> None:
    cache: Cache[str, int] = Cache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    print("lru 剩余:", dict(sorted(((k, cache[k]) for k in ("a", "c")))))


if __name__ == "__main__":
    _demo()
