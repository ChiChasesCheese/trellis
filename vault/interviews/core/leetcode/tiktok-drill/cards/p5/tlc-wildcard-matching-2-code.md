---
id: tlc-wildcard-matching-2-code
node: p5.wildcard-matching
type: qa
step: 2
---
## Q
**LC 44 通配符匹配**｜写出 Python 实现

字符串 `s` 和模式 `p`（长度都在 `0` 到 `2000`；`s` 只含小写字母，`p` 只含小写字母、`?`、`*`）。`?` 匹配任意单个字符，`*` 匹配任意字符序列（含空），要求整个 `s` 被匹配。返回是否匹配，时间 `O(mn)`。

## A
**思路。** `dp[i][j]` 表示 `s` 的前 `i` 个字符能否被 `p` 的前 `j` 个字符完整匹配。`dp[0][0] = True`；第 0 行：`s` 为空时只有连续的 `*` 能匹配；第 0 列保持 `False`。其余格子：`p[j-1]` 是 `*` 时取「匹配空」（同一行左边一格 `dp[i][j-1]`）或「多吞一个字符」（上一行同列 `dp[i-1][j]`）；是 `?` 或与 `s[i-1]` 相等时取左上角 `dp[i-1][j-1]`。

```python
def is_match(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    # dp[i][j]：s[:i] 能否被 p[:j] 完整匹配
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                                  # 空串匹配空模式
    for j in range(1, n + 1):                        # 第 0 行：s 为空，只有连续的 '*' 能匹配
        dp[0][j] = dp[0][j - 1] and p[j - 1] == "*"
    for i in range(1, m + 1):                        # 第 0 列保持 False：非空 s 不能匹配空模式
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]       # '*' 匹配空 / 再多吞掉 s[i-1]
            elif p[j - 1] in ("?", s[i - 1]):
                dp[i][j] = dp[i - 1][j - 1]
    return dp[m][n]
```

运行：`("aa", "a")` → `False`，`("aa", "*")` → `True`，`("cb", "?a")` → `False`，`("", "*")` → `True`，`("", "?")` → `False`，`("adceb", "*a*b")` → `True`，`("acdcb", "a*c?b")` → `False`。

**复杂度。** 时间 `O(mn)`：每个 `(i, j)` 一次常数转移；空间 `O(mn)`：`(m + 1) × (n + 1)` 的布尔表。

**写法要点。** `p[j - 1] in ("?", s[i - 1])` 用元组成员判断把「通配或相等」合成一个条件；布尔链 `dp[0][j - 1] and p[j - 1] == "*"` 直接得到第 0 行的初始化，不用单独的 `if`；没有写 `else`：不匹配的格子保持建表时的 `False`；`[[False] * (n + 1) for _ in range(m + 1)]` 每行都是新列表。
