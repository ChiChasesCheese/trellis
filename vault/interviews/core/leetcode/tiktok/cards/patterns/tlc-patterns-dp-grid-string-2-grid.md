---
id: tlc-patterns-dp-grid-string-2-grid
node: patterns.dp-grid-string
type: qa
step: 2
---
## Q
**动态规划：网格、双串与区间｜网格模板：路径数、最小路径和、最大正方形**

写出三道网格 DP 的完整二维表版本，说明 `dp[r][c]` 的含义、基础行 / 基础列和答案格。

## A
```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]       # dp[r][c]：到 (r, c) 的路径数；基础行 / 列为 1
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]     # 上方 + 左方
    return dp[m - 1][n - 1]


def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]       # dp[r][c]：到 (r, c) 的最小路径和
    dp[0][0] = grid[0][0]
    for c in range(1, n):
        dp[0][c] = dp[0][c - 1] + grid[0][c]       # 基础行：只能从左边来
    for r in range(1, m):
        dp[r][0] = dp[r - 1][0] + grid[r][0]       # 基础列：只能从上边来
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]
    return dp[m - 1][n - 1]


def maximal_square(matrix: list[list[str]]) -> int:
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]     # dp[r][c]：以 matrix[r-1][c-1] 为右下角的最大边长
    best = 0
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            if matrix[r - 1][c - 1] == "1":
                dp[r][c] = min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1]) + 1
                best = max(best, dp[r][c])
    return best * best
```

运行：`unique_paths(3, 7)` → `28`；`(3, 2)` → `3`；`min_path_sum([[1,3,1],[1,5,1],[4,2,1]])` → `7`；`maximal_square([["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]])` → `4`。

- 每道题三件事：`dp[r][c]` 的含义、基础行 / 基础列、答案格（最大正方形取全表最大值）。
- 最小路径和若用 `0` 当哨兵行 / 列代替基础行：哨兵的 `0` 会被 `min` 选中，示例得到 `3`，正确是 `7`；哨兵要用 `inf`。
- 空间可以压到 O(n)：见 Python 工具箱「DP 降维」。
