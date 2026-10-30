---
id: tlc-longest-common-subsequence-2-code
node: p2.longest-common-subsequence
type: qa
step: 2
---
## Q
**LC 1143 最长公共子序列**｜写出 Python 实现

两个只含小写字母的字符串 `text1`、`text2`（长度各 1 到 1000），返回最长公共子序列的长度，不存在返回 `0`。要求 `O(mn)` 时间。

## A
**思路。** `dp[i][j]` 是 `text1` 前 `i` 个字符与 `text2` 前 `j` 个字符的 LCS 长度，第 0 行、第 0 列是 `0`（空串）。逐格填：末尾字符相等取左上角加一，不等取「上」与「左」的较大者。答案是右下角 `dp[m][n]`。

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    # dp[i][j]：text1[:i] 与 text2[:j] 的 LCS 长度；第 0 行、第 0 列保持 0（空串）
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i, a in enumerate(text1, 1):
        for j, b in enumerate(text2, 1):
            if a == b:
                dp[i][j] = dp[i - 1][j - 1] + 1             # 末尾相同：一起算进去
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # 不同：丢掉其中一个串的末尾
    return dp[m][n]
```

运行：`("abcde", "ace")` → `3`，`("abc", "abc")` → `3`，`("abc", "def")` → `0`，`("a", "a")` → `1`，`("bl", "yby")` → `1`，两个 1000 个 `"a"` 的串 → `1000`。

**复杂度。** 时间 `O(mn)`：外层 `m` 次、内层 `n` 次，每格常数；空间 `O(mn)`：`(m + 1) × (n + 1)` 的表。

**写法要点。**
- `[[0] * (n + 1) for _ in range(m + 1)]`：每行是新列表，且第 0 行、第 0 列天然是 `0`，不需要单独初始化。
- `enumerate(text1, 1)`、`enumerate(text2, 1)` 让 `i`、`j` 从 `1` 开始，直接就是前缀长度，同时 `a`、`b` 是当前字符，不用写 `text1[i - 1]`。
- 相等与不等两支分开写成 `if` / `else`，三个依赖格子 `dp[i-1][j-1]`、`dp[i-1][j]`、`dp[i][j-1]` 一眼可见。
