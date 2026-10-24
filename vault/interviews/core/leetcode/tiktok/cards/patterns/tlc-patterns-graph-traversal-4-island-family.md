---
id: tlc-patterns-graph-traversal-4-island-family
node: patterns.graph-traversal
type: qa
step: 4
---
## Q
**图与网格的 BFS / DFS｜岛屿家族：最大面积与不同形状**

最大面积、不同形状的岛屿，在连通块模板上各加了什么？

## A
**LC 695 最大面积**：每个连通块数一下格子数，取最大。

**LC 694 不同形状**：同一个岛屿平移后相同。记录每个格子**相对起点**的偏移，作为形状签名放进 `set`。

```python
def number_of_distinct_islands(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    shapes: set[tuple[tuple[int, int], ...]] = set()
    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                grid[r][c] = 0
                stack, cells = [(r, c)], []
                while stack:
                    x, y = stack.pop()
                    cells.append((x - r, y - c))   # 相对起点的偏移
                    for a, b in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                        if 0 <= a < m and 0 <= b < n and grid[a][b] == 1:
                            grid[a][b] = 0
                            stack.append((a, b))
                shapes.add(tuple(sorted(cells)))   # 排序得到规范形式
    return len(shapes)
```

`[[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]` → `1`；`[[1,1,0,1,1],[1,0,0,0,0],[0,0,0,0,1],[1,1,0,1,1]]` → `3`。
