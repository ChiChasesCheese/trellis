---
id: tlc-shortest-path-in-a-grid-with-obstacles-elimination-5-alt
node: p3.shortest-path-in-a-grid-with-obstacles-elimination
type: qa
step: 5
---
## Q
**LC 1293 网格中的最短路径**｜另一种解法

不做“最大剩余次数”的支配优化，直接用集合给完整状态 `(行, 列, 剩余)` 去重，怎么写？什么时候选它？

## A
**思路。** 状态 `(i, j, left)` 全体去重：`seen` 集合里存所有出现过的状态，BFS 逐层展开，最直观，没有“支配”的推理，不容易写错。先把 `k` 限制到 `m + n - 3`，否则状态太多。

```python
from collections import deque


def shortest_path_states(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    k = min(k, m + n - 3)                      # 多于 m+n-3 次消除用不上
    start = (0, 0, k)
    seen = {start}                             # 状态 = (行, 列, 剩余消除次数)
    queue = deque([(start, 0)])
    while queue:
        (i, j, left), steps = queue.popleft()
        if (i, j) == (m - 1, n - 1):
            return steps
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < m and 0 <= nj < n:
                state = (ni, nj, left - grid[ni][nj])
                if state[2] >= 0 and state not in seen:
                    seen.add(state)
                    queue.append((state, steps + 1))
    return -1
```

输出与主解一致：示例 1 → `6`，示例 2 → `-1`，`[[0]]` → `0`，`[[0,0,1],[1,0,1],[0,1,0]]`、`k = 1` → `4`；`40 x 40` 随机盘面（约 `35%` 的墙）、`k = 30` 和 `k = 77` 都在 `50 ms` 内完成。

**取舍。**
- 集合版：写法只有一个“去重”概念，面试里先写它最稳；状态数最多 `m * n * (min(k, m + n - 3) + 1)`，`40 x 40`、`k = 77` 约 `12.5` 万个，Python 里没有问题。
- 最大剩余版（主解）：同一格里被支配的状态不入队，状态数更少、常数更小，内存也只有一个 `m x n` 的整数表；代价是需要说清“支配”为什么成立。
- 两者复杂度同阶 `O(m * n * min(k, m + n))`。若被问“怎么再快”，先说主解的支配剪枝，再提 A*。
