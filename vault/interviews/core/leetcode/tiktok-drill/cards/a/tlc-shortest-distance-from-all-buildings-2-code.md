---
id: tlc-shortest-distance-from-all-buildings-2-code
node: a.shortest-distance-from-all-buildings
type: qa
step: 2
---
## Q
**LC 317 离建筑物最近的距离**｜写出 Python 实现

`grid` 是 `m × n`（`1 <= m, n <= 50`），值 `0` 空地、`1` 建筑、`2` 障碍，至少一幢建筑。只能上下左右走，建筑和障碍不能穿过。返回空地到所有建筑的最短总距离；没有任何空地能到达全部建筑则返回 `-1`。

## A
**思路。** 对每幢建筑做一次层序 BFS：每扩展一层，距离加一，给新到达的空地累加距离、累加到达计数。所有建筑处理完后，在到达计数等于建筑总数的空地里取总距离最小值。

```python
from collections import deque

def shortest_distance(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    total = [[0] * n for _ in range(m)]        # total[r][c]：空地 (r, c) 到所有已搜过的建筑的距离之和
    reach = [[0] * n for _ in range(m)]        # reach[r][c]：能走到 (r, c) 的建筑数
    buildings = 0
    for br in range(m):
        for bc in range(n):
            if grid[br][bc] != 1:
                continue
            buildings += 1
            seen = [[False] * n for _ in range(m)]
            seen[br][bc] = True
            queue = deque([(br, bc)])
            dist = 0
            while queue:
                dist += 1                      # 当前层的邻居距离建筑 dist
                for _ in range(len(queue)):
                    r, c = queue.popleft()
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 0 and not seen[nr][nc]:
                            seen[nr][nc] = True
                            total[nr][nc] += dist
                            reach[nr][nc] += 1
                            queue.append((nr, nc))
    return min((total[r][c] for r in range(m) for c in range(n)
                if grid[r][c] == 0 and reach[r][c] == buildings), default=-1)
```

运行：`[[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]` → `7`，`[[1,0]]` → `1`，`[[1]]` → `-1`，`[[1,0,2,1]]` → `-1`；`50 × 50`、`625` 幢建筑均匀分布 → 约 `0.2` 秒。

**复杂度。** 时间 `O(B · mn)`：每幢建筑一次 BFS，每次最多访问全部空地；空间 `O(mn)`。

**写法要点。** `for _ in range(len(queue))` 按层处理，`dist` 就是层号，不必在队列里存距离；`min(..., default=-1)` 用生成器和 `default` 同时处理「没有合格空地」；`seen` 每次新建，因为每幢建筑的访问集合互不相干，`total` / `reach` 则跨建筑累加；初始化二维数组用 `[[0] * n for _ in range(m)]`，不能写 `[[0] * n] * m`。
