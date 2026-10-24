---
id: tlc-patterns-dp-grid-string-6-regex
node: patterns.dp-grid-string
type: qa
step: 6
---
## Q
**动态规划：网格、双串与区间｜正则表达式匹配（LC 10）：`*` 的两种选择**

支持 `.` 和 `*` 的整串匹配，`dp[i][j]` 怎么定义？遇到 `*` 时怎样转移？

## A
`dp[i][j]` = 字符串 `s` 的前 `i` 个字符是否被模式 `p` 的前 `j` 个字符完全匹配。

```python
def is_match(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(2, n + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]        # 空串可以匹配 "a*b*" 这类
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 2]    # '*' 匹配零个前一个字符
                if p[j - 2] in (s[i - 1], "."):
                    dp[i][j] = dp[i][j] or dp[i - 1][j]   # 匹配至少一个：吃掉 s[i-1]，p 不动
            elif p[j - 1] in (s[i - 1], "."):
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
```

运行：`("aa", "a")` → `False`；`("aa", "a*")` → `True`；`("ab", ".*")` → `True`；`("aab", "c*a*b")` → `True`；`("mississippi", "mis*is*p*.")` → `False`；`("", "a*")` → `True`。

- `*` 绑定它**前面那个字符**（`a*` 是一个整体）：要么匹配零个（`dp[i][j-2]`，把 `a*` 整体丢掉），要么匹配一个或多个（前提：`p[j-2]` 能匹配 `s[i-1]`，则看 `dp[i-1][j]`，`p` 不动）。
- 第 0 行初始化是关键：`s` 为空时，只有 `x*y*...` 形式能匹配。
- **把 `*` 当通配符的反例**：把 `*` 当作"匹配任意序列"，`("ab", "a*")` 会得到 `True`，正确答案 `False`（`a*` 只能匹配若干个 `a`）。
- 时间、空间 `O(mn)`，`m, n <= 20` 很小。对照：LC 44 通配符匹配里 `*` 才是"任意序列"，转移不同。
