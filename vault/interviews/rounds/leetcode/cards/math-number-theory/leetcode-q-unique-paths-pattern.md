---
id: leetcode-q-unique-paths-pattern
node: math-number-theory.combinatorics
type: qa
anki: 1787102263008
tags: [lc::62, leetcode, pattern, recall]
---
## Q
网格DP：机器人从左上到右下只能右/下移动，求路径数——如何设计状态转移？

## A
递推法：dp[i][j] 表示到达 (i,j) 的路径数，转移方程 dp[i][j] = dp[i-1][j] + dp[i][j-1]。第一行和第一列只有一种走法（一直沿边走），所以初始化整个 dp 数组为 1（而不是 0），这样第一行/第一列天然满足边界条件，无需额外处理。也可用记忆化搜索 dfs(i,j)，终止条件为到达终点返回 1，越界返回 0，两种写法本质等价（组合数学角度：答案即 C(m+n-2, m-1)）。

**Evidence**

dp = [[1] * n for _ in range(m)] ... # 这里必须初始化 1 而不是 0；以及 dfs 终止条件 if i == m-1 and j == n-1: return 1

[原文 ↗](obsidian://open?vault=lc&file=questions%2F62%20-%20Unique%20Paths)
