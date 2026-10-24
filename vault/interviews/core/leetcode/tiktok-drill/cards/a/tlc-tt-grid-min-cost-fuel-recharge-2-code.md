---
id: tlc-tt-grid-min-cost-fuel-recharge-2-code
node: a.tt-grid-min-cost-fuel-recharge
type: qa
step: 2
---
## Q
**带油量限制和补给点的网格最小代价路径**｜写出 Python 实现

写 `min_cost(grid, recharge, fuel)`：`grid` 是 `m x n`（`1 <= m, n <= 50`）的整数网格，`grid[r][c] >= 0` 是进入该格的代价（`<= 100`），`-1` 是障碍；`recharge` 是补给点坐标集合，到达后油量恢复为 `fuel`；起点 `(0, 0)` 不计代价，初始油量 `fuel`（`0 <= fuel <= 10^9`），每走一步耗 `1`，油量为 `0` 时不能再走。返回到 `(m-1, n-1)` 的最小总代价，不可达返回 `-1`。

## A
**思路。** Dijkstra，堆里放 `(总代价, 行, 列, 剩余油量)`。`best_fuel[r][c]` 记录这个格子已弹出过的最大剩余油量：新弹出的状态油量不超过它就被支配，丢弃。走向邻居时，邻居是补给点则油量重置为 `fuel`，否则减 `1`。`fuel` 对 `m * n` 取小。

```python
import heapq


def min_cost(grid: list[list[int]], recharge: set[tuple[int, int]], fuel: int) -> int:
    """grid[r][c] 是进入该格的代价，-1 表示障碍；到达 recharge 里的格子油量恢复到 fuel；每走一步耗 1 单位油。
    从 (0, 0) 到 (m-1, n-1) 的最小总代价，不可达返回 -1。"""
    m, n = len(grid), len(grid[0])
    if grid[0][0] == -1 or grid[m - 1][n - 1] == -1:
        return -1
    fuel = min(fuel, m * n)                          # 最优路径不会重复经过同一格，步数 < m*n，更大的油量没有意义
    best_fuel = [[-1] * n for _ in range(m)]         # 每格已经弹出过的最大剩余油量（支配剪枝）
    heap = [(0, 0, 0, fuel)]                         # (总代价, 行, 列, 剩余油量)
    while heap:
        cost, r, c, left = heapq.heappop(heap)
        if (r, c) == (m - 1, n - 1):
            return cost
        if left <= best_fuel[r][c]:                  # 早先以不更大的代价弹出过、油量不少于现在：现在这个被支配
            continue
        best_fuel[r][c] = left
        if left == 0:
            continue                                 # 没油了，走不动
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] != -1:
                nxt_fuel = fuel if (nr, nc) in recharge else left - 1
                heapq.heappush(heap, (cost + grid[nr][nc], nr, nc, nxt_fuel))
    return -1
```

运行：`[[0,1,1,1],[9,-1,9,1],[1,1,1,1]]`：`K = 5` → `5`，`K = 4` → `-1`，补给点 `{(0, 3)}`、`K = 4` → `5`，`K = 10**9` → `5`；`[[0,5,1],[1,5,1],[1,1,1]]`：`K = 4` → `4`，`K = 3` → `-1`；`[[0]]`、`K = 0` → `0`；`[[0,1]]`、`K = 0` → `-1`；`[[0,-1]]` → `-1`；`60 x 60` 全 `1`、`K = 118` → `118`，`K = 117` → `-1`。

**复杂度。** 每格最多保留 `min(K, m·n) + 1` 个状态（油量严格递增），时间最坏 `O(m·n·min(K, m·n)·log)`，实际远小于此；空间 `O(m·n)` 加堆。

**写法要点。**
- 堆里的元组 `(cost, r, c, left)`：`heapq` 按元素字典序比较，代价在最前面就是按代价出堆，同代价时再比行列，不需要自定义比较。
- `best_fuel` 用 `-1` 初始化，表示这个格子还没有弹出过任何状态；条件 `left <= best_fuel[r][c]` 一个比较同时处理「首次到达」和「被支配」。
- 惰性删除：不做 `decrease-key`，同一状态多次入堆，弹出时用支配条件丢弃过期项。
- `fuel = min(fuel, m * n)`：让 `K = 10^9` 的输入不会产生巨大的状态空间。
