---
slug: tt-longest-zigzag-grid-path
---
## Q
**网格中最长的之字形递增路径**｜Hard

`m x n` 整数网格，路径从任意格出发，每步走到相邻格且值**严格更大**，水平与竖直移动必须交替（首步任意）。求最长路径的格子数。例：`[[1,2,3]]` → `2`。

## A
**一句话。** 状态是「格子 + 下一步必须走的方向类型」，按值从大到小做 DP（严格递增无环），转移时方向取反。

```python
H, V = 0, 1                 # 下一步必须是水平 / 竖直
STEPS = (((0, 1), (0, -1)), ((1, 0), (-1, 0)))

def longest_zigzag_path(grid):
    m, n = len(grid), len(grid[0])
    # dp[d][i][j]：从 (i,j) 出发、下一步方向为 d 的最长格子数
    dp = [[[1] * n for _ in range(m)] for _ in range(2)]
    cells = sorted(((grid[i][j], i, j)
                    for i in range(m) for j in range(n)),
                   reverse=True)       # 大值先算
    for val, i, j in cells:
        for d in (H, V):
            for di, dj in STEPS[d]:
                a, b = i + di, j + dj
                if (0 <= a < m and 0 <= b < n
                        and grid[a][b] > val):
                    dp[d][i][j] = max(dp[d][i][j],
                                      1 + dp[1 - d][a][b])
    return max(max(map(max, layer)) for layer in dp)
```

**复杂度。** 时间 `O(mn log mn)`，空间 `O(mn)`。

**易错点。**
- 状态不带方向：同一格子首步方向不同的路径只留一条，`[[4,2,1],[1,6,1]]` 错成 `2`，应为 `3`。
- 不管交替直接套 LC 329：`[[1,2,3]]` 得 `3`，应为 `2`。

**追问。**
- 要输出路径？：转移时记下取到最大的邻居 `nxt[d][i][j]`，从答案格沿它走到底。
- 不要求交替？：去掉方向这一维，就是 LC 329。

**同模式。** LC 329 矩阵中的最长递增路径、LC 2328 网格图中递增路径的数目、LC 1372 二叉树中的最长交错路径
