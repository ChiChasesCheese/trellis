---
id: tlc-longest-palindromic-subsequence-4-followup
node: b.longest-palindromic-subsequence
type: qa
step: 4
---
## Q
**LC 516 最长回文子序列**｜追问

面试官接着问：（1）除了长度，再返回一个最长回文子序列本身？（2）至少插入几个字符能让 `s` 变成回文？（3）内存只有 `O(n)` 怎么办？

## A
1. **返回子序列**：填完表后从 `(0, n-1)` 出发倒推：两端相同就两边各收下一个字符并向内收缩；不同就走向 `dp` 较大的那一侧；`i == j` 时收下中间字符。

```python
def longest_palindrome_subseq_str(s: str) -> str:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            dp[i][j] = dp[i + 1][j - 1] + 2 if s[i] == s[j] else max(dp[i + 1][j], dp[i][j - 1])
    left: list[str] = []
    i, j = 0, n - 1
    while i <= j:
        if i == j:                            # 奇数长度回文的中心
            return "".join(left) + s[i] + "".join(reversed(left))
        if s[i] == s[j]:
            left.append(s[i])
            i, j = i + 1, j - 1
        elif dp[i + 1][j] >= dp[i][j - 1]:
            i += 1
        else:
            j -= 1
    return "".join(left) + "".join(reversed(left))
```

运行：`"bbbab"` → `"bbbb"`，`"cbbd"` → `"bb"`，`"abcda"` → `"ada"`。

2. **最少插入次数（LC 1312）**：保留最长回文子序列不动，其余每个字符都要在对称位置补一个，答案 `n - dp[0][n-1]`；`"mbadm"` → `2`。
3. **内存 `O(n)`**：空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**Python 提醒**：`[[0] * n] * n` 会让 `n` 行共享同一个列表，必须写 `[[0] * n for _ in range(n)]`。
