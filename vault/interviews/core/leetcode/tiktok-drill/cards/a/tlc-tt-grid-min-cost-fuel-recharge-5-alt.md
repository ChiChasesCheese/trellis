---
id: tlc-tt-grid-min-cost-fuel-recharge-5-alt
node: a.tt-grid-min-cost-fuel-recharge
type: qa
step: 5
---
## Q
**带油量限制和补给点的网格最小代价路径**｜另一种解法

不做支配剪枝，直接把剩余油量作为一个完整的维度，怎么写？什么时候这样写更合适？「把补给点之间压缩成一张小图」的想法什么时候成立？

## A
**直接三维 Dijkstra。** `dist[r][c][f]` 是到达 `(r, c)` 且剩余 `f` 单位油的最小代价，状态 `m·n·(K+1)` 个，惰性删除。

```python
import heapq
from math import inf


def min_cost_layered(grid: list[list[int]], recharge: set[tuple[int, int]], fuel: int) -> int:
    m, n = len(grid), len(grid[0])
    if grid[0][0] == -1 or grid[m - 1][n - 1] == -1:
        return -1
    fuel = min(fuel, m * n)
    dist = [[[inf] * (fuel + 1) for _ in range(n)] for _ in range(m)]     # dist[r][c][f]：到 (r, c) 且剩 f 油的最小代价
    dist[0][0][fuel] = 0
    heap = [(0, 0, 0, fuel)]
    while heap:
        cost, r, c, left = heapq.heappop(heap)
        if cost > dist[r][c][left]:
            continue
        if (r, c) == (m - 1, n - 1):
            return cost
        if left == 0:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
                nf = fuel if (nr, nc) in recharge else left - 1
                nd = cost + grid[nr][nc]
                if nd < dist[nr][nc][nf]:
                    dist[nr][nc][nf] = nd
                    heapq.heappush(heap, (nd, nr, nc, nf))
    return -1
```

结果与带剪枝的版本完全一致：`[[0,1,1,1],[9,-1,9,1],[1,1,1,1]]`、`K = 4` → `-1`，补给点 `{(0, 3)}` → `5`。时间 `O(m·n·min(K, m·n)·log)`，空间 `O(m·n·min(K, m·n))`。

**怎么选。**
- `K` 很小（几十以内）：这个版本直接、不容易写错，面试里先写它，作为对照基线。
- `K` 大或网格大：用支配剪枝的版本，空间只有 `O(m·n)`，大多数格子只保留很少的状态。
- 「压缩成补给点之间的最短距离图再跑 Dijkstra」：只在**每步代价相同**（代价等于步数）时成立，这时补给点之间的最短距离就是 BFS 距离，且距离不超过 `K` 才连边；当每格代价不同时，两个补给点之间需要「步数不超过 `K` 的最小代价」，仍是带资源约束的最短路，压缩后并不更简单。
