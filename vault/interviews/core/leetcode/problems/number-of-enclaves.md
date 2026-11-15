---
slug: number-of-enclaves
---
## Q
**LC 1020 飞地的数量**｜Medium

网格里 `0` 是海、`1` 是陆。一次移动是走到上下左右相邻的陆地。求有多少陆地格子无法走出网格边界。

## A
**一句话。** 反向思考：从边界上的陆地出发 DFS，把能走出去的陆地全部淹掉，剩下的陆地数就是答案。

```python
def num_enclaves(grid):
    m, n = len(grid), len(grid[0])
    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n):
            return
        if not grid[i][j]:
            return
        grid[i][j] = 0              # 淹掉，同时当作已访问
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    for i in range(m):
        for j in range(n):
            if i in (0, m - 1) or j in (0, n - 1):
                dfs(i, j)           # 只从边界出发
    return sum(map(sum, grid))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`（递归栈最坏）。

**易错点。**
- 对每个内部陆地各搜一次再判断能否出界：重复且易错，从边界出发一次扫完更直接。
- 只扫第一行和第一列：边界是四条边，用 `i in (0, m-1) or j in (0, n-1)` 一起覆盖。
- 返回岛的个数：题目问的是陆地格子数，不是岛数。

**追问。**
- 大网格递归会爆栈怎么办？：改用 BFS 队列或显式栈，从所有边界陆地同时入队。
- 想同时知道每个飞地岛的大小？：保留不淹的版本，对每块没被边界标记的陆地再 DFS 计面积。

**同模式。** LC 130 被围绕的区域、LC 1254 统计封闭岛屿的数目、LC 200 岛屿数量、LC 695 岛屿的最大面积
