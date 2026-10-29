---
id: tlc-as-far-from-land-as-possible-2-code
node: a.as-far-from-land-as-possible
type: qa
step: 2
---
## Q
**LC 1162 地图分析**｜写出 Python 实现

`n x n` 网格（`1 <= n <= 100`），0 海洋 1 陆地，求海洋格到最近陆地的曼哈顿距离的最大值；只有陆地或只有海洋时返回 `-1`。要求 `O(n^2)`。

## A
**思路。** 所有陆地距离为 0，一起入队；BFS 每向外一层距离加 1，海洋格第一次被到达时的距离就是它到最近陆地的距离。BFS 按层推进，最后赋出的距离就是最大值。

```python
from collections import deque


def max_distance(grid: list[list[int]]) -> int:
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]          # -1 表示还没被 BFS 到达
    queue = deque((r, c) for r in range(n) for c in range(n) if grid[r][c])
    for r, c in queue:                           # 所有陆地同时作为起点，距离 0
        dist[r][c] = 0
    if not queue or len(queue) == n * n:         # 全是海洋或全是陆地
        return -1
    far = 0
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] < 0:
                dist[nr][nc] = far = dist[r][c] + 1   # 第一次到达就是到最近陆地的距离
                queue.append((nr, nc))
    return far
```

运行：`[[1,0,1],[0,0,0],[1,0,1]]` → `2`，`[[1,0,0],[0,0,0],[0,0,0]]` → `4`，`[[0,0],[0,0]]` → `-1`，`[[1,1],[1,1]]` → `-1`；`100 x 100` 只有左上角是陆地 → `198`。

**复杂度。** 时间 `O(n^2)`：每格最多入队一次，每次检查 4 个邻居；空间 `O(n^2)`：`dist` 表和队列。

**写法要点。** `deque` 用生成器一次装入所有源点，`popleft` 是 `O(1)`；`dist` 兼作「已访问」标记，少一张表；`0 <= nr < n` 是链式比较；`dist[nr][nc] = far = ...` 链式赋值从左到右给两个目标赋同一个值，因为 BFS 的层数不降，最后一次赋值就是最大距离；`[[-1] * n for _ in range(n)]` 而不是 `[[-1] * n] * n`，后者每行是同一个列表。
