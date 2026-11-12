---
slug: the-maze-iii
---
## Q
**LC 499 迷宫 III**｜Hard

球在 `0/1` 迷宫里朝一个方向滚到撞墙才停，滚过洞口会掉进去。求从 `ball` 进 `hole` 的最短路线（方向串 `u/d/l/r`），距离相同取字典序最小，进不了返回 `"impossible"`。

## A
**一句话。** 停下的位置为节点、一次滚动为带权边，跑 Dijkstra，堆键用 `(距离, 路径)` 自动先比距离再比字典序，滚过洞口就截停。

```python
def find_shortest_way(maze, ball, hole):
    m, n = len(maze), len(maze[0])
    dirs = (("d", 1, 0), ("l", 0, -1),
            ("r", 0, 1), ("u", -1, 0))
    hole = tuple(hole)
    heap = [(0, "", *ball)]       # (距离, 路径, 行, 列)
    done = set()
    while heap:
        d, path, r, c = heappop(heap)
        if (r, c) == hole:
            return path
        if (r, c) in done:        # 弹出时才定型
            continue
        done.add((r, c))
        for ch, dr, dc in dirs:
            x, y, s = r, c, 0
            while (0 <= x + dr < m and 0 <= y + dc < n
                   and maze[x + dr][y + dc] == 0):
                x, y, s = x + dr, y + dc, s + 1
                if (x, y) == hole:     # 滚过洞口就掉进去
                    break
            if s and (x, y) not in done:
                heappush(heap, (d + s, path + ch, x, y))
    return "impossible"
```

**复杂度。** 时间 `O(mn(m+n) log mn)`，空间 `O(mn)`，另乘路径长度。

**易错点。**
- 滚动时不检查洞、只在停点判断：球直接滚过洞，`[[0,0,0]]`、`ball=[0,0]`、`hole=[0,1]` 返回 `"impossible"`，应为 `"r"`。
- 堆键只放距离：平局按入堆顺序，样例 1 返回 `"ul"`，应为 `"lul"`。
- 入堆时就标记已访问：后到的同距离、字典序更小的路径被丢掉，要在弹出时定型。

**追问。**
- 只要最短距离、球必须停在终点（LC 505）？：键里去掉路径，不截停，用 `dist` 松弛。
- 只问能否停在终点（LC 490）？：权不重要，BFS / DFS 遍历停点即可。

**同模式。** LC 490 迷宫、LC 505 迷宫 II、LC 743 网络延迟时间、LC 1631 最小体力消耗路径
