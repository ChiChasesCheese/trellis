---
id: tlc-patterns-graph-traversal-2-template
node: patterns.graph-traversal
type: qa
step: 2
---
## Q
**图与网格的 BFS / DFS｜模板：连通块计数与多源 BFS**

写出网格上「岛屿数量」（LC 200）的迭代 DFS 模板，以及「腐烂的橘子」（LC 994）的多源 BFS 模板。

## A
**连通块（迭代 DFS）：**

```python
def num_islands(grid: list[list[str]]) -> int:
    m, n = len(grid), len(grid[0])
    seen = [[False] * n for _ in range(m)]
    count = 0
    for r in range(m):
        for c in range(n):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                seen[r][c] = True          # 入栈时就标记，不要等到弹出
                stack = [(r, c)]
                while stack:
                    x, y = stack.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        a, b = x + dx, y + dy
                        if 0 <= a < m and 0 <= b < n and grid[a][b] == "1" and not seen[a][b]:
                            seen[a][b] = True
                            stack.append((a, b))
    return count
```

运行：`[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]` → `1`；`[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]` → `3`。`300 x 300` 全陆地也正常返回（显式栈没有递归深度问题）。时间、空间 `O(mn)`。

**多源 BFS（按分钟分层）：**

```python
from collections import deque
def oranges_rotting(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    q = deque((r, c) for r in range(m) for c in range(n) if grid[r][c] == 2)   # 所有腐烂橘子同时入队
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while q and fresh:
        minutes += 1
        for _ in range(len(q)):            # 一轮 = 一分钟
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = r + dr, c + dc
                if 0 <= a < m and 0 <= b < n and grid[a][b] == 1:
                    grid[a][b] = 2
                    fresh -= 1
                    q.append((a, b))
    return -1 if fresh else minutes
```

运行：`[[2,1,1],[1,1,0],[0,1,1]]` → `4`；`[[2,1,1],[0,1,1],[1,0,1]]` → `-1`；`[[0,2]]` → `0`。

两个模板的区别：DFS 只关心「访问了哪些」，用栈；BFS 关心「第几层」，用队列并按层展开。把所有起点同时入队，等价于一个虚拟超级源点。
