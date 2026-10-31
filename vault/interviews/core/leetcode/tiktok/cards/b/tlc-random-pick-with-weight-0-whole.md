---
id: tlc-random-pick-with-weight-0-whole
node: b.random-pick-with-weight
type: qa
---
## Q
**LC 528 按权重随机选择**｜Medium · LC TikTok 全时段热度 50/100 · CodeTop 国内累计 12 次 · 最近 2026-09-19（国内 CodeTop）

给一个下标从 0 开始的正整数数组 `w`，`w[i]` 是下标 `i` 的权重。实现 `Solution(w)` 和 `pickIndex()`：每次调用随机返回 `[0, w.length - 1]` 内的一个下标，返回 `i` 的概率是 `w[i] / sum(w)`。`1 <= w.length <= 10^4`，`1 <= w[i] <= 10^5`，`pickIndex` 至多调用 `10^4` 次。例：`w = [1, 3]` 时下标 `0` 的概率是 `25%`，下标 `1` 是 `75%`；`w = [1]` 时永远返回 `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用前缀和（prefix sum）把权重铺成一条长度 `sum(w)` 的数轴，每个下标占一段；在 `[0, sum)` 里均匀取一个整数，再用二分查找（binary search）找出它落在哪一段。构造 `O(n)`，每次抽取 `O(log n)`。

**识别。** 「按权重抽样」而手里只有均匀随机数，就把权重换成区间长度；`pickIndex` 会被调用很多次，所以预处理一次、每次抽取要快；`w[i] >= 1` 使前缀和严格递增，可以二分。

**推导。** 暴力：把下标 `i` 重复 `w[i]` 次展开成数组再均匀取一个，数组长度可达 `10^9`，放不下。每次现算：从左到右累减权重直到用完随机数，每次 `O(n)`，总共 `10^4 × 10^4`。浪费：展开数组里连续一段全是同一个下标，只需要记每段的右端点，那就是前缀和。洞察：随机整数 `r` 落在哪一段，等于第一个满足 `prefix[i] > r` 的 `i`，在严格递增的前缀和上二分。

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

**复杂度。** 构造 `O(n)`，抽取 `O(log n)`；空间 `O(n)`。

**易错点。**
- `randrange(total)` 配 `bisect_left`：区间是左闭右开，`r` 恰好等于某个前缀和时属于下一段。`w = [1, 3]` 时 `r = 0, 1` 都被映射到下标 `0`，下标 `0` 的概率变成 `2/4`（正确是 `1/4`）。要么 `bisect_right`，要么 `randint(1, total)` 配 `bisect_left`。
- `randint(a, b)` 两端都包含，`randrange(b)` 不含 `b`，混用就差一位。
- 每次 `pickIndex` 都重新 `accumulate` 一遍是 `O(n)`，调用 `10^4` 次会很慢；前缀和只在构造时算一次。

**追问。**
- 权重会动态更新：用树状数组（Fenwick tree）维护前缀和，更新和抽取都是 `O(log n)`。
- 要 `O(1)` 抽取：别名法（alias method），构造 `O(n)`，不支持更新。
- 不放回地连续抽：抽中后把该下标权重减到 `0`，仍用树状数组。

**同模式。** LC 497 非重叠矩形中的随机点、LC 710 黑名单中的随机数、LC 398 随机数索引、LC 382 链表随机节点。
