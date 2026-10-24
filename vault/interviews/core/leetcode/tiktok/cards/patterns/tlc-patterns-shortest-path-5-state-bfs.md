---
id: tlc-patterns-shortest-path-5-state-bfs
node: patterns.shortest-path
type: qa
step: 5
---
## Q
**最短路（Shortest Path）｜带状态的 BFS：网格中最多消除 k 个障碍（LC 1293）**

为什么 `seen` 里要记录"剩余可消除次数"？怎样给 BFS 加一个剪枝？

## A
同一个格子，带着不同的剩余次数到达，后续可走的路不同。状态必须是 `(行, 列, 剩余次数)`，每步代价都是 1，所以用 BFS。

```python
from collections import deque
def shortest_path(grid: list[list[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    if k >= m + n - 2:
        return m + n - 2                   # 够把任何一条最短路径上的障碍全消掉
    q = deque([(0, 0, k)])                 # 状态 = (行, 列, 剩余可消除数)
    seen = {(0, 0, k)}
    steps = 0
    while q:
        for _ in range(len(q)):
            r, c, left = q.popleft()
            if (r, c) == (m - 1, n - 1):
                return steps
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = r + dr, c + dc
                if 0 <= a < m and 0 <= b < n:
                    nl = left - grid[a][b]  # 进入障碍格消耗 1 次
                    if nl >= 0 and (a, b, nl) not in seen:
                        seen.add((a, b, nl))
                        q.append((a, b, nl))
        steps += 1
    return -1
```

运行：`([[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], 1)` → `6`；`([[0,1,1],[1,1,1],[1,0,0]], 1)` → `-1`；`([[0]], 1)` → `0`。状态数 `m * n * (k + 1)`，时间、空间同阶。

**反例：`seen` 只记位置。** 网格 `[[0,0],[1,0],[1,1],[0,0]]`，`k = 1`：
- 只用 `(行, 列)` 去重，第一次到达某格子时剩余次数可能较少（先走了障碍），之后带着更多剩余次数的到达被丢弃，返回 `-1`。
- 正确答案是 `4`（`(0,0)→(0,1)→(1,1)→(2,1)→(3,1)`，消除 `(2,1)`）。

- 剪枝 `k >= m + n - 2`：曼哈顿距离的最短路径最多经过 `m + n - 2` 个格子，次数够就直接返回。
- 0-1 BFS：如果"消除障碍"当成代价 1、"普通步"当成 0，就变成另一类问题（最小障碍数），用双端队列 `appendleft` 处理 0 权边。
