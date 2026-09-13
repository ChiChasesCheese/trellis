---
id: leetcode-q-maximum-path-score-in-a-grid-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787181734283
tags: [lc::3742, leetcode, pattern, recall]
---
## Q
网格图 DP 中，若要求路径上恰好有 k 个满足某条件的格子时最大化另一个（不同的）值总和，如何设计状态？

## A
把「计数维度」放进返回值而不是放进递归参数：dfs(i,j) 返回一个长度为 k+1 的数组 arr，其中 arr[c] 表示从 (i,j) 走到终点、这段后缀路径上恰好有 c 个满足条件的格子时能拿到的最大原始值总和。转移时枚举子节点在各个计数下的最优值，取 max 后加上当前格子的值：arr[c+delta] = max(children[c]) + value。这样把「被 k 限制的计数」和「被 maximize 的值」两个不同的量分离开，一次 dfs 调用产出所有 k 值下的答案，避免把 cost 作为参数塞进 @cache 导致状态爆炸。

**Evidence**

maxPathScore 中 dfs(i,j) 返回 tuple(arr)，arr[c] 表示恰好 c 个 >=1 格子时的最大原始值总和；对比 maxPathScore_mle 中 dfs(i,j,cost) 把 cost 作为参数直接缓存。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3742%20-%20Maximum%20Path%20Score%20in%20a%20Grid)
