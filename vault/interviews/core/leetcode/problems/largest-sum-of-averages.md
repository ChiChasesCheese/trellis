---
slug: largest-sum-of-averages
---
## Q
**LC 813 最大平均值和的分组**｜Medium

把正整数数组 `nums` 分成至多 `k` 个相邻的非空子数组，分数是每组平均值之和。求最大分数。

## A
**一句话。** `dp[j][i]` 表示前 `i` 个数分成 `j` 组的最大分数，枚举最后一组的起点 `m`，用前缀和 `O(1)` 算最后一组的平均值。

```python
def largest_sum_of_averages(nums, k):
    n = len(nums)
    pre = list(accumulate(nums, initial=0))
    # dp[j][i]：前 i 个数分成 j 组
    dp = [[0.0] * (n + 1) for _ in range(k + 1)]
    for i in range(1, n + 1):
        dp[1][i] = pre[i] / i
    for j in range(2, k + 1):
        for i in range(j, n + 1):
            dp[j][i] = max(
                dp[j - 1][m] + (pre[i] - pre[m]) / (i - m)
                for m in range(j - 1, i))
    return dp[k][n]
```

**复杂度。** 时间 `O(k n^2)`，空间 `O(k n)`。

**易错点。**
- 以为组数越少越好：数全为正，把一组拆成两组平均值之和不会变小，所以恰好分成 `k` 组（`k ≤ n`）就是最优。
- `m` 的范围写错：前 `j - 1` 组至少需要 `j - 1` 个数，所以 `m` 从 `j - 1` 起，到 `i - 1` 止。
- 平均值用整除：要用真除法。

**追问。**
- 为什么拆开不会变小？：设一组拆成两段，平均值分别 `a`、`b`，合并后的平均是它们的加权平均，不超过 `a + b`（均为正）。
- 能优化到 `O(kn)` 吗？：这类带平均数的转移不满足简单的单调队列结构，一般不优化。

**同模式。** LC 410 分割数组的最大值、LC 1105 填充书架、LC 1235 规划兼职工作、LC 1478 安排邮筒
