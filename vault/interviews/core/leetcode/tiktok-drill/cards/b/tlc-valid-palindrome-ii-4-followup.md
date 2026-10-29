---
id: tlc-valid-palindrome-ii-4-followup
node: b.valid-palindrome-ii
type: qa
step: 4
---
## Q
**LC 680 验证回文字符串 Ⅱ**｜追问

面试官接着问：（1）要**返回**该删的下标？（2）改成**最多删 `k` 个**字符（LC 1216）？（3）字符串里有大小写、空格和标点，只比较字母数字且不区分大小写？分别怎么改。

## A
1. **返回下标**：失配后先试删左，`is_pal(left + 1, right)` 成立就返回 `left`；再试删右，成立返回 `right`；整串本来就是回文返回 `-1`；都不行返回 `None`。
2. **最多删 `k` 个**：失配处的分支会叠加，不再是常数。改求最长回文子序列（longest palindromic subsequence）：删掉 `n - lps` 个字符恰好得到回文，所以判断 `n - lps <= k`。状态 `dp[i][j]` 是 `s[i..j]` 的最长回文子序列长度，用完整二维表：

```python
def can_palindrome_with_k_deletions(s: str, k: int) -> bool:
    n = len(s)
    dp = [[0] * n for _ in range(n)]       # dp[i][j]：s[i..j] 的最长回文子序列长度
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return n - dp[0][-1] <= k
```

   时间空间都是 `O(n^2)`，只适合 `n` 不大；空间可以压到 `O(n)`：见 Python 工具箱「DP 降维」。
3. **忽略大小写与非字母数字**：先 `t = [c.lower() for c in s if c.isalnum()]`（`O(n)`），再把 `s` 换成 `t` 套原函数。

**Python 提醒**：`s[a:b]` 每次复制 `O(b-a)`，在循环里反复切片会把 `O(n)` 悄悄变成 `O(n^2)`；`str.isalnum()` 对中文字符也返回 `True`，题面限定 ASCII 时加 `c.isascii()`。
