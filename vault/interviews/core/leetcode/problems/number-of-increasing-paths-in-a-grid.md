---
slug: number-of-increasing-paths-in-a-grid
---
## Q
**LC 2328 网格图中递增路径的数目**｜Hard

`m x n` 整数网格。从任意格出发，每次向四个方向走到值**严格更大**的相邻格，可以停在任意位置。求所有这样的路径条数（每个格自己算一条长度为 `1` 的路径），对 `10^9 + 7` 取模。

## A
**一句话。** 记忆化 DFS：`dfs(i, j)` 是以 `(i, j)` 为起点的路径条数，等于 `1` 加上所有更大邻居的 `dfs` 之和；严格递增保证没有环。

```python
def count_paths(grid):
    M = 10 ** 9 + 7
    m, n = len(grid), len(grid[0])
    memo = {}

    def dfs(i, j):
        if (i, j) in memo:
            return memo[i, j]
        res = 1                                # 自己单独一条
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if (0 <= x < m and 0 <= y < n
                    and grid[x][y] > grid[i][j]):
                res += dfs(x, y)
        memo[i, j] = res % M
        return memo[i, j]

    return sum(dfs(i, j) for i in range(m)
               for j in range(n)) % M
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 不加记忆化：同一个格被无数条路径重复访问，指数级。
- 漏掉长度为 `1` 的路径：每个格自己算一条，`res` 从 `1` 开始。

**追问。**
- 为什么不用 `visited` 判环？：值严格递增，走过的格一定更小，不会回到自己。

**同模式。** LC 329 矩阵中的最长递增路径、LC 1372 二叉树中的最长交错路径
