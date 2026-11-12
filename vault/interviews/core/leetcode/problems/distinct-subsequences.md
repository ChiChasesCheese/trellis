---
slug: distinct-subsequences
---
## Q
**LC 115 不同的子序列**｜Hard

统计字符串 `s` 的子序列中 `t` 出现的次数（下标不同算不同方案）。

## A
**一句话。** 二维 DP：`dp[i][j]` 为 `s[:i]` 中 `t[:j]` 的出现次数，字符相等时「用」与「不用」两项相加。

```python
def num_distinct(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1                  # 空串：恰一种取法
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i-1][j]     # 不用 s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i-1][j-1]  # 用 s[i-1]
    return dp[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只置 `dp[0][0] = 1`：第 0 列每行都要是 `1`，`("babgbag","bag")` 得 `3`，应为 `5`。
- 相等时丢掉「不用」那一项：`("rabbbit","rabbit")` 得 `1`，应为 `3`。
- 相等时加同行的 `dp[i][j-1]`：`s[i-1]` 被重复使用，`("a","aa")` 得 `1`，应为 `0`。

**追问。**
- 怎么输出方案？：从 `(m,n)` 回溯，`dp[i][j] > dp[i-1][j]` 说明用了 `s[i-1]`。
- 递归加 `@cache` 行不行？：深度可达 `m+n=2000`，超过默认递归上限，需调高。

**同模式。** LC 392 判断子序列、LC 1143 最长公共子序列、LC 72 编辑距离、LC 97 交错字符串
