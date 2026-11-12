---
slug: longest-common-subsequence
---
## Q
**LC 1143 最长公共子序列**｜Medium

求两个字符串的最长公共子序列（不要求连续）的长度。

## A
**一句话。** 二维 DP：末尾相等取左上角加一，不等取上、左的较大值。

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    # dp[i][j]：text1[:i] 与 text2[:j] 的 LCS 长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]   # 首行首列为 0
    for i, a in enumerate(text1, 1):
        for j, b in enumerate(text2, 1):
            if a == b:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 不等时归零（按子串处理）：`"abcde"` 与 `"ace"` 得 `1`，应为 `3`。
- 相等时取同行左格 `dp[i][j-1]+1`：`("a","aaa")` 得 `3`，应为 `1`，一个字符被重复匹配。

**追问。**
- 怎么还原 LCS 字符串？：从右下角回溯，相等就斜上取字符，不等走较大的方向。
- 能省空间吗？：滚动一行到 `O(min(m,n))`，但还原字符串要整表或 Hirschberg 分治。

**同模式。** LC 72 编辑距离、LC 583 两个字符串的删除操作、LC 1035 不相交的线、LC 718 最长重复子数组
