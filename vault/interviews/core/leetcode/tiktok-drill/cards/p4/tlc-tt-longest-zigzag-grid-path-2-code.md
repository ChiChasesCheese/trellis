---
id: tlc-tt-longest-zigzag-grid-path-2-code
node: p4.tt-longest-zigzag-grid-path
type: qa
step: 2
---
## Q
**网格中最长的之字形递增路径**｜写出 Python 实现

`m x n` 网格（`m, n <= 200`，值在 `[0, 2^31 - 1]`），路径每步走到相邻格子，值严格增大，水平和竖直移动交替（第一步任意）。返回最长路径的格子数，不能用递归。

## A
**思路。** `dp[d][i][j]` 是从 `(i, j)` 出发、下一步必须走方向类型 `d` 时的最长格子数。所有转移都指向值更大的邻居，所以按值从大到小处理格子，处理到某格时它更大的邻居都已经算好；答案是整张表的最大值。

```python
H, V = 0, 1                                               # 下一步必须是水平 / 竖直
STEPS = (((0, 1), (0, -1)), ((1, 0), (-1, 0)))            # STEPS[H]、STEPS[V]


def longest_zigzag_path(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    # dp[d][i][j]：从 (i, j) 出发、下一步方向类型必须是 d 时，最长路径的格子数
    dp = [[[1] * n for _ in range(m)] for _ in range(2)]
    # 值从大到小处理：严格递增保证邻居（更大的值）已经算好
    cells = sorted(((grid[i][j], i, j) for i in range(m) for j in range(n)), reverse=True)
    for val, i, j in cells:
        for d in (H, V):
            for di, dj in STEPS[d]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > val:
                    dp[d][i][j] = max(dp[d][i][j], 1 + dp[1 - d][ni][nj])   # 走完这步，下一步换方向
    return max(max(map(max, layer)) for layer in dp)
```

运行：`[[1,2],[4,3]]` → `4`；`[[1,2,3]]` → `2`；`[[5]]` → `1`；`[[1,2],[3,4]]` → `3`；`[[4,2,1],[1,6,1]]` → `3`。

**复杂度。** 时间 `O(mn log(mn))`：排序为主，填表每格 2 方向 × 2 邻居；空间 `O(mn)`（`dp` 两层加排序列表）。

**写法要点。** 方向按类型分组存成 `STEPS[d]`，`1 - d` 一步切换类型，不用写四个 `if`；`[[1] * n for _ in range(m)]` 每行独立，`[[1] * n] * m` 会让所有行共享同一个列表；元组 `(值, i, j)` 直接排序，`reverse=True` 得到从大到小；`max(map(max, layer))` 求二维最大值。
