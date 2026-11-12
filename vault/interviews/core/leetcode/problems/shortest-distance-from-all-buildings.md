---
slug: shortest-distance-from-all-buildings
---
## Q
**LC 317 离建筑物最近的距离**｜Hard

网格里 `0` 空地、`1` 建筑、`2` 障碍；在空地上建房，使到所有建筑的步行距离之和最小，无法到达所有建筑返回 `-1`。

## A
**一句话。** 从每幢建筑各做一次 BFS，累加距离并记录可达建筑数，在可达全部建筑的空地里取最小。

```python
def shortest_distance(grid):
    m, n = len(grid), len(grid[0])
    total = [[0] * n for _ in range(m)]   # 到各建筑的距离和
    reach = [[0] * n for _ in range(m)]   # 能到达的建筑数

    def bfs(br, bc):
        seen = {(br, bc)}
        q = deque([(br, bc)])
        d = 0
        while q:
            d += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for dx, dy in (1,0), (-1,0), (0,1), (0,-1):
                    x, y = r + dx, c + dy
                    if not (0 <= x < m and 0 <= y < n):
                        continue
                    if grid[x][y] or (x, y) in seen:
                        continue
                    seen.add((x, y))
                    total[x][y] += d
                    reach[x][y] += 1
                    q.append((x, y))

    cnt = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                cnt += 1
                bfs(i, j)
    cells = [(i, j) for i in range(m) for j in range(n)]
    return min((total[i][j] for i, j in cells
                if grid[i][j] == 0 and reach[i][j] == cnt),
               default=-1)
```

**复杂度。** 时间 `O(B·mn)`（`B` 为建筑数），空间 `O(mn)`。

**易错点。**
- 不检查 `reach == cnt`：被隔开的空地 `total` 偏小，`[[1,0,2,1]]` 返回 `1`，应为 `-1`。
- BFS 穿过建筑：建筑不可通行，只扩展 `grid == 0` 的格子。

**追问。**
- 建筑很多、空地很少怎么办？：反过来从每块空地 BFS，找到全部建筑即可。
- 无障碍时呢？：就是 LC 296，行、列坐标各取中位数。

**同模式。** LC 296 最佳的碰头地点、LC 286 墙与门、LC 542 01 矩阵、LC 1162 地图分析
