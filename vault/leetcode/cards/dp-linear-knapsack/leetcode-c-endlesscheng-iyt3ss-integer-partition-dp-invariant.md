---
id: leetcode-c-endlesscheng-iyt3ss-integer-partition-dp-invariant
node: dp-linear-knapsack.integer-partition-dp
type: cloze
anki: 1787272429705
tags: [concept-cloze, invariant, leetcode, recall]
---
整数拆分 DP 中外层枚举 part，保证每个 {{c1::多重集只计一次}}。

外层枚举当前允许的最大部件，保证每种多重集只计一次；dp[s] 表示只用已处理部件组成 s 的方案数；dp[0]=1 表示空选择的一种基础方案

**Evidence**

§7.2 整数拆分

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.17%20-%20%E6%95%B4%E6%95%B0%E6%8B%86%E5%88%86%E8%AE%A1%E6%95%B0)
