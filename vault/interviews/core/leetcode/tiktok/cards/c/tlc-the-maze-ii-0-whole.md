---
id: tlc-the-maze-ii-0-whole
node: c.the-maze-ii
type: qa
---
## Q
**LC 505 迷宫 II**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2021-08-10（国内 CodeTop）

迷宫中有一个球，空地为 `0`，墙为 `1`。球可以向上、下、左、右滚动，一直滚到撞墙才停；停下之后才能选新方向。给定 `m x n` 的迷宫 `maze`、起点 `start = [startrow, startcol]` 和终点 `destination = [destinationrow, destinationcol]`，返回球在终点**停下**的最短距离（从起点不含到终点含，经过的空地数），不能在终点停下则返回 `-1`。边界视为墙。`1 <= m, n <= 100`，起点与终点都是空地且不同，迷宫至少有两块空地。例：`maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]`，`start = [0,4]`，`destination = [4,4]` → `12`；`destination = [3,2]` → `-1`（可以经过但不能停下）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 节点是「球能停下的位置」，边是「朝某个方向一直滚到墙」，边权是滚过的格数，在这张带权图上跑 Dijkstra。

**识别。** 「滚到底才停」让每一步的代价不再是 1（滚的格数不同），所以不能用普通 BFS 而要 Dijkstra（最短路，堆优化）。状态只有停下的格子，中途经过的格子不是节点。

**推导。** 暴力 BFS 只数「滚动次数」而不是「距离」，得到的不是最短距离。把每次滚动当成一条边：从停止点 `(r, c)` 出发，往四个方向一直走到下一格是墙或出界，终点 `(nr, nc)` 加上边权 `steps`。每次弹出距离最小的停止点，松弛它的四条边；弹出的恰好是终点就是答案（弹出的都是停止点，所以终点一定是停下来的）。

```python
from heapq import heappop, heappush
from math import inf


def shortest_distance(maze: list[list[int]], start: list[int], destination: list[int]) -> int:
    m, n = len(maze), len(maze[0])
    dist = [[inf] * n for _ in range(m)]
    sr, sc = start
    dist[sr][sc] = 0
    heap = [(0, sr, sc)]                         # (到达该停止点的最短距离, 行, 列)
    while heap:
        d, r, c = heappop(heap)
        if [r, c] == destination:                # 弹出的都是停止点：终点第一次弹出就是最短
            return d
        if d > dist[r][c]:                       # 过期条目（有更短的路径已处理）
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc, steps = r, c, 0
            while 0 <= nr + dr < m and 0 <= nc + dc < n and maze[nr + dr][nc + dc] == 0:
                nr, nc, steps = nr + dr, nc + dc, steps + 1    # 一直滚到下一格是墙或边界
            if d + steps < dist[nr][nc]:
                dist[nr][nc] = d + steps
                heappush(heap, (d + steps, nr, nc))
    return -1
```

运行：示例 1 → `12`，终点换成 `[3,2]` → `-1`；示例 3（`maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]]`，`start = [4,3]`，`destination = [0,1]`）→ `-1`。

**复杂度。** 时间 `O(mn · (m + n) · log(mn))`（每个停止点最多入堆几次，每次滚动 `O(m + n)`），空间 `O(mn)`。

**拓展优化。**
- 只问能否停在终点（LC 490 迷宫）：BFS 或 DFS 标记停止点即可，不需要堆。
- 要求输出路径字典序最小（LC 499 迷宫 III）：堆元素换成 `(距离, 路径字符串, 行, 列)`，同距离比路径。

**易错点。**
- 把每次滚动记为距离 1：这是 LC 490 的模型，示例 1 得到 `7`（滚动次数）而不是 `12`。
- 滚动途中经过终点就返回：球必须停下来，示例 2 因此是 `-1`。
- 不判断过期条目：同一个停止点可能入堆多次，旧条目弹出时若不跳过会重复松弛，效率下降，结果仍对。

**追问。**
- 输出最短路径：记录每个停止点的前驱停止点和方向，到达终点后回溯。
- 有多个终点：弹出任意一个终点即可，更靠前弹出的距离更短。

**同模式。** LC 490 迷宫、LC 499 迷宫 III、LC 743 网络延迟时间、LC 787 K 站中转内最便宜的航班、LC 1631 最小体力消耗路径。
