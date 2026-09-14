---
id: leetcode-q-minimum-height-trees-pattern
node: graphs-traversal.topological-sort
type: qa
anki: 1787102262283
tags: [lc::310, leetcode, pattern, recall]
---
## Q
如何在无向树中求最小高度树(MHT)的根节点（LC 310）？

## A
用“剥叶子”式的拓扑排序：先建邻接表并统计每个节点的度数，把度为1的节点作为初始叶子入队；每轮把当前层的所有叶子同时剥掉（相邻节点度数-1，新出现的度为1节点加入下一轮队列），直到剩余节点数 rem <= 2 为止；此时队列里剩下的 1~2 个节点就是所有 MHT 的根。原理：树的中心一定落在最长路径（直径）的中点上，逐层剥叶子等价于从两端向中心收缩直径。复杂度 O(V+E)，n=1 需特判直接返回 [0]。

**Evidence**

代码用 degrees 数组统计度数，leaves = deque(度为1的节点)，while rem > 2 时按层剥叶子（leaf_cnt = len(leaves) 保证按层处理），最终 return list(leaves)；且开头对 n==1 做了特判 return [0]。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F310%20-%20Minimum%20Height%20Trees)
