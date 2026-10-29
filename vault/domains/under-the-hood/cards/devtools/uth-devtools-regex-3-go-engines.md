---
id: uth-devtools-regex-3-go-engines
node: devtools.regex
type: qa
step: 3
---
## Q
**Go 怎么做到既快又线性**｜Go · regexp · 1.25

保证线性，是不是意味着 Go 的正则每次都在慢速模拟 NFA？

## A
**背景。** 线性时间的保证，会不会意味着每次都在慢速模拟状态图？不会：Go 会先看正则和输入的特点，在三种引擎里挑最合适的一种。

**结构。** 编译后按情况选：onepass（模式没有歧义，每一步只有一种走法，一遍扫完）→ 位状态回溯（bitstate backtracker，回溯，但记住走过的状态）→ NFA 模拟（并行推进所有候选）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<rect x="150" y="14" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">模式无歧义?</text>
<rect x="14" y="14" width="100" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="64" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">onepass</text>
<line x1="150" y1="28" x2="121" y2="28" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M116.0,28.0 L122.8,24.7 L122.8,31.3 Z" fill="currentColor" stroke="none"/>
<text x="133" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">是</text>
<text x="64" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">一遍扫完</text>
<line x1="235" y1="42" x2="235" y2="65" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M235.0,70.0 L231.7,63.2 L238.3,63.2 Z" fill="currentColor" stroke="none"/>
<text x="245" y="60" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">否</text>
<rect x="150" y="70" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">指令 ≤ 500 且输入小?</text>
<rect x="14" y="70" width="100" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="64" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">位状态回溯</text>
<line x1="150" y1="84" x2="121" y2="84" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M116.0,84.0 L122.8,80.7 L122.8,87.3 Z" fill="currentColor" stroke="none"/>
<text x="133" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">是</text>
<text x="64" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每个状态只走一次</text>
<line x1="235" y1="98" x2="235" y2="121" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M235.0,126.0 L231.7,119.2 L238.3,119.2 Z" fill="currentColor" stroke="none"/>
<text x="245" y="116" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">否</text>
<rect x="150" y="126" width="170" height="28" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="235" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">NFA 并行模拟</text>
<text x="235" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">兜底 保证线性</text>
</svg>
```

**细节。**

- 回溯器给每个（指令, 位置）一位 `visited`，每个状态最多走一次，所以仍然是线性
- 只在指令数不超过 500、输入长度小于 262144 ÷ 指令数时才用它：位图小
- 否则落到 NFA，并行推进所有候选线程

**为什么。** 小输入上回溯常数小、速度快；大输入再用 NFA 保证上界。靠“记住走过的状态”，回溯也能变线性。

**例题：** LC 10 正则表达式匹配

实现支持 `.`（任意单个字符）和 `*`（零个或多个前一个元素）的正则匹配，必须匹配整个 `s`。例：`s="aa", p="a*"` → `true`；`s="ab", p=".*"` → `true`。

```python
from functools import cache


def is_match(s: str, p: str) -> bool:
    @cache
    def match(i: int, j: int) -> bool:      # s[i:] 能否被 p[j:] 整个匹配
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], '.')   # 当前字符能否匹配 p[j]
        if j + 1 < len(p) and p[j + 1] == '*':
            # 星号两条路：匹配零次（跳过 "x*"），或匹配一次后留在原位继续
            return match(i, j + 2) or (first and match(i + 1, j))
        return first and match(i + 1, j + 1)

    return match(0, 0)
```
