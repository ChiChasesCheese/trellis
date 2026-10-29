---
id: uth-devtools-regex-1-backtrack-automata
node: devtools.regex
type: qa
step: 1
---
## Q
**回溯引擎 vs 自动机**｜Python re · Go regexp

为什么一条正则能把 Python 的 `re` 卡死，而同样的正则在 Go 里不会？

## A
**背景。** 匹配正则有两种思路。一是回溯（backtracking）：沿着模式一条分支一条分支地试，试不通就退回上一步换一条；直观，也容易支持高级语法，但最坏要试遍指数多的路径。二是自动机：把正则编成状态图，读一个字符，就同时记下“现在可能处在的所有状态”，一遍扫完，时间与输入长度成线性。

**结构。** Python、Java、PCRE 是回溯匹配器。RE2 和 Go 的 `regexp` 用自动机（Thompson 提出的 NFA 模拟），逐字符推进状态集合。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="85" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">回溯</text>
<text x="255" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">自动机</text>
<line x1="170" y1="8" x2="170" y2="150" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="85" y1="50" x2="55" y2="70" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="85" y1="50" x2="115" y2="70" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="55" y1="88" x2="35" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="55" y1="88" x2="65" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="115" y1="88" x2="95" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="115" y1="88" x2="125" y2="108" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="85" cy="40" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="55" cy="78" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="115" cy="78" r="8" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="35" cy="116" r="8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="35" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">x</text>
<circle cx="65" cy="116" r="8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="65" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">x</text>
<circle cx="95" cy="116" r="8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="95" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">x</text>
<circle cx="125" cy="116" r="8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="125" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">x</text>
<text x="85" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">试到失败再退 最坏指数</text>
<circle cx="205" cy="44" r="9" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="205" cy="74" r="9" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="205" cy="104" r="9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="255" cy="44" r="9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="255" cy="74" r="9" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="255" cy="104" r="9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="305" cy="44" r="9" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<circle cx="305" cy="74" r="9" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<circle cx="305" cy="104" r="9" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<line x1="214" y1="44" x2="246" y2="74" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="214" y1="74" x2="246" y2="74" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="264" y1="74" x2="296" y2="74" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="264" y1="74" x2="296" y2="104" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="152" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">同时走所有分支 线性</text>
</svg>
```

**细节。**

- Russ Cox 的经典例子：`a?` 重复 n 次再接 `a` 重复 n 次，去匹配 n 个 `a`；n = 29 时 Perl 要六十多秒，Thompson NFA 约 20 微秒
- Go 文档明确保证匹配时间与输入大小成线性
- RE2 不支持反向引用和广义断言（环视）

**为什么。** 反向引用要记住之前匹配到的内容，自动机做不到；线性时间的保证，是用放弃这些语法换来的。

**例题：** LC 44 通配符匹配（同类：LC 10 正则表达式匹配）

实现支持 `?`（任意单个字符）和 `*`（任意字符序列，含空序列）的通配符匹配，必须匹配整个 `s`。例：`s="aa", p="a"` → `false`；`p="*"` → `true`；`s="cb", p="?a"` → `false`。

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
