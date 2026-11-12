---
slug: minimum-difficulty-of-a-job-schedule
---
## Q
**LC 1335 工作计划的最低难度**｜Hard

工作按顺序做，把它们切成恰好 `d` 天（每天至少一项、连续），一天的难度是当天最大值。求总难度最小值，做不到返回 `-1`。

## A
**一句话。** 划分型 DP：`dp[k][i]` 是前 `i` 项用 `k` 天的最小难度，枚举最后一天的起点。

```python
def min_difficulty(jobs, d):
    n = len(jobs)
    if n < d:
        return -1
    dp = [[inf] * (n + 1) for _ in range(d + 1)]
    dp[0][0] = 0
    for k in range(1, d + 1):
        for i in range(k, n + 1):
            mx = 0
            # 第 k 天做 j..i-1，j 左移，当天最大值只增不减
            for j in range(i - 1, k - 2, -1):
                mx = max(mx, jobs[j])
                dp[k][i] = min(dp[k][i], dp[k-1][j] + mx)
    return dp[d][n]
```

**复杂度。** 时间 `O(dn²)`，空间 `O(dn)`。

**易错点。**
- 忘了 `n < d` 返回 `-1`：DP 全是 `inf`，会返回 `inf`。
- 当天难度只取右端 `jobs[i-1]` 而非区间最大值：`[6,5,4,3,2,1]`, `d=2` 得 `3`，应为 `7`。

**追问。**
- 空间能压吗？：`dp[k]` 只依赖 `dp[k-1]`，留两行即可，但不能再回溯方案。
- 怎么输出切分方案？：记下每格取最小时的 `j`，从 `dp[d][n]` 倒推。

**同模式。** LC 410 分割数组的最大值、LC 813 最大平均值和的分组、LC 1043 分隔数组以得到最大和、LC 1478 安排邮筒
