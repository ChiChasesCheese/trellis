---
id: uth-python-dunder-protocols-5-fallback
node: python.dunder-protocols
type: qa
step: 5
---
## Q
**没写 __bool__ 或 __contains__ 时怎么办**｜Python · CPython 3.14

为什么只写了 `__len__` 的容器，空的时候 `if box:` 为假？没写 `__contains__` 的类，`x in obj` 为什么也能用？

## A
**背景。** 协议太多，要求每个都写全，使用者会累。Python 的做法是定一条「回退链」：先找最直接的方法，没有就退到更通用的那个，这样实现一个最基本的方法，就能得到一批能力。

**结构。** 三条链：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="146" y1="24" x2="156" y2="24"/>
<rect x="156" y="10" width="84" height="28" rx="3"/>
<line x1="240" y1="24" x2="250" y2="24"/>
<rect x="250" y="10" width="60" height="28" rx="3"/>
<line x1="154" y1="84" x2="164" y2="84"/>
<rect x="164" y="70" width="66" height="28" rx="3"/>
<line x1="230" y1="84" x2="240" y2="84"/>
<rect x="240" y="70" width="92" height="28" rx="3"/>
<line x1="128" y1="144" x2="138" y2="144"/>
<rect x="138" y="130" width="92" height="28" rx="3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="62" y="10" width="84" height="28" rx="3"/>
<rect x="62" y="70" width="92" height="28" rx="3"/>
<rect x="62" y="130" width="66" height="28" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="156.0,24.0 150.0,27.0 150.0,21.0"/>
<polygon points="250.0,24.0 244.0,27.0 244.0,21.0"/>
<polygon points="164.0,84.0 158.0,87.0 158.0,81.0"/>
<polygon points="240.0,84.0 234.0,87.0 234.0,81.0"/>
<polygon points="138.0,144.0 132.0,147.0 132.0,141.0"/>
</g>
<g fill="currentColor">
<text x="104" y="28">__bool__</text>
<text x="198" y="28">__len__</text>
<text x="280" y="28">恒为真</text>
<text x="108" y="88">__contains__</text>
<text x="197" y="88">__iter__</text>
<text x="286" y="88">__getitem__</text>
<text x="95" y="148">__iter__</text>
<text x="184" y="148">__getitem__</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="170" y="182">箭头: 没有这个方法, 就退到下一个</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="4" y="29" text-anchor="start">bool(x)</text>
<text x="4" y="89" text-anchor="start">x in s</text>
<text x="4" y="149" text-anchor="start">iter(s)</text>
</g>
</g>
</svg>
```

**细节。**

- 实测：只有 `__getitem__`（下标 0、1、2 返回 0、10、20，下标 3 抛 `IndexError`）的类，`list(obj)` 得 `[0, 10, 20]`，`20 in obj` 为真。
- 回退到逐个比较时，用的是 `x is z or x == z`。

**为什么。** 向后兼容旧的序列写法，也让「只实现最少的方法」就够用。

**坑。** 自定义容器的 `__len__` 返回 0 时，`if obj:` 和 `while obj:` 都为假，这和「是不是 `None`」是两回事；要判断有没有对象，写 `is None`。

**例题：** LC 200 岛屿数量

给 `m x n` 的网格，`'1'` 是陆地、`'0'` 是水，上下左右相连的陆地算一座岛，求岛屿数量。`1 <= m, n <= 300`。例：`[["1","1","0"],["0","1","0"],["0","0","1"]]` 得 `2`。

```python
from collections import deque

def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def sink(sr: int, sc: int) -> None:
        queue = deque([(sr, sc)])
        grid[sr][sc] = "0"  # 入队即淹没，避免重复入队
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"
                    queue.append((nr, nc))

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
```
