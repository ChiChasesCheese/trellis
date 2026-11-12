---
slug: put-marbles-in-bags
---
## Q
**LC 2551 将珠子放入背包中**｜Hard

把 `weights` 切成 `k` 段连续的背包，一个背包的价格是首尾珠子重量之和。求所有分法中最大分数与最小分数的差。

## A
**一句话。** 每个切点贡献相邻两数之和，首尾项恒定抵消，答案是最大 `k-1` 个切点和减最小 `k-1` 个。

```python
def put_marbles(weights, k):
    cuts = sorted(a + b for a, b in pairwise(weights))
    # k=1 时两个切片都为空，结果 0
    m = len(cuts) - (k - 1)
    return sum(cuts[m:]) - sum(cuts[:k - 1])
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 写 `cuts[-(k - 1):]`：`k = 1` 时变成 `cuts[-0:]`，是整个列表，`([1,3,5], 1)` 得 `12`，应为 `0`。
- 切点数写成 `k`：`k` 个背包只有 `k-1` 个切点。

**追问。**
- 只求最大分数怎么做？：`weights[0] + weights[-1]` 加最大的 `k-1` 个切点和。
- 价格改成 `weights[i] * weights[j]` 呢？：贡献不再可加，要改用 DP。

**同模式。** LC 410 分割数组的最大值、LC 1423 可获得的最大点数、LC 2742 给墙壁刷油漆
