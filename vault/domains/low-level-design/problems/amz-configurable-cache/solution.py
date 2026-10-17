"""可配置缓存（Configurable Cache）：淘汰策略与存储后端是两条互相独立的变化轴。
设计：`Cache` 只管"一次读写的流程、容量上限、过期时间、统计、锁"，它不知道谁被淘汰，也不知道数据放哪。
"淘汰谁"交给 `EvictionPolicy`（`LruPolicy` / `LfuPolicy`，只记元数据、不存值），"数据放哪"交给 `Store`
（`MemoryStore` / `FileStore`，只存值、不懂顺序）。两个接口互不引用，所以 2 种策略 x 2 种后端只写
4 个小类，而不是 4 个组合类；`CacheConfig` + `create_cache` 把名字（"lru"、"file"）翻译成对象。
一致性规则：先写存储（会失败的那一步），成功之后才动策略；淘汰同理，存储删除成功才让策略忘记。
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

Clock = Callable[[], float]


class CacheError(Exception):
    """本组件所有失败的共同基类。"""


class ConfigError(CacheError, ValueError):
    """配置不合法：容量非正、名字不认识、文件后端没给目录、目录里已有数据。"""


class StoreError(CacheError):
    """存储后端读写失败（磁盘错误、值不能序列化、文件损坏）。缓存把它原样抛给调用方。"""


class EmptyPolicyError(CacheError, LookupError):
    """策略里一个 key 都没有时问"该淘汰谁"。"""


# ---------------------------------------------------------------- 淘汰策略


class EvictionPolicy(Protocol):
    """淘汰策略只维护"key 的使用顺序 / 次数"，从不持有值。四个动作足以表达 LRU、LFU、FIFO。"""

    def __len__(self) -> int: ...
    def __contains__(self, key: object) -> bool: ...
    def on_insert(self, key: str) -> None: ...
    def on_access(self, key: str) -> None: ...
    def on_remove(self, key: str) -> None: ...
    def victim(self) -> str: ...


class LruPolicy:
    """最近最少使用：OrderedDict 的顺序就是使用顺序，队首是最久没用的，所有操作 O(1)。"""

    def __init__(self) -> None:
        self._order: OrderedDict[str, None] = OrderedDict()

    def __len__(self) -> int:
        return len(self._order)

    def __contains__(self, key: object) -> bool:
        return key in self._order

    def on_insert(self, key: str) -> None:
        self._order[key] = None
        self._order.move_to_end(key)

    def on_access(self, key: str) -> None:
        self._order.move_to_end(key)

    def on_remove(self, key: str) -> None:
        self._order.pop(key, None)

    def victim(self) -> str:
        if not self._order:
            raise EmptyPolicyError("no key to evict")
        return next(iter(self._order))


class LfuPolicy:
    """最不经常使用：按访问次数分桶，桶内按插入先后；同频时淘汰最久没动的（退化为 LRU）。

    `_min` 指向最小的非空桶（0 表示"刚被删空、还没重算"），所以 victim 通常是 O(1)；淘汰之后紧跟着插入，
    `_min` 立刻回到 1，重算只会在过期删除之后遇到。桶一旦空了立即删除——否则桶表会无限增长。
    """

    def __init__(self) -> None:
        self._freq: dict[str, int] = {}
        self._buckets: dict[int, OrderedDict[str, None]] = {}
        self._min = 0

    def __len__(self) -> int:
        return len(self._freq)

    def __contains__(self, key: object) -> bool:
        return key in self._freq

    @property
    def bucket_count(self) -> int:
        """当前非空频率桶的个数（回归测试用：空桶必须被回收）。"""
        return len(self._buckets)

    def _detach(self, key: str) -> int:
        """把 key 从它当前的频率桶里摘出来，空桶当场删除；返回它原来的频率。"""
        freq = self._freq[key]
        bucket = self._buckets[freq]
        del bucket[key]
        if not bucket:
            del self._buckets[freq]
        return freq

    def _attach(self, key: str, freq: int) -> None:
        self._freq[key] = freq
        self._buckets.setdefault(freq, OrderedDict())[key] = None

    def on_insert(self, key: str) -> None:
        self.on_remove(key)
        self._attach(key, 1)
        self._min = 1

    def on_access(self, key: str) -> None:
        freq = self._detach(key)
        self._attach(key, freq + 1)
        if freq == self._min and freq not in self._buckets:
            self._min = freq + 1             # 刚摘空的就是最小桶：新桶 freq+1 顶上

    def on_remove(self, key: str) -> None:
        if key not in self._freq:
            return
        freq = self._detach(key)
        del self._freq[key]
        if freq == self._min and freq not in self._buckets:
            self._min = 0                    # 最小桶空了：先标记"未知"，真被问到受害者时再找

    def victim(self) -> str:
        if not self._freq:
            raise EmptyPolicyError("no key to evict")
        if not self._min:
            self._min = min(self._buckets)   # 只在"删除之后、插入之前"被问到才会走到这里
        return next(iter(self._buckets[self._min]))


# ---------------------------------------------------------------- 存储后端


class Store(Protocol):
    """存储后端只负责"按 key 存取值"，不知道容量、顺序和过期。`delete` 对不存在的 key 是空操作。"""

    def __len__(self) -> int: ...
    def get(self, key: str) -> Any: ...
    def put(self, key: str, value: Any) -> None: ...
    def delete(self, key: str) -> None: ...


class MemoryStore:
    """内存后端：一个 dict。get 缺 key 抛 KeyError。"""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def __len__(self) -> int:
        return len(self._data)

    def get(self, key: str) -> Any:
        return self._data[key]

    def put(self, key: str, value: Any) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)


class FileStore:
    """文件后端：目录里一个 key 一个 JSON 文件，文件名是 key 的 sha256（key 里的 `/`、`..` 无法逃出目录）。

    写入先写临时文件再 `os.replace`：失败时旧文件原封不动，不会留下写了一半的值。
    值必须能被 JSON 序列化；不能的话在碰磁盘之前就抛 StoreError。
    """

    def __init__(self, directory: Path) -> None:
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        return self._dir / (hashlib.sha256(key.encode()).hexdigest() + ".json")

    def __len__(self) -> int:
        return sum(1 for _ in self._dir.glob("*.json"))

    def get(self, key: str) -> Any:
        try:
            return json.loads(self._path(key).read_text(encoding="utf-8"))["value"]
        except FileNotFoundError:
            raise KeyError(key) from None
        except (OSError, ValueError, KeyError) as exc:
            raise StoreError(f"cannot read {key!r}: {exc}") from exc

    def put(self, key: str, value: Any) -> None:
        try:
            body = json.dumps({"key": key, "value": value})
        except (TypeError, ValueError) as exc:
            raise StoreError(f"value for {key!r} is not JSON-serialisable: {exc}") from exc
        try:
            fd, tmp = tempfile.mkstemp(dir=self._dir, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(body)
            os.replace(tmp, self._path(key))
        except OSError as exc:
            raise StoreError(f"cannot write {key!r}: {exc}") from exc

    def delete(self, key: str) -> None:
        try:
            self._path(key).unlink(missing_ok=True)
        except OSError as exc:
            raise StoreError(f"cannot delete {key!r}: {exc}") from exc


# ---------------------------------------------------------------- 配置与工厂


@dataclass(frozen=True, slots=True)
class CacheConfig:
    """一份缓存的全部旋钮。`eviction` / `backend` 是注册表里的名字；`path` 只有文件后端用。"""

    capacity: int
    eviction: str = "lru"
    backend: str = "memory"
    path: Path | None = None
    default_ttl: float | None = None


POLICIES: dict[str, Callable[[], EvictionPolicy]] = {"lru": LruPolicy, "lfu": LfuPolicy}
BACKENDS: dict[str, Callable[[CacheConfig], Store]] = {
    "memory": lambda cfg: MemoryStore(),
    "file": lambda cfg: FileStore(_need_path(cfg)),
}


def _need_path(cfg: CacheConfig) -> Path:
    if cfg.path is None:
        raise ConfigError("file backend needs a path")
    return cfg.path


@dataclass(frozen=True, slots=True)
class CacheStats:
    """某一时刻的计数快照（冻结，调用方拿到后不会被后续操作改动）。"""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


# ---------------------------------------------------------------- 缓存本体


class Cache:
    """缓存：编排策略与后端，自己只守三条不变量。

    1. `len(policy) <= capacity`，且 policy 里的 key 集合 == store 里的 key 集合（每次操作返回时成立）。
    2. 先动会失败的一方（store），成功后才动 policy；失败时两边都停在操作之前的状态。
    3. 过期的 key 对外等同于不存在：读到就当场清掉，并计入 expirations。
    一把粗粒度锁包住每个公开操作——文件 IO 也在锁内，吞吐换正确性（见题解"并发"一节）。
    """

    def __init__(self, capacity: int, policy: EvictionPolicy, store: Store,
                 clock: Clock = time.monotonic, default_ttl: float | None = None) -> None:
        if capacity <= 0:
            raise ConfigError(f"capacity must be positive, got {capacity}")
        if len(store) != 0:
            raise ConfigError("store must be empty: the policy cannot know keys it never saw")
        self._capacity = capacity
        self._policy = policy
        self._store = store
        self._clock = clock
        self._default_ttl = default_ttl
        self._expires: dict[str, float] = {}
        self._hits = self._misses = self._evictions = self._expirations = 0
        self._lock = threading.Lock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._policy)

    @property
    def store_size(self) -> int:
        """存储后端里实际有多少条（不变量检查用：必须等于 len(cache)）。"""
        with self._lock:
            return len(self._store)

    @property
    def stats(self) -> CacheStats:
        with self._lock:
            return CacheStats(self._hits, self._misses, self._evictions, self._expirations)

    def _drop(self, key: str) -> None:
        """删除一个 key：先删存储（可能失败），成功后策略与过期表才忘记它。"""
        self._store.delete(key)
        self._policy.on_remove(key)
        self._expires.pop(key, None)

    def _live(self, key: str) -> bool:
        """key 是否存在且未过期；过期的当场清掉。"""
        if key not in self._policy:
            return False
        deadline = self._expires.get(key)
        if deadline is not None and self._clock() >= deadline:
            self._drop(key)
            self._expirations += 1
            return False
        return True

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            if not self._live(key):
                self._misses += 1
                return default
            value = self._store.get(key)
            self._policy.on_access(key)
            self._hits += 1
            return value

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        ttl = self._default_ttl if ttl is None else ttl
        with self._lock:
            exists = self._live(key)
            self._store.put(key, value)             # 会失败的一步放最前：失败则什么都没变
            if exists:
                self._policy.on_access(key)
            else:
                self._make_room(key)
                self._policy.on_insert(key)
            if ttl is None:
                self._expires.pop(key, None)
            else:
                self._expires[key] = self._clock() + ttl

    def _make_room(self, new_key: str) -> None:
        """容量已满时淘汰一个。此时新值已写进 store，所以删旧值失败要把新值也撤回。"""
        if len(self._policy) < self._capacity:
            return
        victim = self._policy.victim()
        try:
            self._drop(victim)
        except StoreError:
            self._store.delete(new_key)
            raise
        self._evictions += 1

    def delete(self, key: str) -> bool:
        with self._lock:
            if not self._live(key):
                return False
            self._drop(key)
            return True


def create_cache(config: CacheConfig, clock: Clock = time.monotonic) -> Cache:
    """按配置组装：名字查注册表，找不到就报 ConfigError。新增一种策略或后端只改注册表。"""
    if config.eviction not in POLICIES:
        raise ConfigError(f"unknown eviction policy {config.eviction!r}; known: {sorted(POLICIES)}")
    if config.backend not in BACKENDS:
        raise ConfigError(f"unknown backend {config.backend!r}; known: {sorted(BACKENDS)}")
    return Cache(config.capacity, POLICIES[config.eviction](), BACKENDS[config.backend](config),
                 clock, config.default_ttl)


if __name__ == "__main__":
    cache = create_cache(CacheConfig(capacity=2, eviction="lfu"))
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)                      # 满了：a 被用了 2 次，b 只有 1 次 -> 淘汰 b
    print(cache.get("a"), cache.get("b"), cache.get("c"), cache.stats)
