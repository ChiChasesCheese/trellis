---
id: uth-devtools-diff-3-patience
node: devtools.diff
type: qa
step: 3
---
## Q
**patience diff：先锚定唯一行**｜Git · diff-algorithm · 2.56

挪动一个函数后，默认 diff 有时把一堆 `}` 配错位置，`--patience` 为什么更好看？

## A
**背景。** 把一个函数整段挪到文件别处，默认的 diff 常把大量 `}`、空行配错位置，读起来一团糟。原因是 Myers 只追求增删行数最少，不管可读性：重复的行配给谁，行数都一样少。patience 的办法：先找“在两个文件里各只出现一次”的行（函数签名之类）当锚点，因为它们几乎肯定是同一行。

**结构。** patience：把这些唯一行配成对，取它们的最长递增子序列（配对后位置不交叉的最长一组）做锚点；锚点之间的区间递归处理，没有唯一行的区间退回 Myers。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<text x="72" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">旧</text>
<text x="268" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">新</text>
<rect x="40" y="32" width="64" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="72" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">foo()</text>
<rect x="236" y="32" width="64" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="268" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">foo()</text>
<rect x="40" y="64" width="64" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">}</text>
<rect x="236" y="64" width="64" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">}</text>
<rect x="40" y="96" width="64" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="72" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">bar()</text>
<rect x="236" y="96" width="64" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="268" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">baz()</text>
<rect x="40" y="128" width="64" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="72" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">}</text>
<rect x="236" y="128" width="64" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">}</text>
<rect x="40" y="160" width="64" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="72" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">baz()</text>
<rect x="236" y="160" width="64" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="268" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">bar()</text>
<line x1="104" y1="43" x2="236" y2="43" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="104" y1="171" x2="236" y2="107" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="104" y1="107" x2="236" y2="171" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.45"/>
<text x="170" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">交叉 丢掉</text>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">唯一行配对 取不交叉的最长一组当锚点</text>
<text x="170" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">} 不是唯一行 不参与</text>
</svg>
```

**细节。**

- 选项：`--diff-algorithm=myers|minimal|patience|histogram`，默认 `myers`
- `histogram` 是 patience 的扩展，支持“出现次数少”的行
- 唯一行（函数签名之类）比 `}`、空行更能代表“真正没变的代码”

**为什么。** 用唯一行当锚点，更符合人对“哪里没变”的直觉。

**例题：** LC 300 最长递增子序列

求数组中最长严格递增子序列（不要求连续）的长度，进阶要求 O(n log n)。例：`[10,9,2,5,3,7,101,18]` → 4（如 `[2,3,7,101]`）。

```python
from bisect import bisect_left


def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []                          # tails[k] = 长度为 k+1 的递增子序列的最小结尾
    for x in nums:
        i = bisect_left(tails, x)                  # 严格递增：第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)                        # x 比所有结尾都大：最长长度 +1
        else:
            tails[i] = x                           # 让长度 i+1 的结尾变得更小，对后面更有利
    return len(tails)
```
