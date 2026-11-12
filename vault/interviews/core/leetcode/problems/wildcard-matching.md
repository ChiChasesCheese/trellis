---
slug: wildcard-matching
---
## Q
**LC 44 通配符匹配**｜Hard

`?` 匹配任意单个字符，`*` 匹配任意序列（含空），判断模式 `p` 能否完整匹配字符串 `s`。

## A
**一句话。** 二维 DP：`dp[i][j]` 表示 `s[:i]` 能否被 `p[:j]` 匹配，`*` 取「匹配空」或「多吞一个」。

```python
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):       # s 为空：只有连续 * 能匹配
        dp[0][j] = dp[0][j - 1] and p[j - 1] == "*"
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] in ("?", s[i - 1]):
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 漏掉第 0 行初始化：`("aa", "*")` 和 `("", "*")` 都得 `False`，应为 `True`。
- 把 `*` 当 `?` 只取左上角：`("adceb", "*a*b")` 得 `False`，应为 `True`。
- 第 0 列设成 `True`：`("a", "")` 得 `True`，应为 `False`。

**追问。**
- 想要 `O(1)` 额外空间？：贪心加回溯到最近一个 `*`（只有最后一个值得回溯），最坏仍是 `O(mn)`。
- 与 LC 10 的区别？：那里 `*` 绑定前一个字符，转移是 `dp[i][j-2]`，或前字符兼容时的 `dp[i-1][j]`。

**同模式。** LC 10 正则表达式匹配、LC 72 编辑距离、LC 97 交错字符串、LC 115 不同的子序列
