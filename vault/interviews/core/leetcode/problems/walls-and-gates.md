---
slug: walls-and-gates
---
## Q
**LC 286 Walls and Gates**｜Medium

网格里 `-1` 是墙，`0` 是门，`INF = 2^31 - 1` 是空房间。原地给每个空房间填上它到最近门的步数，到不了保持 `INF`。

## A
**一句话。** 所有门同时入队做多源 BFS，第一次到达某个房间的那一层就是它到最近门的距离。

```python
INF = 2**31 - 1

def walls_and_gates(rooms):
    m, n = len(rooms), len(rooms[0])
    q = deque((r, c) for r in range(m) for c in range(n)
              if rooms[r][c] == 0)
    while q:
        r, c = q.popleft()
        for x, y in (r+1, c), (r-1, c), (r, c+1), (r, c-1):
            if 0 <= x < m and 0 <= y < n:
                if rooms[x][y] == INF:   # 兼作 visited
                    rooms[x][y] = rooms[r][c] + 1
                    q.append((x, y))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 每个门单独跑一次 BFS 且只填 `INF`：第二个门填不进已被第一个门填过的格子，`[[0,INF,INF,INF,0]]` 得 `[0,1,2,3,0]`，应为 `[0,1,2,1,0]`。
- 用 DFS：先到的路径不一定最短，要反复比较更新，还可能 `62500` 层递归。

**追问。**
- 要知道最近的是哪扇门？：队列里同时携带源门编号，扩散时继承。
- 格子有不同代价？：BFS 失效，改 Dijkstra（`heapq`）。

**同模式。** LC 542 01 矩阵、LC 994 腐烂的橘子、LC 1162 地图分析、LC 317 离建筑物最近的距离
