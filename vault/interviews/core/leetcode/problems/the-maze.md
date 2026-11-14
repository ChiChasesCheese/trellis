---
slug: the-maze
---
## Q
**LC 490 迷宫**｜Medium

迷宫 `maze` 里 `0` 是空地、`1` 是墙，外圈也算墙。球从 `start` 向上下左右滚，撞墙才停，停下才能换方向。问球能否停在 `destination`。

## A
**一句话。** BFS 的节点是停点：从停点朝四个方向一直滚到下一格是墙，得到新停点；终点必须是停点，滚过去不算。

```python
def has_path(maze, start, destination):
    m, n = len(maze), len(maze[0])
    start, dest = tuple(start), tuple(destination)
    seen, q = {start}, deque([start])
    while q:
        r, c = q.popleft()
        if (r, c) == dest:    # 必须停在这里，路过不算
            return True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = r, c
            while (0 <= x + dr < m and 0 <= y + dc < n
                   and maze[x + dr][y + dc] == 0):
                x, y = x + dr, y + dc   # 滚到墙前
            if (x, y) not in seen:
                seen.add((x, y))
                q.append((x, y))
    return False
```

**复杂度。** 时间 `O(mn(m + n))`，空间 `O(mn)`。

**易错点。**
- 滚动途中碰到终点就返回 `True`：球停不下来，只有停点等于终点才算。
- 每滚一格就入队：那是普通网格 BFS，球会「中途停下」换方向。

**追问。**
- 求最短滚动距离（LC 505）？：边权是滚过的格数，改 Dijkstra。
- 球每步走一格、但不许右转或掉头？：方向放进状态，在 `(行, 列, 朝向)` 上 BFS。

**同模式。** LC 994 腐烂的橘子、LC 505 迷宫 II、LC 499 迷宫 III、LC 1926 迷宫中离入口最近的出口
