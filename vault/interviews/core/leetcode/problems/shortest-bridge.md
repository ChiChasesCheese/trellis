---
slug: shortest-bridge
---
## Q
**LC 934 最短的桥**｜Medium

`n×n` 的 0/1 矩阵里恰有两座岛，求连通两座岛最少需要翻转的 `0` 的个数。

## A
**一句话。** DFS 圈出第一座岛，再以整座岛为起点做多源 BFS，碰到第二座岛时的层数就是答案。

```python
def shortest_bridge(grid):
    n = len(grid)

    def nbrs(i, j):
        for a, b in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= a < n and 0 <= b < n:
                yield a, b

    seen = set()

    def dfs(x, y):                 # 圈出第一座岛
        seen.add((x, y))
        for a, b in nbrs(x, y):
            if grid[a][b] and (a, b) not in seen:
                dfs(a, b)

    start = next((i, j) for i in range(n) for j in range(n)
                 if grid[i][j])
    dfs(*start)
    frontier = list(seen)          # 整座岛作为 BFS 起点
    flips = 0
    while frontier:
        nxt = []
        for x, y in frontier:
            for a, b in nbrs(x, y):
                if (a, b) not in seen:
                    if grid[a][b]:     # 碰到第二座岛
                        return flips
                    seen.add((a, b))
                    nxt.append((a, b))
        frontier = nxt
        flips += 1
    return -1
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 只从一个格子 BFS：会多算，`[[0,0,1],[1,0,1],[0,0,0]]` 得 `2`，应为 `1`。
- `seen` 没包含整座岛 A：BFS 回头碰到 A 的格子，立刻返回 `0`。
- 蛇形岛上 `dfs` 能深到约 `10^4` 层，会 `RecursionError`，要调大递归上限或改显式栈。

**追问。**
- 要输出具体填哪些格子？：给每格记前驱，碰到 B 时沿前驱回溯。
- 翻转代价不同？：BFS 换 Dijkstra，代价只有 `0/1` 时用 0-1 BFS。

**同模式。** LC 1091 二进制矩阵中的最短路径、LC 542 01 矩阵、LC 994 腐烂的橘子、LC 827 最大人工岛
