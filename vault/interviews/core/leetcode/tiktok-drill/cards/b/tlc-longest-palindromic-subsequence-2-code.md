---
id: tlc-longest-palindromic-subsequence-2-code
node: b.longest-palindromic-subsequence
type: qa
step: 2
---
## Q
**LC 516 最长回文子序列**｜写出 Python 实现

字符串 `s`（`1 <= 长度 <= 1000`，小写字母）里最长的回文子序列有多长？子序列可以不连续。要求 `O(n^2)`。

## A
**思路。** `dp[i][j]` 是 `s[i..j]` 的答案。单字符为 `1`；两端相同取 `dp[i+1][j-1] + 2`，不同取 `max(dp[i+1][j], dp[i][j-1])`。因为依赖下一行，`i` 从 `n-1` 倒着走，`j` 从 `i+1` 正着走。

```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]          # dp[i][j]：s[i..j] 内最长回文子序列的长度
    for i in range(n - 1, -1, -1):            # i 从后往前：dp[i][*] 依赖 dp[i+1][*]
        dp[i][i] = 1                          # 单个字符本身是回文
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2   # 两端相同：夹在中间的最优解外面各加一个
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])   # 两端不同：至少丢掉一端
    return dp[0][n - 1]
```

运行：`"bbbab"` → `4`，`"cbbd"` → `2`，`"a"` → `1`，`"ab"` → `1`，`"abcda"` → `3`。

**复杂度。** 时间 `O(n^2)`：上三角 `n(n-1)/2` 个区间，每个 `O(1)`；空间 `O(n^2)` 的表。

**写法要点。** `range(n - 1, -1, -1)` 是倒序遍历的标准写法（也可写 `reversed(range(n))`，更易读）；表只用上三角，对角线下方保持 `0`，正好充当「空区间」的值，`j = i + 1` 且两端相同时读到 `dp[i+1][i] = 0`，得到 `2`，不需要单独处理长度 2。
