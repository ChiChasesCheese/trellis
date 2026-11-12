---
slug: max-area-of-island
---
## Q
**LC 695 岛屿的最大面积**｜Medium

`0/1` 矩阵里上下左右相连的 `1` 构成岛屿，求最大岛屿的面积，没有岛返回 `0`。

## A
**一句话。** 连通块 DFS：遇到 `1` 就沉岛（改成 `0`），返回自己加四个方向的面积。

```python
def max_area_of_island(grid):
    m, n = len(grid), len(grid[0])

    def dfs(i, j):
        if not (0 <= i < m and 0 <= j < n):
            return 0
        if grid[i][j] != 1:
            return 0
        grid[i][j] = 0       # 先沉岛再扩散，每格只数一次
        return (1 + dfs(i+1, j) + dfs(i-1, j)
                + dfs(i, j+1) + dfs(i, j-1))

    return max(dfs(i, j)
               for i in range(m) for j in range(n))
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 邻居写成八个方向：对角相邻不算同一岛，会把面积 `6` 算成 `11`。
- 先递归邻居后沉岛：`[[1,1]]` 两格互相递归，抛 `RecursionError`。
- 递归深度：蛇形大岛可达上千层，超过 CPython 默认上限。

**追问。**
- 递归太深怎么办？：改显式栈，入栈时就置 `0`，面积在出栈时累计。
- 不许改输入？：先 `[r[:] for r in grid]` 深拷贝，或另开 `visited`。

**同模式。** LC 200 岛屿数量、LC 463 岛屿的周长、LC 827 最大人工岛、LC 130 被围绕的区域
