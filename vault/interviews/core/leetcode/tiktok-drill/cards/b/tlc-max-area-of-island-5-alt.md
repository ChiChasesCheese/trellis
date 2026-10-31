---
id: tlc-max-area-of-island-5-alt
node: b.max-area-of-island
type: qa
step: 5
---
## Q
**LC 695 岛屿的最大面积**｜另一种解法

递归 DFS 在蛇形岛（`1275` 格）或 `50 x 50` 全陆地的网格上会超过 Python 默认递归上限，不递归怎么写 LC 695（`1 <= m, n <= 50`）？为什么必须在入栈时就沉岛？什么时候该选它而不是递归版？

## A
**显式栈 DFS。** 外层双层循环找到没处理过的 `1`，把它压栈并立刻改成 `0`；循环里弹出一格、面积加 `1`，把四个方向上仍是 `1` 的邻居改成 `0` 再压栈。栈空时这座岛搜完，取所有岛的最大面积。`O(mn)` 时间，`O(mn)` 空间，不受递归深度限制。

```python
from itertools import product


def max_area_stack(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    best = 0
    for si, sj in product(range(m), range(n)):
        if grid[si][sj] != 1:
            continue
        grid[si][sj] = 0               # 入栈时就沉岛，保证每格只入栈一次
        stack = [(si, sj)]
        area = 0
        while stack:
            i, j = stack.pop()
            area += 1
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 0
                    stack.append((ni, nj))
        best = max(best, area)
    return best
```

**为什么入栈时就沉岛。** 出栈才沉岛，同一格会被好几个已展开的邻居各压一次栈，面积被重复累加：`[[1,1],[1,1]]` 会数成 `5`，正确是 `4`。

**什么时候选它。** 岛可能很长（蛇形、整张图全是陆地）、又不想调 `sys.setrecursionlimit` 时选显式栈；网格小、递归深度有把握时，递归版更短、更直观。把 `pop()` 换成 `popleft()`（`collections.deque`）就是 BFS，面积相同。
