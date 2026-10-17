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
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError

    def on_insert(self, key: str) -> None:
        raise NotImplementedError

    def on_access(self, key: str) -> None:
        raise NotImplementedError

    def on_remove(self, key: str) -> None:
        raise NotImplementedError

    def victim(self) -> str:
        raise NotImplementedError


class LfuPolicy:
    """最不经常使用：按访问次数分桶，桶内按插入先后；同频时淘汰最久没动的（退化为 LRU）。

    `_min` 指向最小的非空桶（0 表示"刚被删空、还没重算"），所以 victim 通常是 O(1)；淘汰之后紧跟着插入，
    `_min` 立刻回到 1，重算只会在过期删除之后遇到。桶一旦空了立即删除——否则桶表会无限增长。
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, key: object) -> bool:
        raise NotImplementedError

    @property
    def bucket_count(self) -> int:
        """当前非空频率桶的个数（回归测试用：空桶必须被回收）。"""
        raise NotImplementedError

    def _detach(self, key: str) -> int:
        """把 key 从它当前的频率桶里摘出来，空桶当场删除；返回它原来的频率。"""
        raise NotImplementedError

    def _attach(self, key: str, freq: int) -> None:
        raise NotImplementedError

    def on_insert(self, key: str) -> None:
        raise NotImplementedError

    def on_access(self, key: str) -> None:
        raise NotImplementedError

    def on_remove(self, key: str) -> None:
        raise NotImplementedError

    def victim(self) -> str:
        raise NotImplementedError


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
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def get(self, key: str) -> Any:
        raise NotImplementedError

    def put(self, key: str, value: Any) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


class FileStore:
    """文件后端：目录里一个 key 一个 JSON 文件，文件名是 key 的 sha256（key 里的 `/`、`..` 无法逃出目录）。

    写入先写临时文件再 `os.replace`：失败时旧文件原封不动，不会留下写了一半的值。
    值必须能被 JSON 序列化；不能的话在碰磁盘之前就抛 StoreError。
    """

    def __init__(self, directory: Path) -> None:
        raise NotImplementedError

    def _path(self, key: str) -> Path:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def get(self, key: str) -> Any:
        raise NotImplementedError

    def put(self, key: str, value: Any) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


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
    raise NotImplementedError


@dataclass(frozen=True, slots=True)
class CacheStats:
    """某一时刻的计数快照（冻结，调用方拿到后不会被后续操作改动）。"""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def hit_rate(self) -> float:
        raise NotImplementedError


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
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    @property
    def store_size(self) -> int:
        """存储后端里实际有多少条（不变量检查用：必须等于 len(cache)）。"""
        raise NotImplementedError

    @property
    def stats(self) -> CacheStats:
        raise NotImplementedError

    def _drop(self, key: str) -> None:
        """删除一个 key：先删存储（可能失败），成功后策略与过期表才忘记它。"""
        raise NotImplementedError

    def _live(self, key: str) -> bool:
        """key 是否存在且未过期；过期的当场清掉。"""
        raise NotImplementedError

    def get(self, key: str, default: Any = None) -> Any:
        raise NotImplementedError

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        raise NotImplementedError

    def _make_room(self, new_key: str) -> None:
        """容量已满时淘汰一个。此时新值已写进 store，所以删旧值失败要把新值也撤回。"""
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        raise NotImplementedError


def create_cache(config: CacheConfig, clock: Clock = time.monotonic) -> Cache:
    """按配置组装：名字查注册表，找不到就报 ConfigError。新增一种策略或后端只改注册表。"""
    raise NotImplementedError
