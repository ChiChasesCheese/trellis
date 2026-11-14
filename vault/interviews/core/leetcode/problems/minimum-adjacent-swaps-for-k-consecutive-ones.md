---
slug: minimum-adjacent-swaps-for-k-consecutive-ones
---
## Q
**LC 1703 得到连续 K 个 1 的最少相邻交换次数**｜Hard

`0/1` 数组，每次交换相邻两数，求出现连续 `k` 个 `1` 的最少交换次数。`n` 到 `10^5`。

## A
**一句话。** 取出 `1` 的下标 `pos`，令 `p[i] = pos[i] - i`，问题变成「`p` 的每个长 `k` 窗口里所有点到中位数的距离和」，前缀和 `O(1)` 算每个窗口。

```python
def min_moves(nums, k):
    p = [i - j for j, i in enumerate(
        i for i, v in enumerate(nums) if v)]  # 去掉排队偏移
    s = list(accumulate(p, initial=0))
    ans = inf
    for l in range(len(p) - k + 1):
        r, m = l + k - 1, l + k // 2           # m 是中位数
        left = p[m] * (m - l) - (s[m] - s[l])
        right = (s[r + 1] - s[m + 1]) - p[m] * (r - m)
        ans = min(ans, left + right)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 直接让 `pos` 都靠到中位数：目标是连续的 `k` 格而不是同一格，要先减去 `i` 变成「靠到同一点」。
- 每个窗口逐个求距离：`O(nk)`。

**追问。**
- 为什么是中位数？：所有点到一点的距离和在中位数处最小。
- 窗口是 `p` 上的连续段吗？：是，最优方案只会把相邻的 `k` 个 `1` 聚在一起。

**同模式。** LC 462 最小操作次数使数组元素相等 II、LC 296 最佳的碰头地点、LC 2448 使数组相等的最小开销
