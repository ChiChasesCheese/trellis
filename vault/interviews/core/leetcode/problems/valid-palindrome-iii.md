---
slug: valid-palindrome-iii
---
## Q
**LC 1216 验证回文串 III**｜Hard

给字符串 `s` 和整数 `k`，判断最多删去 `k` 个字符能否变成回文串。

## A
**一句话。** 区间 DP：`dp[i][j]` 是把 `s[i..j]` 变回文最少删几个，两端相同看内部，不同就删一端取小。

```python
def is_valid_palindrome(s, k):
    n = len(s)
    dp = [[0] * n for _ in range(n)]  # 最少删除数
    for i in range(n - 1, -1, -1):    # i 倒序，dp[i+1] 先算好
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1] <= k
```

**复杂度。** 时间 `O(n²)`，空间 `O(n²)`。

**易错点。**
- 遍历顺序错：`i` 正序时 `dp[i+1][*]` 还是初值 `0`，结果偏小。
- 两端不同写成 `1 + dp[i+1][j-1]`：`"abc"`、`k = 1` 会得 `True`，应为 `False`。

**追问。**
- 空间能压到 `O(n)` 吗？：能，`dp[i]` 只依赖下一行，滚动数组即可。
- 要输出删了哪些字符？：记录每个状态的决策，从 `(0, n-1)` 倒推。

**同模式。** LC 516 最长回文子序列、LC 1312 让字符串成为回文串的最少插入次数、LC 647 回文子串
