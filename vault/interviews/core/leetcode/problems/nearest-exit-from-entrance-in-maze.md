---
slug: nearest-exit-from-entrance-in-maze
---
## Q
**LC 1926 迷宫中离入口最近的出口**｜Medium

迷宫里 `'.'` 是空格，`'+'` 是墙。从 `entrance` 出发每步走上下左右一格，求到最近出口（边界上的空格，入口本身不算）的最少步数，到不了返回 `-1`。

## A
**一句话。** 每步代价相同的最短路用 BFS，按步数一层层扩，第一次碰到的出口最近。

```python
def nearest_exit(maze, entrance):
    m, n = len(maze), len(maze[0])
    start = tuple(entrance)
    seen = {start}                 # 入队即标记
    q = deque([(*start, 0)])       # (行, 列, 步数)
    while q:
        r, c, d = q.popleft()
        edge = r in (0, m - 1) or c in (0, n - 1)
        if edge and (r, c) != start:
            return d               # 入口在边上也不算出口
        for x, y in (r+1, c), (r-1, c), (r, c+1), (r, c-1):
            if 0 <= x < m and 0 <= y < n:
                if maze[x][y] == "." and (x, y) not in seen:
                    seen.add((x, y))
                    q.append((x, y, d + 1))
    return -1
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 把入口当成出口：入口常在边界上，必须排除。
- 出队时才标记已访问：同一格被邻居重复入队，队列膨胀。

**追问。**
- 多个入口怎么办？：所有入口一起入队，就是多源 BFS。
- 每步代价不同？：BFS 不再成立，换 Dijkstra，用堆按累计代价出队。

**同模式。** LC 1091 二进制矩阵中的最短路径、LC 542 01 矩阵、LC 994 腐烂的橘子、LC 286 墙与门
