"""增删查最近值（Add / Remove / Closest）参考解。

设计五句话：
1. NumberStore 是门面：校验输入、定平局规则、持有一把锁，保证「查两侧邻居」是一次原子读。
2. 真正存数据的是 OrderedIndex（有序索引）这条接缝，只回答 floor / ceiling / count 三个问题。
3. SortedListIndex：有序列表加二分，无值域限制，插入删除 O(n) 的内存搬移但常数极小。
4. FenwickIndex：值域有界时用树状数组（Fenwick tree）存每个值的个数，增删查都是 O(log R)。
5. 最近值 = 比较 floor(target) 与 ceiling(target) 两个候选；k 个最近值 = 从两侧向外归并。
"""

from __future__ import annotations

import bisect
import enum
import threading
from collections.abc import Iterator
from typing import Protocol

MAX_SPAN = 5_000_000  # 树状数组允许的最大值域宽度，超过请改用 SortedListIndex


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

    LOWER = "lower"
    HIGHER = "higher"


class OrderedIndex(Protocol):
    """有序多重集合（multiset）的存储接缝：只要能回答这几个问题就能被 NumberStore 使用。"""

    def __len__(self) -> int: ...

    def add(self, value: int) -> None: ...

    def remove(self, value: int) -> bool:
        """删掉一个副本；原本就没有则返回 False，不改变状态。"""
        ...

    def count(self, value: int) -> int: ...

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
        self._xs: list[int] = []

    def __len__(self) -> int:
        return len(self._xs)

    def add(self, value: int) -> None:
        bisect.insort(self._xs, value)

    def remove(self, value: int) -> bool:
        i = bisect.bisect_left(self._xs, value)
        if i == len(self._xs) or self._xs[i] != value:
            return False
        del self._xs[i]
        return True

    def count(self, value: int) -> int:
        return bisect.bisect_right(self._xs, value) - bisect.bisect_left(self._xs, value)

    def floor(self, value: int) -> int | None:
        i = bisect.bisect_right(self._xs, value)
        return self._xs[i - 1] if i else None

    def ceiling(self, value: int) -> int | None:
        i = bisect.bisect_left(self._xs, value)
        return self._xs[i] if i < len(self._xs) else None

    def values(self) -> tuple[int, ...]:
        return tuple(self._xs)


class FenwickIndex:
    """值域 [lo, hi] 内的树状数组：下标是「值 - lo + 1」，节点存一段区间内的个数。"""

    def __init__(self, lo: int, hi: int) -> None:
        if hi < lo or hi - lo + 1 > MAX_SPAN:
            raise InvalidValueError(f"值域 [{lo}, {hi}] 必须非空且宽度不超过 {MAX_SPAN}")
        self._lo, self._hi = lo, hi
        self._n = hi - lo + 1
        self._tree = [0] * (self._n + 1)
        self._cnt = [0] * (self._n + 1)  # 每个值的个数，count() 因此是 O(1)
        self._total = 0
        self._top = 1 << (self._n.bit_length() - 1)  # 不超过 n 的最大 2 的幂，kth 的起步步长

    def __len__(self) -> int:
        return self._total

    def _bump(self, value: int, delta: int) -> None:
        pos = value - self._lo + 1
        self._cnt[pos] += delta
        self._total += delta
        while pos <= self._n:
            self._tree[pos] += delta
            pos += pos & -pos

    def _prefix(self, pos: int) -> int:
        """下标 1..pos 的个数之和。"""
        total = 0
        while pos > 0:
            total += self._tree[pos]
            pos -= pos & -pos
        return total

    def _kth(self, k: int) -> int:
        """按升序第 k 个（1 起）元素的值：在树上倍增下降，O(log R)。"""
        pos, step = 0, self._top
        while step:
            nxt = pos + step
            if nxt <= self._n and self._tree[nxt] < k:
                pos = nxt
                k -= self._tree[nxt]
            step >>= 1
        return self._lo + pos

    def add(self, value: int) -> None:
        if not self._lo <= value <= self._hi:
            raise OutOfRangeError(f"{value} 不在 [{self._lo}, {self._hi}] 内")
        self._bump(value, 1)

    def remove(self, value: int) -> bool:
        if not self._lo <= value <= self._hi or self._cnt[value - self._lo + 1] == 0:
            return False
        self._bump(value, -1)
        return True

    def count(self, value: int) -> int:
        return self._cnt[value - self._lo + 1] if self._lo <= value <= self._hi else 0

    def floor(self, value: int) -> int | None:
        if value < self._lo:
            return None
        k = self._prefix(min(value, self._hi) - self._lo + 1)
        return self._kth(k) if k else None

    def ceiling(self, value: int) -> int | None:
        if value > self._hi:
            return None
        k = self._prefix(max(value, self._lo) - self._lo) + 1
        return self._kth(k) if k <= self._total else None

    def values(self) -> tuple[int, ...]:
        return tuple(self._lo + i - 1 for i in range(1, self._n + 1) for _ in range(self._cnt[i]))


class NumberStore:
    """对外的门面：整数多重集合，支持增、删、查离 target 最近的值。"""

    def __init__(self, index: OrderedIndex | None = None, tie: Tie = Tie.LOWER) -> None:
        self._index: OrderedIndex = index if index is not None else SortedListIndex()
        self._tie = tie
        self._lock = threading.Lock()  # 一次查询要读 floor 与 ceiling 两次，必须是同一个版本

    @staticmethod
    def _check(value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidValueError(f"需要整数，得到 {value!r}")

    def add(self, value: int) -> None:
        self._check(value)
        with self._lock:
            self._index.add(value)

    def remove(self, value: int) -> None:
        self._check(value)
        with self._lock:
            if not self._index.remove(value):
                raise ValueNotFoundError(value)

    def count(self, value: int) -> int:
        with self._lock:
            return self._index.count(value)

    def __contains__(self, value: object) -> bool:
        return isinstance(value, int) and self.count(value) > 0

    def __len__(self) -> int:
        with self._lock:
            return len(self._index)

    def values(self) -> tuple[int, ...]:
        with self._lock:
            return self._index.values()

    def _prefers_lower(self, target: int, lower: int, higher: int) -> bool:
        gap_lo, gap_hi = target - lower, higher - target
        return gap_lo < gap_hi or (gap_lo == gap_hi and self._tie is Tie.LOWER)

    def closest(self, target: int) -> int:
        """离 target 最近的值；一样近时按 tie 规则。空集合抛 EmptyStoreError。"""
        self._check(target)
        with self._lock:
            lower, higher = self._index.floor(target), self._index.ceiling(target)
        if lower is None and higher is None:
            raise EmptyStoreError("集合为空")
        if lower is None or higher is None:
            return lower if higher is None else higher  # type: ignore[return-value]
        return lower if self._prefers_lower(target, lower, higher) else higher

    def k_closest(self, target: int, k: int) -> tuple[int, ...]:
        """最近的 k 个值（重复值各算一个），升序返回；不足 k 个就全返回。"""
        self._check(target)
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise InvalidValueError(f"k 必须是非负整数，得到 {k!r}")
        chosen: list[int] = []
        with self._lock:
            down, up = self._runs_down(target), self._runs_up(target + 1)
            a, b = next(down, None), next(up, None)
            while len(chosen) < k and (a or b):
                from_lower = b is None or (a is not None and self._prefers_lower(target, a[0], b[0]))
                value, copies = a if from_lower else b  # type: ignore[misc]
                chosen.extend([value] * min(copies, k - len(chosen)))
                if from_lower:
                    a = next(down, None)
                else:
                    b = next(up, None)
        return tuple(sorted(chosen))

    def _runs_down(self, start: int) -> Iterator[tuple[int, int]]:
        """从 start 往下，逐个不同的值与它的个数。"""
        value = self._index.floor(start)
        while value is not None:
            yield value, self._index.count(value)
            value = self._index.floor(value - 1)

    def _runs_up(self, start: int) -> Iterator[tuple[int, int]]:
        value = self._index.ceiling(start)
        while value is not None:
            yield value, self._index.count(value)
            value = self._index.ceiling(value + 1)


if __name__ == "__main__":
    store = NumberStore(FenwickIndex(0, 100))
    for v in (5, 20, 20, 42):
        store.add(v)
    print(store.closest(30), store.k_closest(21, 3))
