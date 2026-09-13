---
id: leetcode-c-endlesscheng-luu0kb-knapsack-dp-invariant
node: dp-linear-knapsack.knapsack-dp
type: cloze
anki: 1787272457680
tags: [concept-cloze, invariant, leetcode, recall]
---
一维 {{c1::0-1 背包}} 的容量循环必须倒序，才能保证一个物品最多使用一次。

dp[c] 表示已处理物品下容量 c 的最佳值或方案数；0-1 背包倒序容量，保证同一物品只用一次；完全背包正序容量，允许重复使用当前物品

**Evidence**

二、动态规划：0-1 背包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.07%20-%20%E8%83%8C%E5%8C%85%20DP)
