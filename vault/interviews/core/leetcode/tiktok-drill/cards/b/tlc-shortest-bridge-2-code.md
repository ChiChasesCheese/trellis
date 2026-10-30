---
id: tlc-shortest-bridge-2-code
node: b.shortest-bridge
type: qa
step: 2
---
## Q
**LC 934 最短的桥**｜写出 Python 实现

`n x n` 的 0/1 矩阵 `grid`（`2 <= n <= 100`），恰有两座岛（四连通的 `1`），可把任意个 `0` 变成 `1`，返回连通两座岛所需翻转的 `0` 的最少个数。

## A
**思路。** 先找到任意一块陆地，用显式栈 DFS 圈出它所在的整座岛，记入 `seen`。再把这座岛的所有格子当作第 0 层做 BFS：每扩一层 `flips += 1`，扩出的水格记入 `seen`；扩的过程中碰到不在 `seen` 里的陆地，就是第二座岛，返回当前的 `flips`。

```python
from collections.abc import Iterator

def shortest_bridge(grid: list[list[int]]) -> int:
    n = len(grid)

    def neighbors(i: int, j: int) -> Iterator[tuple[int, int]]:
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    start = next((i, j) for i in range(n) for j in range(n) if grid[i][j])   # 第一块陆地
    seen = {start}
    stack = [start]
    while stack:                                   # 第一步：DFS 圈出第一座岛
        x, y = stack.pop()
        for a, b in neighbors(x, y):
            if grid[a][b] and (a, b) not in seen:
                seen.add((a, b))
                stack.append((a, b))
    frontier = list(seen)                          # 第二步：整座岛作为起点的多源 BFS，一层 = 翻一格水
    flips = 0
    while frontier:
        nxt: list[tuple[int, int]] = []
        for x, y in frontier:
            for a, b in neighbors(x, y):
                if (a, b) not in seen:
                    if grid[a][b]:                 # 碰到第二座岛：已经翻的层数就是答案
                        return flips
                    seen.add((a, b))
                    nxt.append((a, b))
        frontier = nxt
        flips += 1
    return -1
```

运行：`[[0,1],[1,0]]` → `1`，`[[0,1,0],[0,0,0],[0,0,1]]` → `2`，`[[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]` → `1`，`[[0,0,1],[1,0,1],[0,0,0]]` → `1`。

**复杂度。** 时间 `O(n^2)`：每个格子至多访问一次；空间 `O(n^2)`：`seen` 集合与当前层。

**写法要点。** `next(生成器表达式)` 一步找到第一块陆地，不用双重 `for` 加 `break`；`seen` 用 `set` 存 `(行, 列)` 元组，既当「已访问」又当「第一座岛」；按层 BFS 用两个列表 `frontier` / `nxt` 交替，比 `deque` 加记层数更直观，层数变量 `flips` 与答案一一对应；`neighbors` 生成器封装了方向与边界，两个阶段共用。
