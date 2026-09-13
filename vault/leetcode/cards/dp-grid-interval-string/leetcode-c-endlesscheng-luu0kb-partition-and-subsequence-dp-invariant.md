---
id: leetcode-c-endlesscheng-luu0kb-partition-and-subsequence-dp-invariant
node: dp-grid-interval-string.partition-and-subsequence-dp
type: cloze
anki: 1787272457979
tags: [concept-cloze, invariant, leetcode, recall]
---
划分型 DP 中 dp[i] 应表示 {{c1::恰好覆盖前 i 个元素}} 的最优值。

划分 dp[i] 覆盖恰好前 i 个元素；子序列 dp[i] 表示以 i 结尾的最优值；枚举前驱时只接受能合法接到当前状态的转移

**Evidence**

二、动态规划：划分型 DP、子序列 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.08%20-%20%E5%88%92%E5%88%86%E5%9E%8B%E4%B8%8E%E5%AD%90%E5%BA%8F%E5%88%97%20DP)
