---
slug: paint-house-ii
---
## Q
**LC 265 粉刷房子 II**｜Hard

一排 `n` 间房子，每间用 `k` 种颜色之一粉刷，`costs[i][j]` 是把第 `i` 间刷成第 `j` 种颜色的花费。相邻两间房子的颜色不能相同。返回刷完所有房子的最小花费。

## A
**一句话。** `dp[i][j]` 是刷完前 `i` 间且第 `i` 间刷成 `j` 的最小花费；转移只需要上一行的最小值和次小值，避免对每个颜色再扫一遍。

```python
def min_cost_ii(costs):
    n, k = len(costs), len(costs[0])
    dp = [[0] * k for _ in range(n + 1)]
    for i in range(1, n + 1):
        prev = dp[i - 1]
        lo = min(range(k), key=lambda c: prev[c])  # 最小颜色
        second = min(prev[c] for c in range(k) if c != lo)
        for j in range(k):
            # 与上一间不同色：若 j 正是最小颜色，只能取次小
            dp[i][j] = costs[i - 1][j] + (
                second if j == lo else prev[lo])
    return min(dp[n])
```

**复杂度。** 时间 `O(nk)`，空间 `O(nk)`。

**易错点。**
- 对每个 `j` 都扫一遍上一行：`O(nk^2)`，`k` 大时会超时，要先记最小、次小。
- 次小值取同一个颜色：必须排除最小值所在的颜色。
- `k = 1` 且 `n > 1`：无解，题目保证 `k ≥ 2`（除非只有一间房子）。

**追问。**
- `k = 3` 的原题？：LC 256，转移里直接对另外两个颜色取最小。
- 空间还能再省吗？：只用到上一行，滚动成两个长度为 `k` 的数组。

**同模式。** LC 256 粉刷房子、LC 1473 粉刷房子 III、LC 198 打家劫舍、LC 1411 给 N x 3 网格图涂色的方案数
