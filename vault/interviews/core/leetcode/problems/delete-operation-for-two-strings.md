---
slug: delete-operation-for-two-strings
---
## Q
**LC 583 两个字符串的删除操作**｜Medium

给 `word1`、`word2`，每步可以删除其中一个字符串的一个字符，求使两个字符串相同所需的最少步数。

## A
**一句话。** 留下的必是公共子序列，留得越长删得越少，所以答案是 `m + n - 2·LCS`。

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    f = [[0] * (n + 1) for _ in range(m + 1)]  # 前缀 LCS
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                f[i][j] = f[i - 1][j - 1] + 1   # 一起保留
            else:
                f[i][j] = max(f[i - 1][j], f[i][j - 1])
    return m + n - 2 * f[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只算 `m - LCS` 或 `n - LCS`：两边都要删，总数是两边各删 `len - LCS`。
- 把 LCS 当作最长公共子串：子序列不要求连续。
- 不等时只取左边或上边：两个都要比较，取较大者。

**追问。**
- 直接做 DP 而不借 LCS？：`dp[i][j]` 为使前缀相同的最少删除数，相同取 `dp[i-1][j-1]`，不同取 `min(dp[i-1][j], dp[i][j-1]) + 1`。
- 想允许替换呢？：就是编辑距离，多一个 `dp[i-1][j-1] + 1` 的转移。

**同模式。** LC 1143 最长公共子序列、LC 72 编辑距离、LC 712 两个字符串的最小ASCII删除和、LC 1035 不相交的线
