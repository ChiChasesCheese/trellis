---
id: leetcode-c-endlesscheng-txls3i-knapsack-family-invariant
node: dp-linear-knapsack.knapsack-family
type: cloze
anki: 1787272412903
tags: [concept-cloze, invariant, leetcode, recall]
---
一维 0-1 背包必须按容量 {{c1::倒序}} 更新。

dp[c] 是处理过的候选能达到的容量 c 最优值；0-1 倒序循环保证当前物品只贡献一次

**Evidence**

§3.1 0-1 背包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.05%20-%20%E8%83%8C%E5%8C%85%EF%BC%9A0-1%E3%80%81%E5%AE%8C%E5%85%A8%E3%80%81%E5%A4%9A%E9%87%8D%E4%B8%8E%E5%88%86%E7%BB%84)
