---
id: leetcode-c-endlesscheng-luu0kb-dp-optimizations-monotonic-queue-fenwick-invariant
node: dp-linear-knapsack.dp-optimizations-monotonic-queue-fenwick
type: cloze
anki: 1787272458880
tags: [concept-cloze, invariant, leetcode, recall]
---
单调队列优化中，队首必须始终位于 {{c1::当前有效转移窗口}} 内。

单调队列下标始终在有效窗口内，值保持单调；树状数组节点维护其负责前缀的聚合最优值；每个状态在查询后再更新，避免使用未来状态

**Evidence**

二、动态规划：单调队列优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.11%20-%20DP%20%E4%BC%98%E5%8C%96%EF%BC%9A%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97%E4%B8%8E%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84)
