---
id: tlc-rotting-oranges-2-code
node: b.rotting-oranges
type: qa
step: 2
---
## Q
**LC 994 腐烂的橘子**｜写出 Python 实现

`m x n` 网格 `grid`（`1 <= m, n <= 10`），`0` 为空格，`1` 为新鲜橘子，`2` 为腐烂橘子。每分钟，腐烂橘子上下左右相邻的新鲜橘子变腐烂。返回没有新鲜橘子所需的最少分钟数，做不到返回 `-1`。

## A
**思路。** 初始腐烂橘子全部入队，并统计新鲜橘子数 `fresh`；每分钟处理当前这一层，把相邻的新鲜橘子标成腐烂、入队、`fresh` 减一；队列空或没有新鲜橘子就停。

```python
from collections import deque


def oranges_rotting(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    queue = deque((i, j) for i, row in enumerate(grid) for j, v in enumerate(row) if v == 2)
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while queue and fresh:                     # 没有新鲜橘子就立刻停，不多算一分钟
        minutes += 1
        for _ in range(len(queue)):            # 恰好处理完当前这一层 = 过去一分钟
            i, j = queue.popleft()
            for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2           # 入队时就标记，避免重复入队
                    fresh -= 1
                    queue.append((ni, nj))
    return -1 if fresh else minutes
```

运行：`[[2,1,1],[1,1,0],[0,1,1]]` → `4`，`[[2,1,1],[0,1,1],[1,0,1]]` → `-1`，`[[0,2]]` → `0`，`[[0]]` → `0`，`[[1]]` → `-1`，`[[2]]` → `0`。

**复杂度。** 时间 `O(mn)`：每个格子最多入队、出队各一次；空间 `O(mn)`：队列。

**写法要点。** `deque` 的构造参数是一个生成器，直接用 `enumerate` 嵌套把所有 `2` 的坐标收集进队列；`row.count(1)` 是 `list` 的内置计数，比手写双重循环短。`for _ in range(len(queue))` 在循环开始前固定层大小，循环里新入队的属于下一层。`-1 if fresh else minutes` 同时处理“有橘子烂不了”。原地改网格节省空间，代价是破坏输入。
