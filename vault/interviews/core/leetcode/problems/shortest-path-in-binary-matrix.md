---
slug: shortest-path-in-binary-matrix
---
## Q
**LC 1091 二进制矩阵中的最短路径**｜Medium

`n×n` 的 0/1 矩阵，只走 `0` 的格子、可沿 8 个方向，求左上到右下的最短路径经过的格子数，不存在返回 `-1`。

## A
**一句话。** 无权最短路用 BFS：向 8 邻居逐层扩展，队列里带已走格子数，入队即标记。

```python
def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n-1][n-1]:
        return -1
    seen = [row[:] for row in grid]   # 1 = 障碍或已入队
    seen[0][0] = 1
    q = deque([(0, 0, 1)])            # 格子数从 1 起算
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                x, y = r + dr, c + dc
                if not (0 <= x < n and 0 <= y < n):
                    continue
                if not seen[x][y]:
                    seen[x][y] = 1
                    q.append((x, y, d + 1))
    return -1
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 只用 4 个方向：`[[0,1],[1,0]]` 得 `-1`，应为 `2`。
- 不先查起点：`[[1,0],[0,0]]` 起点是障碍，应为 `-1`。
- 长度按边数算：起点就是第 1 格，`[[0]]` 答案是 `1`。

**追问。**
- 怎么输出路径？：用 `parent` 字典兼作已访问集合，到终点后回溯。
- 斜走代价 `√2` 呢？：不再是无权图，改用 Dijkstra。

**同模式。** LC 542 01 矩阵、LC 994 腐烂的橘子、LC 752 打开转盘锁、LC 1293 网格中的最短路径
