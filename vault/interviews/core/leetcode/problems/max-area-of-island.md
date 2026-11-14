---
slug: max-area-of-island
---
## Q
**LC 695 岛屿的最大面积**｜Medium

`0/1` 矩阵里上下左右相连的 `1` 构成岛屿，求最大岛屿的面积，没有岛返回 `0`。

## A
**一句话。** 连通块 DFS：遇到 `1` 就沉岛（改成 `0`），返回自己加四个方向的面积。

**图解。** DFS 每沉一格返回 1 加四邻面积，整座岛的面积一次求出。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 140">
<rect x="20" y="16" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="34.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="48" y="16" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="34.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="76" y="16" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="16" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="16" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="44" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="62.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="48" y="44" width="28" height="28" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="62.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="76" y="44" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="44" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="44" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="48" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="76" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="72" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="72" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="20" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="48" y="100" width="28" height="28" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="76" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="104" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="132" y="100" width="28" height="28" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="176" y="34" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">数字：沉岛顺序</text>
<text x="176" y="56" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dfs 返回 1 + 四邻之和</text>
<text x="176" y="80" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三座岛面积 4、3、1</text>
<text x="176" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)" font-weight="600">答案 4</text>
</svg>

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
