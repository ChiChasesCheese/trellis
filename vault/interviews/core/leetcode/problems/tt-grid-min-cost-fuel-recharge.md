---
slug: tt-grid-min-cost-fuel-recharge
---
## Q
**带油量限制和补给点的网格最小代价路径**｜Hard

网格 `grid[r][c] >= 0` 是进入该格的代价，`-1` 是障碍。起点 `(0,0)` 初始油量 `K`，每步耗 `1`，到补给点油量恢复到 `K`，油量为 `0` 不能再走。求到 `(m-1,n-1)` 的最小总代价，不可达返回 `-1`。

## A
**一句话。** 状态是（位置，剩余油量），在扩展图上跑 Dijkstra，同格里油量不更多的状态被支配而丢弃。

```python
def min_cost(grid, recharge, fuel):
    m, n = len(grid), len(grid[0])
    if grid[0][0] == -1 or grid[m-1][n-1] == -1:
        return -1
    fuel = min(fuel, m * n)       # 更大的油量用不上
    best = [[-1] * n for _ in range(m)]   # 每格弹出过的最大油量
    heap = [(0, 0, 0, fuel)]      # (总代价, 行, 列, 剩余油量)
    while heap:
        cost, r, c, left = heapq.heappop(heap)
        if (r, c) == (m - 1, n - 1):
            return cost
        if left <= best[r][c]:    # 被支配
            continue
        best[r][c] = left
        if left == 0:
            continue
        for nr, nc in (r+1,c), (r-1,c), (r,c+1), (r,c-1):
            if not (0 <= nr < m and 0 <= nc < n):
                continue
            if grid[nr][nc] == -1:
                continue
            nf = fuel if (nr, nc) in recharge else left - 1
            ncost = cost + grid[nr][nc]
            heapq.heappush(heap, (ncost, nr, nc, nf))
    return -1
```

**复杂度。** 时间 `O(mn·min(K, mn)·log)`，空间同阶。

**易错点。**
- 忽略油量只比代价：示例 `K = 4` 会得 `5`，应为 `-1`（至少要走 `5` 步）。
- 补给写成「加一点」：到补给点应重置为满。
- 剪枝用 `<`：等油量的重复状态也被支配，会重复展开变慢。

**追问。**
- `K` 很大？：对 `K` 封顶 `mn` 并用支配剪枝，不开 `m·n·K` 的三维数组。
- 只问能否到达？：BFS，每格只保留最大剩余油量。

**同模式。** LC 787 K 站中转内最便宜的航班、LC 1293 网格中的最短路径、LC 871 最低加油次数、LC 1631 最小体力消耗路径
