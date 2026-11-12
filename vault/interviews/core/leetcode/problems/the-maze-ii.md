---
slug: the-maze-ii
---
## Q
**LC 505 迷宫 II**｜Medium

球在 `0/1` 迷宫（`1` 是墙）里朝一个方向一直滚到撞墙才停。求从 `start` 到在 `destination` 停下所经过的最短格数，到不了返回 `-1`。

## A
**一句话。** 节点是球能停下的位置，边是朝一个方向滚到底，边权是滚过的格数，跑 Dijkstra。

```python
def shortest_distance(maze, start, destination):
    m, n = len(maze), len(maze[0])
    dist = {tuple(start): 0}
    heap = [(0, *start)]
    while heap:
        d, r, c = heappop(heap)
        if [r, c] == destination:    # 弹出的都是停止点
            return d
        if d > dist[r, c]:           # 过期条目
            continue
        for dr, dc in (1, 0), (-1, 0), (0, 1), (0, -1):
            x, y, s = r, c, 0
            while (0 <= x + dr < m and 0 <= y + dc < n
                   and maze[x + dr][y + dc] == 0):
                x, y, s = x + dr, y + dc, s + 1   # 滚到底
            if d + s < dist.get((x, y), inf):
                dist[x, y] = d + s
                heappush(heap, (d + s, x, y))
    return -1
```

**复杂度。** 时间 `O(mn(m+n) log mn)`，空间 `O(mn)`。

**易错点。**
- 每次滚动记距离 `1`：这是 LC 490 的模型，示例 1 得 `7`，应为 `12`。
- 滚动途中经过终点就返回：球必须停下，目的地 `[3,2]` 只能经过，应为 `-1`。

**追问。**
- 要输出具体路径？：记录每个停止点的前驱停止点和方向，到终点后回溯。
- 为什么不用普通 BFS？：边权是滚过的格数，不再相等，BFS 的层序不等于距离序。

**同模式。** LC 490 迷宫、LC 499 迷宫 III、LC 743 网络延迟时间、LC 1631 最小体力消耗路径
