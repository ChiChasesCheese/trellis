---
slug: minimum-path-sum
---
## Q
**LC 64 最小路径和**｜Medium

非负整数网格 `grid`，每次只能向下或向右，求左上角到右下角路径数字和的最小值。

## A
**一句话。** 网格 DP：`dp[i][j] = grid[i][j] + min(上, 左)`，第一行第一列只有一个来源。

```python
def min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]   # 走到 (i,j) 的最小和
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]   # 第一行只能从左来
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]   # 第一列只能从上来
    for i in range(1, m):
        for j in range(1, n):
            best = min(dp[i - 1][j], dp[i][j - 1])
            dp[i][j] = best + grid[i][j]
    return dp[m - 1][n - 1]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 边界没初始化：留着的 `0` 被当成免费来源，`[[1],[2],[3]]` 得 `0`，应为 `6`。
- 外圈哨兵用 `0` 统一转移：路径能凭空从边外进来，哨兵要用 `inf`（仅起点上方为 `0`）。
- 每步贪心走较小的邻格：`[[1,3,1],[1,5,1],[4,2,1]]` 得 `9`，应为 `7`。

**追问。**
- 要输出路径？：从右下角回溯，看 `dp - grid` 等于上方还是左方，收集后反转。
- 允许四个方向？：没有拓扑顺序了，改用 Dijkstra，`O(mn log mn)`。

**同模式。** LC 62 不同路径、LC 63 不同路径 II、LC 120 三角形最小路径和、LC 174 地下城游戏
