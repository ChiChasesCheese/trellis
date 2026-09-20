"""内存键值存储练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。
内部表示随你换，但测试只会通过公开方法和只读属性断言，所以公开面不要改。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


class KVStoreError(Exception):
    """本设计所有失败路径的公共基类。"""


class KeyNotFoundError(KVStoreError):
    """key 不存在，或者它的字段已经全部过期/被删空了。"""


class FieldNotFoundError(KVStoreError):
    """字段不存在，或者已经过期——对调用方来说这两者没有区别。"""


class InvalidTTLError(KVStoreError):
    """存活时间不是正数。"""


class NoActiveTransactionError(KVStoreError):
    """在没有对应 `begin` 的情况下调用了 `commit` 或 `rollback`。"""


@dataclass(frozen=True, slots=True)
class Slot:
    """一个字段的当前取值：值本身，加上它自己的绝对过期时刻。"""

    value: str
    expires_at: int | None


class KVStore:
    """字段表加撤销日志。见 `solution.py` 的类文档字符串了解每一关对应哪些方法。"""

    def __init__(self) -> None:
        self._fields: dict[str, dict[str, Slot]] = {}
        self._key_expiry: dict[str, int] = {}
        self._frames: list[list[Callable[[], None]]] = []

    # ---------- 只读视图 ----------

    @property
    def transaction_depth(self) -> int:
        raise NotImplementedError

    @property
    def expiring_key_count(self) -> int:
        raise NotImplementedError

    def key_count(self, timestamp: int) -> int:
        raise NotImplementedError

    # ---------- 第 1 关：基本读写 ----------

    def set(self, timestamp: int, key: str, field: str, value: str, ttl: int | None = None) -> None:
        raise NotImplementedError

    def get(self, timestamp: int, key: str, field: str) -> str:
        raise NotImplementedError

    def delete(self, timestamp: int, key: str, field: str) -> None:
        raise NotImplementedError

    def count_by_field_value(self, timestamp: int, field: str, value: str) -> int:
        raise NotImplementedError

    # ---------- 第 2 关：扫描 ----------

    def scan_prefix(self, timestamp: int, prefix: str) -> list[str]:
        raise NotImplementedError

    def fields(self, timestamp: int, key: str) -> list[str]:
        raise NotImplementedError

    # ---------- 第 3 关：key 级 TTL ----------

    def expire_key(self, timestamp: int, key: str, ttl: int) -> None:
        raise NotImplementedError

    # ---------- 第 4 关：嵌套事务 ----------

    def begin(self) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError
