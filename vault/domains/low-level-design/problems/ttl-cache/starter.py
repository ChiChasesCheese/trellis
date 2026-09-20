"""TTL 缓存练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。
内部表示随你换，但测试只会通过公开方法和只读属性断言，所以公开面不要改。
"""

from __future__ import annotations

import time
from collections.abc import Callable, Hashable, Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Generic, Protocol, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

Clock = Callable[[], float]


class CacheError(Exception):
    """本模块所有异常的根。"""


class InvalidConfiguration(CacheError, ValueError):
    """参数本身就不成立：非正的容量、非正的存活时间。"""


class EvictionReason(Enum):
    """一条数据离开缓存的原因。"""

    EXPIRED = "expired"
    CAPACITY = "capacity"
    REPLACED = "replaced"
    REMOVED = "removed"


@dataclass(frozen=True, slots=True)
class EvictionEvent(Generic[K, V]):
    """一条数据离开缓存这件事本身：事件带着值，监听者不必回头查缓存。"""

    key: K
    value: V
    reason: EvictionReason


@dataclass(frozen=True, slots=True)
class CacheStats:
    """某一瞬间的统计快照。"""

    hits: int
    misses: int
    expirations: int
    evictions: int
    loads: int

    @property
    def hit_rate(self) -> float:
        raise NotImplementedError


class ExpiryIndex(Generic[K]):
    """按截止时刻排序的小顶堆，支持改期与撤销——惰性删除加压实。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        """还有效的条目数。"""
        raise NotImplementedError

    @property
    def heap_size(self) -> int:
        """堆里实际占着内存的元素数（含墓碑）。"""
        raise NotImplementedError

    def push(self, key: K, deadline: float) -> None:
        """登记（或改期）一个 key 的截止时刻。"""
        raise NotImplementedError

    def discard(self, key: K) -> None:
        """撤销一个 key 的登记；不存在时什么都不做。"""
        raise NotImplementedError

    def pop_due(self, now: float) -> K | None:
        """弹出一个已到期的 key；没有就返回 None。"""
        raise NotImplementedError


class EvictionPolicy(Protocol[K]):
    """容量满时淘汰谁的规则。"""

    def record_insert(self, key: K, expires_at: float | None) -> None: ...

    def record_access(self, key: K) -> None: ...

    def remove(self, key: K) -> None: ...

    def evict(self) -> K: ...


class LRUPolicy(Generic[K]):
    """最近最少使用。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def record_insert(self, key: K, expires_at: float | None) -> None:
        raise NotImplementedError

    def record_access(self, key: K) -> None:
        raise NotImplementedError

    def remove(self, key: K) -> None:
        raise NotImplementedError

    def evict(self) -> K:
        raise NotImplementedError


class NearestDeadlinePolicy(Generic[K]):
    """先赶走本来就快过期的那条；没有存活时间的 key 之间退回 LRU。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def record_insert(self, key: K, expires_at: float | None) -> None:
        raise NotImplementedError

    def record_access(self, key: K) -> None:
        raise NotImplementedError

    def remove(self, key: K) -> None:
        raise NotImplementedError

    def evict(self) -> K:
        raise NotImplementedError


class TTLCache(Generic[K, V]):
    """固定容量 + 每条数据各自存活时间的缓存。"""

    def __init__(self, capacity: int, *, default_ttl: float | None = None,
                 clock: Clock = time.monotonic, policy: EvictionPolicy[K] | None = None,
                 refresh_on_access: bool = False) -> None:
        raise NotImplementedError

    @property
    def capacity(self) -> int:
        raise NotImplementedError

    @property
    def stats(self) -> CacheStats:
        """统计快照。"""
        raise NotImplementedError

    @property
    def expiry_heap_size(self) -> int:
        """到期索引实际占着的元素数。"""
        raise NotImplementedError

    @property
    def inflight_count(self) -> int:
        """正在回源的 key 数。"""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def keys(self) -> tuple[K, ...]:
        """当前存活 key 的快照。"""
        raise NotImplementedError

    def __contains__(self, key: K) -> bool:
        raise NotImplementedError

    def add_listener(self, listener: Callable[[EvictionEvent[K, V]], None]) -> None:
        """注册淘汰监听者。"""
        raise NotImplementedError

    def get(self, key: K) -> V:
        """取值；不存在或已过期抛 `KeyError`。"""
        raise NotImplementedError

    def put(self, key: K, value: V, ttl: float | None = None) -> None:
        """写入。"""
        raise NotImplementedError

    def delete(self, key: K) -> None:
        """主动删除。"""
        raise NotImplementedError

    def purge_expired(self) -> int:
        """显式清一遍到期条目，返回清掉的条数。"""
        raise NotImplementedError

    def get_or_load(self, key: K, loader: Callable[[], V], ttl: float | None = None) -> V:
        """取值；没有就回源。同一个 key 同时只有一个线程在回源。"""
        raise NotImplementedError

    def __getitem__(self, key: K) -> V:
        raise NotImplementedError

    def __setitem__(self, key: K, value: V) -> None:
        raise NotImplementedError

    def __delitem__(self, key: K) -> None:
        raise NotImplementedError

    def __iter__(self) -> Iterator[K]:
        raise NotImplementedError
