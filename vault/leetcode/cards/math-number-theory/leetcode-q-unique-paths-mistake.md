---
id: leetcode-q-unique-paths-mistake
node: math-number-theory.combinatorics
type: qa
anki: 1787102795588
tags: [lc::62, leetcode, mistake, recall]
---
## Q
写网格DP的递推解法时，为什么把 dp 数组初始化为 0 会出错？

## A
如果初始化为 0，dp[0][j] 和 dp[i][0]（第一行、第一列）会一直是 0，因为循环从 i=1, j=1 开始，永远不会被转移方程更新，导致最终结果全是 0 或远小于正确值。必须初始化为 1，因为第一行/第一列各只有唯一一种路径（全右走或全下走）。

**Evidence**

代码中显式写了注释 "# 这里必须初始化 1 而不是 0"，且 for 循环 range(1, m)/range(1, n) 从索引 1 开始，说明作者意识到边界行列不会被循环覆盖，必须靠初始值兜底。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F62%20-%20Unique%20Paths)
