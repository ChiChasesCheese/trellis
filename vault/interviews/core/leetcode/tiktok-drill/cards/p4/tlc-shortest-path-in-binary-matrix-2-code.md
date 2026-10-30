---
id: tlc-shortest-path-in-binary-matrix-2-code
node: p4.shortest-path-in-binary-matrix
type: qa
step: 2
---
## Q
**LC 1091 二进制矩阵中的最短路径**｜写出 Python 实现

`n x n` 的 0/1 矩阵（`1 <= n <= 100`），从左上角走到右下角，只经过 `0`，8 方向连通，返回最短路径经过的格子数，不通返回 `-1`。

## A
**思路。** 起点或终点是 1 直接返回 `-1`。否则用队列做 BFS，队列项带上已走的格子数；弹出终点时返回；扩展 8 个邻居，入队时就标记已访问。

```python
from collections import deque
from itertools import product

def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1                                    # 起点或终点被堵死
    dirs = [(dr, dc) for dr, dc in product((-1, 0, 1), repeat=2) if dr or dc]   # 8 个方向
    seen = [row[:] for row in grid]                  # 1 = 障碍或已入队；不改动入参
    seen[0][0] = 1
    q = deque([(0, 0, 1)])                           # (行, 列, 路径经过的格子数)
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = 1                     # 入队时就标记，每格只入队一次
                q.append((nr, nc, d + 1))
    return -1
```

运行：`[[0,1],[1,0]]` → `2`，`[[0,0,0],[1,1,0],[1,1,0]]` → `4`，`[[1,0,0],[1,1,0],[1,1,0]]` → `-1`，`[[0]]` → `1`，`[[1]]` → `-1`，`100 x 100` 全 0 → `100`。

**复杂度。** 时间 `O(n^2)`：每格最多入队一次，每次枚举 8 个邻居；空间 `O(n^2)`：`seen` 加队列。

**写法要点。** `itertools.product((-1, 0, 1), repeat=2)` 生成 9 个偏移，过滤掉 `(0, 0)` 就是 8 方向，比手写八个元组不易漏；`deque.popleft()` 是 `O(1)`，`list.pop(0)` 是 `O(n)`；`[row[:] for row in grid]` 复制二维数组（不能 `grid[:]`，那只复制外层）；把「已访问」和「障碍」合并进同一张表，省一次判断。
