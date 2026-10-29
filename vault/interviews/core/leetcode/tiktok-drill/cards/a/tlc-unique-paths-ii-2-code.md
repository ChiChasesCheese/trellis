---
id: tlc-unique-paths-ii-2-code
node: a.unique-paths-ii
type: qa
step: 2
---
## Q
**LC 63 不同路径 II**｜写出 Python 实现

`m x n` 网格（`1 <= m, n <= 100`），`1` 是障碍、`0` 是空格；从左上角只向下或向右走到右下角，不经过障碍，有多少条不同路径？答案不超过 `2 * 10^9`。要求 `O(mn)`。

## A
**思路。** `dp[i][j]` 是走到第 `i` 行第 `j` 列（从 1 数起）的路径数，等于上方与左方之和；障碍格保持 `0`。第 0 行、第 0 列是哨兵，`dp[0][1] = 1` 让起点得到 `1`，边界不用特判。

```python
def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]   # dp[i][j]：走到第 i 行第 j 列（行列都从 1 数起）的路径数
    dp[0][1] = 1                                  # 哨兵：让起点 dp[1][1] = dp[0][1] + dp[1][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if obstacle_grid[i - 1][j - 1] == 0:  # 障碍格保持 0
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m][n]
```

运行：`[[0,0,0],[0,1,0],[0,0,0]]` → `2`，`[[0,1],[0,0]]` → `1`，`[[1]]` → `0`，`[[0]]` → `1`，`[[0,0],[0,1]]` → `0`。

**复杂度。** 时间 `O(mn)`：每格一次加法；空间 `O(mn)`：`(m+1) x (n+1)` 的表。

**写法要点。** `[[0] * (n + 1) for _ in range(m + 1)]` 每行是独立列表；写成 `[[0] * (n + 1)] * (m + 1)` 会让所有行共享同一个列表，改一格全列都变。哨兵行列把「第一行、第一列、起点」三种特判合成一个公式，下标统一偏移 1，读网格时用 `i - 1, j - 1`。
