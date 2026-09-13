---
id: leetcode-q-minimum-path-cost-in-a-grid-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787354596331
tags: [lc::2304, leetcode, pattern, recall]
---
## Q
网格图 DP：每步移动到下一行且移动代价与「起点格子的值」相关时（如 LC 2304 Minimum Path Cost in a Grid），状态转移该怎么设计？

## A
定义 dfs(x, y) 表示从格子 (x, y) 走到最后一行的最小总代价。边界：x == m-1 时直接返回 grid[x][y]。转移：枚举下一行所有列 ny，代价为 dfs(x+1, ny) + moveCost[grid[x][y]][ny] + grid[x][y]，取最小值。移动代价矩阵按「当前格子的值」而非「当前格子坐标」索引，是本题区别于普通网格 DP 的关键点。最终答案是枚举第一行所有起点 dfs(0, y) 的最小值，用 @cache 做记忆化。

**Evidence**

dfs(x, y) 中 `for ny, dist in enumerate(moveCost[val])` 按 val=grid[x][y] 索引 moveCost，且 `return min(dfs(0, x) for x in range(n))` 枚举起点，与 Unique Paths 系列中直接按坐标转移的写法形成对比。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2304%20-%20Minimum%20Path%20Cost%20in%20a%20Grid)
