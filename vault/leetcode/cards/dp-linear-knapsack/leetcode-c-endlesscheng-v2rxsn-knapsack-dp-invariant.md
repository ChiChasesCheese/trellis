---
id: leetcode-c-endlesscheng-v2rxsn-knapsack-dp-invariant
node: dp-linear-knapsack.knapsack-dp
type: cloze
anki: 1787272465180
tags: [concept-cloze, invariant, leetcode, recall]
---
一维 0-1 背包容量必须 {{c1::从大到小}} 遍历。

dp[c] 表示处理到当前物品集合时容量 c 的目标值；0-1 背包倒序遍历容量，避免同一物品重复使用

**Evidence**

二、动态规划：背包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.09%20-%20%E8%83%8C%E5%8C%85%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
