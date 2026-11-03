---
slug: nearest-exit-from-entrance-in-maze
---
## Q
**LC 1926 迷宫中离入口最近的出口**｜Medium

给一个 `m x n` 的迷宫，`'.'` 是空格，`'+'` 是墙。给定入口坐标 `entrance`。每步可以上下左右走一格，不能穿墙，也不能走出迷宫。出口是位于迷宫边界的空格，入口本身不算出口。返回从入口到最近出口的最少步数，走不到返回 `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 每条边代价相同的最短路用 BFS：按步数一层层向外扩，第一次碰到的出口就是最近的。

**识别。** 「网格 + 每步代价相同 + 求最少步数」就是无权图最短路，也就是 BFS。

**推导。** DFS 找到一条路时并不知道它是否最短，必须走遍所有路径才能比较。BFS 先处理完距离 `d` 的所有格子才处理 `d + 1`，所以第一个到达的出口步数最小，可以立刻返回。

```python
from collections import deque


def nearest_exit(maze: list[list[str]], entrance: list[int]) -> int:
    rows, cols = len(maze), len(maze[0])
    start = tuple(entrance)
    seen = {start}                       # 入队时就标记，同一格不会被多次加入
    q = deque([(*start, 0)])             # (行, 列, 步数)：BFS 第一次碰到的出口一定最近
    while q:
        r, c, d = q.popleft()
        if (r, c) != start and (r in (0, rows - 1) or c in (0, cols - 1)):
            return d                     # 入口本身在边上也不算出口
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc, d + 1))
    return -1
```

**复杂度。** 时间 O(mn)，每格最多入队一次；空间 O(mn)。

**易错点。**
- 出队时才标记已访问：同一格会被邻居重复加入，队列可能膨胀很多倍。
- 把入口当成出口：入口常常就在边界上，必须排除。
- 判断出口用边界条件，不是找特殊字符。

**追问。**
- 想省一点时间：在生成邻居时就判断出口并返回 `d + 1`，比出队时判断少扩展一层。
- 多个入口：把所有入口一起放进队列，就是多源 BFS，同样的写法。
- 边的代价不同：BFS 不再成立，换成 Dijkstra（用堆按累计代价出队）。
