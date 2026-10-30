---
id: tlc-making-a-large-island-5-alt
node: p2.making-a-large-island
type: qa
step: 5
---
## Q
**LC 827 最大人工岛**｜另一种解法

用并查集（Union-Find）怎么做这个问题？它和「DFS 标号」相比各有什么优劣？

## A
**思路。** 格子 `(i, j)` 编号 `i * n + j`。扫描网格合并相邻的 `1`，集合大小存在根上；再枚举每个 `0`，对四邻里 `1` 的**根**去重，面积相加再加 `1`。

```python
def largest_island_dsu(grid: list[list[int]]) -> int:
    n = len(grid)
    parent = list(range(n * n))
    size = [1] * (n * n)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]          # 路径减半
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra                        # 小的挂到大的下面
            size[ra] += size[rb]

    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                if i + 1 < n and grid[i + 1][j]:
                    union(i * n + j, (i + 1) * n + j)
                if j + 1 < n and grid[i][j + 1]:
                    union(i * n + j, i * n + j + 1)
    best = max((size[find(k)] for k in range(n * n) if grid[k // n][k % n]), default=0)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                around = ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1))
                roots = {find(a * n + b) for a, b in around if 0 <= a < n and 0 <= b < n and grid[a][b]}
                best = max(best, 1 + sum(size[r] for r in roots))
    return best
```

运行：`[[1,0],[0,1]]` → `3`，`[[1,1],[1,0]]` → `4`，`[[1,1],[1,1]]` → `4`，`[[0]]` → `1`。

**复杂度。** 时间近似 `O(n^2)`（反阿克曼函数视为常数）；空间 `O(n^2)`。

**何时选哪个。**
- DFS/BFS 标号：思路最直白，每座岛一个编号，调试时能直接看 `label`；Python 里要用显式栈。
- 并查集：不需要栈，可以**在线**加点（逐格变成 `1` 时增量合并），也自然支持「合并两座岛」的语义；代价是常数略大。
