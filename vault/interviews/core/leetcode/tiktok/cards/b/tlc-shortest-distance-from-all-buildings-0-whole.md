---
id: tlc-shortest-distance-from-all-buildings-0-whole
node: b.shortest-distance-from-all-buildings
type: qa
---
## Q
**LC 317 离建筑物最近的距离**｜Hard · LC TikTok 热度 41/100

`m × n` 网格，`0` 是可以自由通过的空地，`1` 是不能通过的建筑，`2` 是不能通过的障碍。要在一块空地上建房子，使它到**所有建筑**的总行走距离（上下左右移动）最短。返回这个最短总距离；若无法建造（没有空地能到达所有建筑）返回 `-1`。`1 <= m, n <= 50`，`grid[i][j]` 是 `0`、`1` 或 `2`，至少有一幢建筑。例：`[[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]` → `7`（落在 `(1,2)`，距离 `3 + 3 + 1`），`[[1,0]]` → `1`，`[[1]]` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 对**每幢建筑**各做一次 BFS，把它到每块可达空地的距离累加进 `total`，同时记下每块空地被多少幢建筑到达（`reach`）；最后在 `reach == 建筑总数` 的空地里取 `total` 最小值。`O(B · mn)`，`B` 是建筑数。

**识别。** 「到多个目标的**距离之和**最小的点」+ 网格 + 障碍：边权都是 `1`，用 BFS 求单源最短路；目标有多个，距离要累加，所以每个目标跑一次 BFS 把结果加起来。`m, n <= 50`，`mn = 2500`：`B · mn` 最坏约 `3 · 10^6`，可行。

**推导。** 暴力：枚举每块空地，对每幢建筑求最短路，`O(E · B · mn)` → 浪费在于一次 BFS 能同时得到「该建筑到所有空地」的距离 → 反过来从建筑出发：每幢建筑 BFS 一次，把 `dist` 累加到所有空地的 `total`；再用 `reach` 过滤出能到达全部建筑的空地（被障碍和建筑隔开的空地不合格）。建筑本身不能穿过，所以 BFS 只扩展 `grid == 0` 的格子。

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

运行：示例 1 → `7`，`[[1,0]]` → `1`，`[[1]]` → `-1`，`[[1,0,2,1]]` → `-1`；`50 × 50` 中 `625` 幢建筑均匀分布 → 约 `0.2` 秒。

**复杂度。** 时间 `O(B · mn)`；空间 `O(mn)`（`total`、`reach`、每次 BFS 的 `seen`）。

**易错点。**
- 不检查 `reach == buildings`：被障碍隔开的空地也可能有较小的 `total`。`[[1,0,2,1]]` 返回 `1`（空地只能到左边的建筑），正确是 `-1`。
- 让 BFS 穿过建筑：建筑不可通行，只能扩展 `grid == 0` 的格子。

**追问。**
- 建筑很多、空地很少：改成从每块空地出发 BFS，数能找到几幢建筑并累加距离，谁少就从谁出发。
- 多次查询或增加建筑：缓存每幢建筑的距离表，累加即可。
- 用曼哈顿距离近似（无障碍时）：总距离最小点是 `x`、`y` 坐标各自的中位数（LC 296 最佳的碰头地点）。

**同模式。** LC 296 最佳的碰头地点、LC 286 墙与门、LC 542 01 矩阵、LC 1162 地图分析。
