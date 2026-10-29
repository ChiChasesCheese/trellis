---
id: tlc-shortest-path-in-binary-matrix-4-followup
node: b.shortest-path-in-binary-matrix
type: qa
step: 4
---
## Q
**LC 1091 二进制矩阵中的最短路径**｜追问

面试官接着问：（1）返回具体路径经过的格子？（2）斜走代价是 `√2`、直走是 `1` 呢？（3）网格很大、起终点距离远，能不能比 BFS 少搜一些格子？

## A
1. **返回路径**：用字典 `parent` 记录每个格子从哪来，同时兼作「已访问」集合；到终点后沿 `parent` 回溯再反转。
```python
from collections import deque
from itertools import product

def shortest_path_cells(grid: list[list[int]]) -> list[tuple[int, int]]:
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return []
    dirs = [(dr, dc) for dr, dc in product((-1, 0, 1), repeat=2) if dr or dc]
    parent: dict[tuple[int, int], tuple[int, int] | None] = {(0, 0): None}
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        if (r, c) == (n - 1, n - 1):
            path, cur = [], (r, c)
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and (nr, nc) not in parent:
                parent[nr, nc] = (r, c)
                q.append((nr, nc))
    return []
```
`[[0,0,0],[1,1,0],[1,1,0]]` 得 `[(0, 0), (0, 1), (1, 2), (2, 2)]`。
2. **带权（`√2` / `1`）**：边权不同，BFS 的"先到就最短"不成立，改 Dijkstra：`heapq` 存 `(距离, 行, 列)`，弹出时若距离大于记录值就跳过（过期堆项）。该例得 `3.414...`。
3. **少搜一些**：A*，估价取切比雪夫距离 `max(n-1-r, n-1-c)`，8 方向统一代价下它永远不高估；或双向 BFS，从起终点同时扩展，各走一半。

**Python 提醒**：`[[0] * n] * n` 的各行是同一个对象；复制二维列表要 `[row[:] for row in grid]` 或 `copy.deepcopy`。
