---
id: tlc-patterns-graph-traversal-5-large-island
node: patterns.graph-traversal
type: qa
step: 5
---
## Q
**图与网格的 BFS / DFS｜最大人工岛（LC 827）：先标号再枚举 0 格**

可以把一个 0 变成 1，最大的岛屿面积是多少？为什么相邻岛屿要去重？

## A
思路：① 给每个岛编号并记面积；② 对每个 `0` 格，把四周**不同**岛屿的面积相加再加 1。

```python
def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    area: dict[int, int] = {}
    label = 2                              # 从 2 开始编号，避免和 0/1 混淆
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                grid[r][c] = label
                stack, size = [(r, c)], 0
                while stack:
                    x, y = stack.pop()
                    size += 1
                    for a, b in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                        if 0 <= a < n and 0 <= b < n and grid[a][b] == 1:
                            grid[a][b] = label
                            stack.append((a, b))
                area[label] = size
                label += 1
    best = max(area.values(), default=0)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                near = {grid[a][b] for a, b in ((r+1, c), (r-1, c), (r, c+1), (r, c-1))
                        if 0 <= a < n and 0 <= b < n and grid[a][b] > 1}   # 集合去重
                best = max(best, 1 + sum(area[k] for k in near))
    return best
```

`[[1,0],[0,1]]` → `3`；`[[1,1],[1,0]]` → `4`；`[[1,1],[1,1]]` → `4`。去重很关键：`[[1,1,0],[1,0,0],[0,0,0]]` 中 `(1,1)` 的上、左邻居是同一座面积 3 的岛，不用集合去重会得到 `7`，正确是 `4`。
