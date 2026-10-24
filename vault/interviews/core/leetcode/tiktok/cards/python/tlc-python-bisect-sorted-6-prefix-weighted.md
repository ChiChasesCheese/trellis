---
id: tlc-python-bisect-sorted-6-prefix-weighted
node: python.bisect-sorted
type: qa
step: 6
---
## Q
**Python 工具箱｜`accumulate` 前缀和配 `bisect`**

「区间内有多少个数」和「按权重随机选下标」（LC 528）都能用 `bisect` 做，各自怎么写？

## A
**区间计数**：有序数组里 `[lo, hi]` 内元素个数 = `bisect_right(a, hi) - bisect_left(a, lo)`，`O(log n)`。

```python
from bisect import bisect_left, bisect_right
s = [1, 3, 3, 5, 8, 10]
print(bisect_right(s, 8) - bisect_left(s, 3))   # 4：3,3,5,8
```

**按权重随机**：权重 `w`，前缀和 `pre = accumulate(w)`，在 `[0, total)` 里均匀取一个整数 `r`，找第一个 `pre[i] > r` 的 `i`，即 `bisect_right(pre, r)`。

```python
import random
from bisect import bisect_right
from itertools import accumulate
class Solution:
    def __init__(self, w: list[int]) -> None:
        self.pre = list(accumulate(w))          # [1, 4]：下标 0 占 [0,1)，下标 1 占 [1,4)
    def pick_index(self) -> int:
        return bisect_right(self.pre, random.randrange(self.pre[-1]))
print([bisect_right([1, 4], r) for r in range(4)])   # [0, 1, 1, 1]：权重 1 : 3
```

- 每次 `pick_index` 是 `O(log n)`，构造 `O(n)`。
- 用 `randrange(total)`（0 到 `total-1`）配 `bisect_right`；若改成 `randint(1, total)` 就要配 `bisect_left`，两种成对出现，混用会差一位。
- 这个「前缀和 + 二分」的组合也用于：LC 1146 快照数组（每个下标存 `(版本号, 值)` 列表，按版本号二分）、离线统计「小于某值的个数」。

**坑**：`accumulate` 返回迭代器，要多次访问必须 `list(...)`；权重全为 0 或总和为 0 时 `randrange` 报 `ValueError`。
