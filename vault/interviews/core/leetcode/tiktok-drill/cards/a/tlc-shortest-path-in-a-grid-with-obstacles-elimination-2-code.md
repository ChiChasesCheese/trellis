---
id: tlc-shortest-path-in-a-grid-with-obstacles-elimination-2-code
node: a.shortest-path-in-a-grid-with-obstacles-elimination
type: qa
step: 2
---
## Q
**LC 1293 网格中的最短路径**｜写出 Python 实现

`m x n` 的 `0/1` 网格 `grid`（`1 <= m, n <= 40`，起点终点都是 `0`），整数 `k`（`1 <= k <= m * n`）。每步上下左右移动一格，最多可以消除 `k` 个障碍。返回从左上角到右下角的最少步数，走不到返回 `-1`。

## A
**思路。** BFS，状态 `(行, 列, 剩余消除次数)`。对每个格子记录到达时见过的最大剩余次数，只有剩余次数更多的新状态才入队；`k` 足够大时直接返回曼哈顿距离。

```python
from collections import deque


def shortest_path(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    if k >= m + n - 3:                         # 最短路 m+n-2 步，至多穿过 m+n-3 堵墙：直接走
        return m + n - 2
    best_left = [[-1] * n for _ in range(m)]   # 到达每格时见过的最大剩余消除次数
    best_left[0][0] = k
    queue = deque([(0, 0, k)])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):
            i, j, left = queue.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if not (0 <= ni < m and 0 <= nj < n):
                    continue
                nleft = left - grid[ni][nj]    # 踩墙花一次，空格不花
                if nleft > best_left[ni][nj]:  # 剩余次数更多才值得再来；负数天然被挡掉
                    if (ni, nj) == (m - 1, n - 1):
                        return steps
                    best_left[ni][nj] = nleft
                    queue.append((ni, nj, nleft))
    return -1
```

运行：示例 1 → `6`，示例 2 → `-1`，`[[0]]`、`k = 1` → `0`，`[[0,0,1],[1,0,1],[0,1,0]]`、`k = 1` → `4`。

**复杂度。** 时间 `O(m * n * min(k, m + n))`：状态数至多这么多，每个状态 `4` 次转移；空间 `O(m * n)` 的最大剩余表，加队列。

**写法要点。** `left - grid[ni][nj]` 利用格子值本身就是 `0` 或 `1`，一行完成“踩墙扣一次”。`best_left` 初值 `-1`，所以 `nleft > best_left[...]` 同时挡掉了“次数不足”（`nleft < 0`）和“没有更优”两种情况，不用单独判负。层序 BFS 用 `for _ in range(len(queue))` 数层，`steps` 就是步数。终点在“更新状态”时就检查，早一层返回。
