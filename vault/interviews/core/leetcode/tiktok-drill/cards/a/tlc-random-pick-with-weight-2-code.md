---
id: tlc-random-pick-with-weight-2-code
node: a.random-pick-with-weight
type: qa
step: 2
---
## Q
**LC 528 按权重随机选择**｜写出 Python 实现

实现类 `Solution(w)` 和 `pickIndex()`：`w` 是正整数数组，`pickIndex` 返回下标 `i` 的概率为 `w[i] / sum(w)`。`1 <= w.length <= 10^4`，`1 <= w[i] <= 10^5`，`pickIndex` 至多调用 `10^4` 次。

## A
**思路。** 构造时算一次前缀和，数轴 `[0, total)` 被切成 `n` 段，第 `i` 段长 `w[i]`。每次抽取在 `[0, total)` 取均匀整数 `r`，二分找第一个 `prefix[i] > r` 的下标。

```python
import random
from bisect import bisect_right
from itertools import accumulate


class Solution:
    def __init__(self, w: list[int]):
        self.prefix = list(accumulate(w))        # prefix[i] = w[0] + ... + w[i]
        self.total = self.prefix[-1]

    def pickIndex(self) -> int:
        r = random.randrange(self.total)         # 均匀落在 [0, total)
        return bisect_right(self.prefix, r)      # 第一个 prefix[i] > r 的 i
```

运行：`w = [1, 3]` 时 `r = 0, 1, 2, 3` 分别映射到下标 `0, 1, 1, 1`；`random.seed(1)` 后抽 `10^5` 次得到 `Counter({1: 75025, 0: 24975})`；`w = [1]` 连抽 5 次全是 `0`；`10^4` 个权重建表加 `10^4` 次抽取约 `3 ms`。

**复杂度。** 构造 `O(n)`；每次抽取 `O(log n)`（一次二分）；空间 `O(n)`。

**写法要点。** `accumulate` 一次得到前缀和，比手写循环短且在 C 里跑；`randrange(total)` 是 `[0, total)` 的整数，正好配 `bisect_right`（左闭右开）；`total` 存成属性，不用每次取 `prefix[-1]`。标准库的 `random.choices(range(n), cum_weights=self.prefix)` 一行也能做，但面试要能写出二分。
