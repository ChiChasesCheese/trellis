"""增删查最近值练习骨架：公开 API 与 `solution.py` 完全一致，方法体全部待补全。
把每个 `raise NotImplementedError` 换成你自己的实现，然后用
`IMPL=starter uv run --with pytest python -m pytest <本目录> -q` 验收。
内部表示随你换，测试只通过公开方法断言。"""
from __future__ import annotations
import bisect
import enum
import threading
from collections.abc import Iterator
from typing import Protocol
MAX_SPAN = 5000000

class NumberStoreError(Exception):
    """本模块所有异常的根。"""

class InvalidValueError(NumberStoreError, ValueError):
    """输入不是整数（bool 也不算），或 k 为负。"""

class OutOfRangeError(InvalidValueError):
    """值落在有界索引的值域之外。"""

class ValueNotFoundError(NumberStoreError, LookupError):
    """删除一个不存在的值。"""

class EmptyStoreError(NumberStoreError, LookupError):
    """在空集合里查最近值。"""

class Tie(enum.Enum):
    """离 target 一样近的两个值，取哪一个。"""
    LOWER = 'lower'
    HIGHER = 'higher'

class OrderedIndex(Protocol):
    """有序多重集合（multiset）的存储接缝：只要能回答这几个问题就能被 NumberStore 使用。"""

    def __len__(self) -> int:
        ...

    def add(self, value: int) -> None:
        ...

    def remove(self, value: int) -> bool:
        """删掉一个副本；原本就没有则返回 False，不改变状态。"""
        ...

    def count(self, value: int) -> int:
        ...

    def floor(self, value: int) -> int | None:
        """不大于 value 的最大值；没有则 None。"""
        ...

    def ceiling(self, value: int) -> int | None:
        """不小于 value 的最小值；没有则 None。"""
        ...

    def values(self) -> tuple[int, ...]:
        """升序快照（含重复）。"""
        ...

class SortedListIndex:
    """有序列表 + bisect：重复值就在列表里重复出现。"""

    def __init__(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def add(self, value: int) -> None:
        raise NotImplementedError

    def remove(self, value: int) -> bool:
        raise NotImplementedError

    def count(self, value: int) -> int:
        raise NotImplementedError

    def floor(self, value: int) -> int | None:
        raise NotImplementedError

    def ceiling(self, value: int) -> int | None:
        raise NotImplementedError

    def values(self) -> tuple[int, ...]:
        raise NotImplementedError

class FenwickIndex:
    """值域 [lo, hi] 内的树状数组：下标是「值 - lo + 1」，节点存一段区间内的个数。"""

    def __init__(self, lo: int, hi: int) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def _bump(self, value: int, delta: int) -> None:
        raise NotImplementedError

    def _prefix(self, pos: int) -> int:
        """下标 1..pos 的个数之和。"""
        raise NotImplementedError

    def _kth(self, k: int) -> int:
        """按升序第 k 个（1 起）元素的值：在树上倍增下降，O(log R)。"""
        raise NotImplementedError

    def add(self, value: int) -> None:
        raise NotImplementedError

    def remove(self, value: int) -> bool:
        raise NotImplementedError

    def count(self, value: int) -> int:
        raise NotImplementedError

    def floor(self, value: int) -> int | None:
        raise NotImplementedError

    def ceiling(self, value: int) -> int | None:
        raise NotImplementedError

    def values(self) -> tuple[int, ...]:
        raise NotImplementedError

class NumberStore:
    """对外的门面：整数多重集合，支持增、删、查离 target 最近的值。"""

    def __init__(self, index: OrderedIndex | None=None, tie: Tie=Tie.LOWER) -> None:
        raise NotImplementedError

    @staticmethod
    def _check(value: int) -> None:
        raise NotImplementedError

    def add(self, value: int) -> None:
        raise NotImplementedError

    def remove(self, value: int) -> None:
        raise NotImplementedError

    def count(self, value: int) -> int:
        raise NotImplementedError

    def __contains__(self, value: object) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def values(self) -> tuple[int, ...]:
        raise NotImplementedError

    def _prefers_lower(self, target: int, lower: int, higher: int) -> bool:
        raise NotImplementedError

    def closest(self, target: int) -> int:
        """离 target 最近的值；一样近时按 tie 规则。空集合抛 EmptyStoreError。"""
        raise NotImplementedError

    def k_closest(self, target: int, k: int) -> tuple[int, ...]:
        """最近的 k 个值（重复值各算一个），升序返回；不足 k 个就全返回。"""
        raise NotImplementedError

    def _runs_down(self, start: int) -> Iterator[tuple[int, int]]:
        """从 start 往下，逐个不同的值与它的个数。"""
        raise NotImplementedError

    def _runs_up(self, start: int) -> Iterator[tuple[int, int]]:
        raise NotImplementedError
