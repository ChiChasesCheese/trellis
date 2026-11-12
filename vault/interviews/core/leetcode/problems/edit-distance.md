---
slug: edit-distance
---
## Q
**LC 72 编辑距离**｜Medium

把 `word1` 变成 `word2`，每次可插入、删除或替换一个字符，求最少操作数。

## A
**一句话。** 二维 DP：末尾相同继承斜上方，否则取替换、删除、插入三者最小再加 `1`。

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i             # word1[:i] 变空串：删 i 次
    for j in range(n + 1):
        dp[0][j] = j             # 空串变 word2[:j]：插 j 次
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],    # 替换
                    dp[i - 1][j],        # 删除
                    dp[i][j - 1])        # 插入
    return dp[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 第 0 行第 0 列没初始化：`("", "a")` 得 `0`，应为 `1`。
- `min` 漏一种转移：只取替换和删除，`("a", "ab")` 得 `2`，应为 `1`。
- 下标少减 `1`：表多一行一列，要写 `word1[i-1]`，写 `word1[i]` 会 `IndexError`。

**追问。**
- 只允许插入和删除（LC 583）？：答案是 `m + n - 2·LCS`。
- 三种操作代价不同？：转移里把 `1 +` 换成各自代价，边界同步乘代价。

**同模式。** LC 1143 最长公共子序列、LC 583 两个字符串的删除操作、LC 712 两个字符串的最小ASCII删除和、LC 97 交错字符串
