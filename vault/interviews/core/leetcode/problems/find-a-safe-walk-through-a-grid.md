---
slug: find-a-safe-walk-through-a-grid
---
## Q
**LC 3286 穿越网格图的安全路径**｜Medium

`m × n` 的 0/1 网格，踩到 `1`（包括起点）生命值减 1。从 `(0, 0)` 四方向走到 `(m-1, n-1)`，到达时生命值必须 `>= 1`。给初始 `health`，问能否做到。

## A
**一句话。** 等价于最小化路径上 `1` 的个数；进格的代价只有 0 或 1，用 0-1 BFS：0 边插队头，1 边排队尾，松弛成功才入队。

```python
def find_safe_walk(grid, health):
    m, n = len(grid), len(grid[0])
    cost = [[float("inf")] * n for _ in range(m)]
    cost[0][0] = grid[0][0]   # 起点也扣血
    dq = deque([(0, 0)])
    while dq:
        i, j = dq.popleft()
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= x < m and 0 <= y < n:
                w = grid[x][y]
                if cost[i][j] + w < cost[x][y]:
                    cost[x][y] = cost[i][j] + w
                    if w:
                        dq.append((x, y))
                    else:
                        dq.appendleft((x, y))  # 0 边插队头
    return cost[m - 1][n - 1] < health  # 到达时还剩 >= 1
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 起点不扣血：`cost[0][0]` 要从 `grid[0][0]` 开始。
- 最后写成 `<=`：扣完 `health` 点血就是 0，不算安全。

**追问。**
- 有回血格（负权）？：Dijkstra 和 0-1 BFS 都失效，改 Bellman-Ford，并检查负环。
- `health` 很小？：也可以 BFS 状态 `(格, 剩余血量)`，`O(mn · health)`。

**同模式。** LC 743 网络延迟时间、LC 2290 到达角落需要移除障碍物的最小数目、LC 1368 使网格图至少有一条有效路径的最小代价、LC 1631 最小体力消耗路径
