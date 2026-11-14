---
slug: amazon-merge-strings-min-conflicts
---
## Q
**保序合并两串使相邻冲突最少**｜Medium

把字符串 `s`、`t` 交错合并成一个串（各自字符的相对顺序不变），合并串里相邻两字符相同算一次冲突，求最少冲突数。

## A
**一句话。** 交错合并是网格路径 DP：`dp[i][j][k]` 是用完 `s[:i]`、`t[:j]` 且末字符来自 `s`（`k = 0`）或 `t`（`k = 1`）时的最少冲突，下一步取 `s[i]` 或 `t[j]`，和末字符相同就加 1。

```python
def min_conflicts(s, t):
    m, n, INF = len(s), len(t), float("inf")
    if m + n == 0:
        return 0
    # dp[i][j][k]：用完 s[:i]、t[:j]，末字符来自 s(0)/t(1)
    dp = [[[INF] * 2 for _ in range(n + 1)]
          for _ in range(m + 1)]
    if m:
        dp[1][0][0] = 0
    if n:
        dp[0][1][1] = 0
    for i in range(m + 1):
        for j in range(n + 1):
            for k in (0, 1):
                cur = dp[i][j][k]
                if cur == INF:
                    continue
                last = s[i - 1] if k == 0 else t[j - 1]
                if i < m:     # 下一个放 s[i]
                    a = cur + (s[i] == last)
                    dp[i+1][j][0] = min(dp[i+1][j][0], a)
                if j < n:     # 下一个放 t[j]
                    b = cur + (t[j] == last)
                    dp[i][j+1][1] = min(dp[i][j+1][1], b)
    return min(dp[m][n])
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 状态只有 `(i, j)`：不知道末字符是谁，判断不了下一步冲不冲突。
- 第一个字符也去比前一个：它没有前驱，要单独置 `dp[1][0][0] = dp[0][1][1] = 0`。

**追问。**
- 「冲突」没说清？：先问是相邻相同、与模板串同位不同，还是逆序对；只要代价只看上一个字符，就是这个 DP。
- 要输出合并串？：每格记下是从哪个状态转来的，从 `(m, n)` 倒推。

**同模式。** LC 97 交错字符串、LC 1143 最长公共子序列、LC 72 编辑距离
