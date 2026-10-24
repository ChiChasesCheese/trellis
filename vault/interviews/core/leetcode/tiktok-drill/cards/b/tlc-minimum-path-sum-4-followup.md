---
id: tlc-minimum-path-sum-4-followup
node: b.minimum-path-sum
type: qa
step: 4
---
## Q
**LC 64 最小路径和**｜追问

面试官接着问：（1）要输出具体路径怎么办？（2）如果允许上下左右四个方向走？（3）有障碍格呢？

## A
1. **输出路径。** 一维滚动会丢掉历史，要还原路径就保留二维 `dp`（空间 `O(mn)`），从右下角往回走：当前格的 `dp` 减去 `grid`，看它等于上方还是左方的 `dp`，就知道从哪来；收集下标后反转。
2. **四个方向。** 格子之间可能互相到达，不再有从左上到右下的固定顺序，DP 失效；改用 Dijkstra（边权非负，点权可以挪到入边上）：

```python
from heapq import heappop, heappush
from math import inf


def min_path_sum_4dir(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dist = [[inf] * n for _ in range(m)]
    dist[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        d, i, j = heappop(heap)
        if d > dist[i][j]:                       # 过期条目（懒删除）
            continue
        if (i, j) == (m - 1, n - 1):
            return d
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < m and 0 <= nj < n and d + grid[ni][nj] < dist[ni][nj]:
                dist[ni][nj] = d + grid[ni][nj]
                heappush(heap, (dist[ni][nj], ni, nj))
    return dist[m - 1][n - 1]
```

时间 `O(mn log mn)`。
3. **障碍格。** 把障碍格的 `dp` 设为 `inf`（求最小和），或设为 `0` 条路（计数问题 LC 63）。

**Python 提醒**：`heapq` 没有「减小键」操作，更新距离时直接再压入新条目，弹出时用 `if d > dist[i][j]: continue` 丢弃过期条目；元组 `(距离, i, j)` 的比较会在距离相同时继续比较下标，不需要额外的计数器。
