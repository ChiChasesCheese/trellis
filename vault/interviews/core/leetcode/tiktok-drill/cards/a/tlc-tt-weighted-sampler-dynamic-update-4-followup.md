---
id: tlc-tt-weighted-sampler-dynamic-update-4-followup
node: a.tt-weighted-sampler-dynamic-update
type: qa
step: 4
---
## Q
**按权重采样器（支持动态修改权重）**｜追问

面试官接着问：（1）如果权重从不修改，最简单的写法是什么；（2）线段树、Fenwick 树、平衡树怎么选；（3）一次要无放回地抽 `k` 个；（4）权重是小数。

## A
1. **静态权重**（LC 528）：前缀和加 `bisect_right`，建表 `O(n)`，采样 `O(log n)`。

```python
import random
from bisect import bisect_right
from itertools import accumulate


class StaticSampler:
    def __init__(self, w: list[int]) -> None:
        self._prefix = list(accumulate(w))             # 前缀和：_prefix[i] = w[0] + ... + w[i]

    def sample(self) -> int:
        r = random.randrange(self._prefix[-1])         # r 在 [0, total) 均匀取整数
        return bisect_right(self._prefix, r)           # 第一个前缀和 > r 的下标
```

权重 `[1,3,0,6]` 的前缀和是 `[1, 4, 4, 10]`，`r = 0..9` 对应 `[0, 1, 1, 1, 3, 3, 3, 3, 3, 3]`。
2. **数据结构选择**：Fenwick 树代码最短、常数小，只做单点更新加前缀和；线段树同样 `O(log n)`，还能做区间更新；需要增删元素个数（下标会移动）时用平衡二叉搜索树或跳表。
3. **无放回抽 `k` 个**：每抽中一个，把它的权重 `update` 成 `0`，继续抽；抽完再把被抽中的权重改回来，总计 `O(k log n)`。
4. **小数权重**：Fenwick 树里放浮点数，`r = rng.random() * total`；要警惕累加误差让 `r` 恰好等于总和，造成下标越界，所以最后要把 `pos` 夹到 `n - 1`；或者先把权重乘以公倍数换成整数。

**Python 提醒**：`itertools.accumulate` 对整数精确，对浮点会累积舍入误差；`random.randrange(n)` 是 `[0, n)` 的整数，比 `int(random.random() * n)` 更可靠，后者受浮点精度限制，`n` 很大时无法覆盖所有整数。
