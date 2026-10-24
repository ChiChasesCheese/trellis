---
id: tlc-patterns-binary-search-2-template
node: patterns.binary-search
type: qa
step: 2
---
## Q
**二分查找（Binary Search）｜模板：左闭右开的「找第一个 True」**

写出一个通用的二分模板，既能做下标上的下界查找，也能做对答案二分；循环条件和边界怎么保证不死循环、不越界？

## A
```python
from typing import Callable
def first_true(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """在 [lo, hi) 上找第一个 ok 为 True 的位置；全为 False 时返回 hi。"""
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid                       # mid 可能就是答案，保留
        else:
            lo = mid + 1                   # mid 一定不是答案，丢掉
    return lo
```

运行（`a = [1, 3, 3, 5]`）：
- 第一个 `>= 3`：`first_true(0, 4, lambda i: a[i] >= 3)` → `1`；
- 第一个 `> 3`：→ `3`；
- 第一个 `>= 7`（不存在）：→ `4`，即 `len(a)`；
- 第一个 `>= 0`：→ `0`。

对答案二分只需换掉区间和判定。LC 875：速度 `k` 能否在 `h` 小时内吃完，`first_true(1, max(piles) + 1, ok)`：`([3,6,7,11], 8)` → `4`，`([30,11,23,4,20], 5)` → `30`，`([30,11,23,4,20], 6)` → `23`。

- 区间约定 `[lo, hi)`：`hi` 取「答案上界 + 1」，答案可能不存在时返回 `hi`。
- 每次循环区间严格缩小：`hi = mid`（`mid < hi`）或 `lo = mid + 1`，所以不会死循环。
- `mid = (lo + hi) // 2`：Python 整数不溢出，不必写 `lo + (hi - lo) // 2`。
- 求「最后一个 True」：把判定取反，找第一个 `False`，答案是它减 1。
