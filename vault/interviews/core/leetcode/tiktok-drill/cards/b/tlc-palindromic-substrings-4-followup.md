---
id: tlc-palindromic-substrings-4-followup
node: b.palindromic-substrings
type: qa
step: 4
---
## Q
**LC 647 回文子串**｜追问

面试官接着问：（1）用 DP 怎么写，什么时候比中心扩展更合适？（2）改成返回最长回文子串？（3）能做到 `O(n)` 吗？

## A
1. **区间 DP**：`dp[i][j]` 表示 `s[i..j]` 是否回文，`dp[i][j] = s[i] == s[j] and (j - i < 2 or dp[i+1][j-1])`。`dp[i][j]` 依赖 `dp[i+1][j-1]`，所以 `i` 从大到小、`j` 从 `i` 往大填。时间同为 `O(n^2)`，但多 `O(n^2)` 空间；好处是填完后能 `O(1)` 查询任意子串，后续还要大量查询时（如 LC 131 分割回文串）更合适。

```python
def count_substrings_dp(s: str) -> int:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    total = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[i][j] = s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1])
            total += dp[i][j]
    return total
```

`"aaa"` → `6`，`"abba"` → `6`。
2. **最长回文子串（LC 5）**：同样枚举中心，扩展结束后回文是 `s[left + 1 : right]`，长度 `right - left - 1`，保留最长的一组下标，最后切片一次。
3. **`O(n)`**：Manacher 算法。在字符间插入分隔符统一奇偶，维护最右回文边界 `R` 及其中心 `C`；新中心 `i < R` 时，其镜像 `2C - i` 的半径给出初始半径 `min(R - i, p[2C - i])`，再继续扩。`R` 只增不减，总扩展次数 `O(n)`。设 `p[i]` 是插入分隔符后的串里以 `i` 为中心的回文半径（不含中心），原串回文子串个数是 `sum((r + 1) // 2 for r in p)`。

**Python 提醒**：`[[False] * n] * n` 会让 `n` 行共用同一个列表，改一格整列都变；二维表一律用 `[[False] * n for _ in range(n)]`。
