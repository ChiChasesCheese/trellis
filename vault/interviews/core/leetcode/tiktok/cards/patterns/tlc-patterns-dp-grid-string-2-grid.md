---
id: tlc-patterns-dp-grid-string-2-grid
node: patterns.dp-grid-string
type: qa
step: 2
---
## Q
**动态规划：网格、双串与区间｜网格模板：路径数、最小路径和、最大正方形**

写出三道网格 DP 的一维滚动版本，说明 `dp[c]` 在更新前后分别代表什么。

## A
```python
def unique_paths(m: int, n: int) -> int:
    dp = [1] * n                           # 第一行全是 1
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]             # dp[c]（上方，旧值）+ dp[c-1]（左方，新值）
    return dp[-1]

def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [0] * n
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0:
                dp[c] = grid[0][0]
            elif r == 0:
                dp[c] = dp[c - 1] + grid[r][c]
            elif c == 0:
                dp[c] += grid[r][c]
            else:
                dp[c] = min(dp[c], dp[c - 1]) + grid[r][c]
    return dp[-1]

def maximal_square(matrix: list[list[str]]) -> int:
    dp = [0] * (len(matrix[0]) + 1)        # dp[c+1]：以当前行第 c 列为右下角的最大正方形边长
    best = 0
    for row in matrix:
        diag = 0                           # 左上角 dp[r-1][c-1]
        for c, ch in enumerate(row):
            up = dp[c + 1]
            dp[c + 1] = min(up, dp[c], diag) + 1 if ch == "1" else 0
            best = max(best, dp[c + 1])
            diag = up
    return best * best
```

运行：`unique_paths(3, 7)` → `28`；`(3, 2)` → `3`；`min_path_sum([[1,3,1],[1,5,1],[4,2,1]])` → `7`；`maximal_square([["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]])` → `4`。

- 更新前，`dp[c]` 是**上一行**同一列的值（上方）；更新后是本行的值；`dp[c - 1]` 已经更新过，是左方。
- 最大正方形：右下角为 `(r, c)` 的正方形边长 = 上、左、左上三个方向最小边长 + 1；任一方向为 0 就是 0。
- 路径数有组合数公式 `C(m+n-2, m-1)`，面试里可作为验证。
