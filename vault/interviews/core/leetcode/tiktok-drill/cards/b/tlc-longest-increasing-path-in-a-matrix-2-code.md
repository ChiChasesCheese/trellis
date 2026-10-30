---
id: tlc-longest-increasing-path-in-a-matrix-2-code
node: b.longest-increasing-path-in-a-matrix
type: qa
step: 2
---
## Q
**LC 329 矩阵中的最长递增路径**｜写出 Python 实现

整数矩阵 `matrix`（`1 <= m, n <= 200`，值 `0..2^31 - 1`），每步可上下左右移动，路径上的值严格递增。写 `longest_increasing_path(matrix)`，返回最长递增路径的格子数。

## A
**思路。** `dfs(i, j)` 表示从 `(i, j)` 出发的最长递增路径格子数：`1 + max(dfs(严格更大的邻居))`，没有更大邻居时是 `1`。`memo[i][j]` 缓存算过的值（`0` 表示还没算），对所有格子取最大值。

```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]         # memo[i][j]：从 (i, j) 出发的最长递增路径点数，0 表示还没算

    def dfs(i: int, j: int) -> int:
        if memo[i][j]:
            return memo[i][j]
        best = 1                               # 至少有自己
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                best = max(best, 1 + dfs(x, y))   # 邻居严格更大才能走，所以不会走回头路
        memo[i][j] = best
        return best

    return max(dfs(i, j) for i in range(m) for j in range(n))
```

运行：`[[9,9,4],[6,6,8],[2,1,1]]` → `4`，`[[3,4,5],[3,2,6],[2,2,1]]` → `4`，`[[1]]` → `1`，`[[5,5],[5,5]]` → `1`；`200 x 200` 蛇形严格递增矩阵 → `40000`；`200 x 200` 的梳状矩阵（最长路径 `20101` 格）在默认递归上限下抛 `RecursionError`，`sys.setrecursionlimit(100000)` 后 → `20101`。

**复杂度。** 时间 `O(mn)`：每格只计算一次，每次看 `4` 个邻居；空间 `O(mn)`：`memo` 表加递归栈（最深等于最长路径的格子数，梳状矩阵会触到默认递归上限）。

**写法要点。** `memo` 用二维表，`0` 当作「还没算」（答案至少是 `1`，不会冲突）；方向直接写成四元组 `((i + 1, j), …)`，`0 <= x < m` 是链式比较；比较写 `>`，严格大于保证 DAG，不需要 `visited`；`max(dfs(i, j) for …)` 用生成器求全局最大。`functools.cache` 能把 `dfs` 缓存写成一行装饰器，但它的包装器是 C 实现，深递归时即使调高递归上限也会在 C 栈上限处报 `RecursionError`；路径可能很长，所以这里手写 `memo`。
