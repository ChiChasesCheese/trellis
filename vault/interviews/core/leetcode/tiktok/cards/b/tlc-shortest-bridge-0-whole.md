---
id: tlc-shortest-bridge-0-whole
node: b.shortest-bridge
type: qa
---
## Q
**LC 934 最短的桥**｜Medium · TikTok·字节 高频

给 `n x n` 的二元矩阵 `grid`，`1` 表示陆地，`0` 表示水域。岛是由四面相连的 `1` 形成的一个最大组；`grid` 中**恰好存在两座岛**。可以将任意数量的 `0` 变为 `1`，使两座岛连接成一座岛，返回必须翻转的 `0` 的最小数目。`n == grid.length == grid[i].length`，`2 <= n <= 100`，`grid[i][j]` 为 `0` 或 `1`，`grid` 中恰有两个岛。例：`[[0,1],[1,0]]` → `1`；`[[0,1,0],[0,0,0],[0,0,1]]` → `2`；`[[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两步：先用 DFS 找出第一座岛的全部格子；再以这整座岛为起点做**多源 BFS**，每扩一层就是多翻一格水，第一次碰到另一座岛时，已扩的层数就是答案。`O(n^2)`。

**识别。** 「两座岛之间的最少填水格数」= 两个格子集合之间的最短距离，网格上的最短路用 BFS；起点不是一个点而是一整座岛，所以是多源 BFS（multi-source BFS）。`n <= 100`，一万个格子，BFS 轻松。

**推导。** 暴力：枚举两座岛的所有格子对，取曼哈顿距离的最小值再减 `1`，`O(m1 × m2)`，最坏约 `n^4/4` = 2.5×10^7，勉强 → 浪费：只需要最近的一对，不需要所有对 → 把第一座岛的所有格子同时放进队列作为第 0 层，按层向外扩（扩出的每一层都是水，翻一格），先碰到第二座岛的那一层决定最短距离。

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

运行：`[[0,1],[1,0]]` → `1`，`[[0,1,0],[0,0,0],[0,0,1]]` → `2`，`[[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]` → `1`，`[[0,0,1],[1,0,1],[0,0,0]]` → `1`；`100×100` 的对角两角各一块陆地 → `197`。

**复杂度。** 时间 `O(n^2)`：每个格子最多入队一次；空间 `O(n^2)`：`seen` 与队列。

**易错点。**
- 起点必须是整座岛，而不是一个格子：只从第一块陆地单点 BFS 并把本岛的格子也当作可走路径，会多算。例 3 得到 `3`，正确是 `1`；`[[0,0,1],[1,0,1],[0,0,0]]` 得到 `2`，正确是 `1`。
- 层数在每层**扩完**后才加一：第一层扩出的水格是第 `1` 个要翻的格子，碰到岛 B 时返回的 `flips` 恰好是已翻的格子数，不要再 `-1`。
- 标记 `seen` 要包含整座岛 A，否则 BFS 会回头把 A 的格子当成「新碰到的陆地」，立刻返回 `0`。

**追问。**
- 要输出具体填哪些格子：给每个格子记前驱，碰到 B 时沿前驱回溯。
- 水格有代价（比如某些格子翻转更贵）：BFS 换成 Dijkstra，或在代价只有 `0/1` 时用 0-1 BFS（双端队列）。
- 有 `k` 座岛要全部连通：这是在岛之间求最小生成树（或更难的 Steiner 树），先对每对岛求最短距离。

**同模式。** LC 1091 二进制矩阵中的最短路径、LC 542 01 矩阵（多源 BFS）、LC 994 腐烂的橘子、LC 827 最大人工岛。
