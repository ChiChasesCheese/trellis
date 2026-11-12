---
slug: longest-palindromic-subsequence
---
## Q
**LC 516 最长回文子序列**｜Medium

求字符串 `s` 中最长回文子序列（不要求连续）的长度。

## A
**一句话。** 区间 DP：两端相同则中间最优加 `2`，不同则丢掉一端取较大。

```python
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]  # s[i..j] 的答案
    for i in range(n - 1, -1, -1):     # dp[i] 依赖 dp[i+1]
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]
```

**复杂度。** 时间 `O(n²)`，空间 `O(n²)`。

**易错点。**
- 当成回文子串（要连续）：`"bbbab"` 得 `3`，应为 `4`。
- `i` 从小到大遍历：读到的 `dp[i+1]` 还没算，`"bbbab"` 得 `2`。
- 两端不同时写成只取 `dp[i+1][j-1]`：漏掉只丢一端的情况。

**追问。**
- 能换成别的问题吗？：等于 `s` 与 `s[::-1]` 的最长公共子序列（LC 1143）。
- 让串变回文的最少插入数？：`n - LPS`（LC 1312）。

**同模式。** LC 5 最长回文子串、LC 1143 最长公共子序列、LC 1312 让字符串成为回文串的最少插入次数、LC 730 统计不同回文子序列
