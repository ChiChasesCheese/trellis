---
id: uth-python-iterators-generators-4-lazy-genexp
node: python.iterators-generators
type: qa
step: 4
---
## Q
**生成器表达式：省多少内存、有什么坑**｜Python · CPython 3.14

`sum(x*x for x in range(10**6))` 和 `sum([x*x for x in range(10**6)])` 差在哪？

## A
**背景。** 列表推导式会一口气把所有结果算出来存好。如果后面只是求和，或者只想找第一个满足条件的元素，存下来就是浪费。

**结构。** 把 `[...]` 换成 `(...)` 就是生成器表达式：它不存结果，外面每要一个，才算一个。它本身也是一个生成器对象。`sum`、`any`、`max`、`next` 都是这样逐个拉取。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="6" y="20" width="60" height="30" rx="3"/>
<rect x="276" y="20" width="58" height="30" rx="3"/>
<line x1="116" y1="42" x2="66" y2="42"/>
<line x1="276" y1="42" x2="226" y2="42"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="116" y="20" width="110" height="30" rx="3"/>
<rect x="20" y="112" width="300" height="24" rx="3"/>
<rect x="20" y="150" width="3" height="24" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="66" y1="30" x2="116" y2="30"/>
<line x1="226" y1="30" x2="276" y2="30"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="66.0,42.0 72.0,39.0 72.0,45.0"/>
<polygon points="226.0,42.0 232.0,39.0 232.0,45.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="116.0,30.0 110.0,33.0 110.0,27.0"/>
<polygon points="276.0,30.0 270.0,33.0 270.0,27.0"/>
</g>
<g fill="currentColor">
<text x="36" y="39">sum</text>
<text x="171" y="39">x*x for x</text>
<text x="305" y="39">range</text>
<text x="170" y="128">列表推导式 8,448,728 B</text>
<text x="32" y="167" text-anchor="start">生成器表达式 200 B</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="91" y="66" font-size="11">给一个</text>
<text x="251" y="66" font-size="11">给一个</text>
<text x="170" y="100">10^6 个元素时的对象大小 (实测)</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="91" y="12" font-size="11">要一个</text>
<text x="251" y="12" font-size="11">要一个</text>
</g>
</g>
</svg>
```

**细节。**

- 实测 3.14.8：`sys.getsizeof` 对 10^6 个元素的列表推导式是 8,448,728 字节（还不含元素对象本身），对生成器表达式只有 200 字节。
- `any(...)` 和 `next((...), None)` 找到第一个就停，后面的元素根本不会被计算。
- 代价：只能走一遍，不能 `len()`，也不能按下标取。

**坑。** 生成器里漏出的 `StopIteration` 不会悄悄结束循环，而会被改成 `RuntimeError: generator raised StopIteration`（3.7 起一律如此）。

**例题：** LC 934 最短的桥

`n x n` 的 0/1 矩阵里恰好有两座岛（上下左右相连的 `1`）。可以把 `0` 翻成 `1`，求连通两座岛最少要翻几个 `0`。`2 <= n <= 100`。例：`[[0,1],[1,0]]` 得 `1`，`[[0,1,0],[0,0,0],[0,0,1]]` 得 `2`。

```python
from collections.abc import Iterator

def shortest_bridge(grid: list[list[int]]) -> int:
    n = len(grid)

    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j])   # 第一块陆地
    seen = {start}
    stack = [start]
    while stack:                                   # 第一步：DFS 圈出第一座岛
        x, y = stack.pop()
        for a, b in neighbors(x, y):
            if grid[a][b] and (a, b) not in seen:
                seen.add((a, b))
                stack.append((a, b))
    frontier = list(seen)                          # 第二步：整座岛作为起点的多源 BFS，一层 = 翻一格水
    flips = 0
    while frontier:
        nxt: list[tuple[int, int]] = []
        for x, y in frontier:
            for a, b in neighbors(x, y):
                if (a, b) not in seen:
                    if grid[a][b]:                 # 碰到第二座岛：已经翻的层数就是答案
                        return flips
                    seen.add((a, b))
                    nxt.append((a, b))
        frontier = nxt
        flips += 1
    return -1
```
