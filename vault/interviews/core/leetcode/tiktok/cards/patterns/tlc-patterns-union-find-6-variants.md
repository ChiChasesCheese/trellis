---
id: tlc-patterns-union-find-6-variants
node: patterns.union-find
type: qa
step: 6
---
## Q
**并查集（Union-Find）｜变形：按块统计（LC 827）与带权并查集（LC 399）**

最大人工岛为什么要对四邻居所属的块去重？除法求值怎样让并查集带上比值？

## A
- **按块统计**：先给每个连通块编号（并查集的根，或 DFS 打标签）并统计每块面积；再对每个 `0` 格看它的四个邻居分属哪些块，同一个块可能从几个方向碰到，所以先按块编号去重，再把这些块的面积相加，加上这个格子本身。水的编号记作 `0`，面积记 `0`（例：LC 827 最大人工岛）。
- **带权并查集**：每个点记 `ratio[x] = x / parent[x]`。`find` 压缩路径时累乘比值：`x/root = (x/parent) * (parent/root)`；`union(a, b, v)`（`a / b = v`）把 `a` 的根挂到 `b` 的根下，根与根的比值设为 `v * ratio[b] / ratio[a]`。查询 `c / d`：两者在同一个块里时等于 `ratio[c] / ratio[d]`，否则 `-1.0`。例：`a/b=2, b/c=3` 时 `a/c = 6.0`，`b/a = 0.5`（例：LC 399 除法求值）。

**例题：** LC 399 除法求值

已知若干 `Ai / Bi = values[i]`，回答每个查询 `Cj / Dj = ?`，无法确定或变量没出现过则为 `-1.0`，`1 <= equations.length <= 20`，`0.0 < values[i] <= 20.0`。

```python
def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}
    def find(x: str) -> str:
        p = parent.setdefault(x, x)
        ratio.setdefault(x, 1.0)
        if p != x:
            root = find(p)
            ratio[x] *= ratio[p]
            parent[x] = root
        return parent[x]
    for (a, b), v in zip(equations, values):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            ratio[ra] = v * ratio[b] / ratio[a]
    ans: list[float] = []
    for c, d in queries:
        if c in parent and d in parent and find(c) == find(d):
            ans.append(ratio[c] / ratio[d])
        else:
            ans.append(-1.0)
    return ans
```

**例题：** LC 827 最大人工岛

给 `n x n` 的二进制矩阵 `grid`，**最多**只能将一格 `0` 变成 `1`。返回执行此操作后，`grid` 中最大的岛屿面积。岛屿由一组上、下、左、右四个方向相连的 `1` 形成。`n == grid.length == grid[i].length`，`1 <= n <= 500`，`grid[i][j]` 为 `0` 或 `1`。

```python
from collections.abc import Iterator

def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    label = [[0] * n for _ in range(n)]            # 0 = 水或还没编号；岛从 1 开始编号
    size: dict[int, int] = {}                      # 岛编号 -> 面积

    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    def dfs(i: int, j: int, tag: int) -> int:      # 给这座岛的每一格打上 tag，返回面积
        label[i][j] = tag
        area = 1
        for a, b in neighbors(i, j):
            if grid[a][b] == 1 and label[a][b] == 0:
                area += dfs(a, b, tag)
        return area

    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1 and label[i][j] == 0:
                tag = len(size) + 1
                size[tag] = dfs(i, j, tag)
    best = max(size.values(), default=0)           # 一格都不翻（或没有 0 可翻）
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                tags = {label[a][b] for a, b in neighbors(i, j)}   # 集合去重：同一座岛可能从几个方向碰到
                best = max(best, 1 + sum(size.get(t, 0) for t in tags))   # 水的编号是 0，不在 size 里，记 0
    return best
```
