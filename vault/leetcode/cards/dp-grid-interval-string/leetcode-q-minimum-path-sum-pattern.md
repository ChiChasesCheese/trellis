---
id: leetcode-q-minimum-path-sum-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787102263108
tags: [lc::64, leetcode, pattern, recall]
---
## Q
网格图最小路径和问题（如 LC 64 Minimum Path Sum）用记忆化 DFS 怎么写？边界条件如何处理？

## A
定义 dfs(i, j) 表示从 (i, j) 走到终点 (m-1, n-1) 的最小路径和。

边界：
- 终点 (m-1, n-1)：直接返回 grid[i][j]
- 越界 (i>=m or j>=n)：返回 inf（表示此路不通，不会被 min 选中）

转移：dfs(i, j) = grid[i][j] + min(dfs(i, j+1), dfs(i+1, j))

用 @cache 装饰实现记忆化，从 dfs(0, 0) 开始递归。这是网格图 DP 的通用模板：先想清楚终点和越界两种边界返回值，再写转移方程。

**Evidence**

```
@cache
def dfs(i: int, j: int) -> int:
    if i == m - 1 and j == n - 1:
        return grid[i][j]
    if i >= m or j >= n:
        return inf
    return grid[i][j] + min(dfs(i, j + 1), dfs(i + 1, j))
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F64%20-%20Minimum%20Path%20Sum)
