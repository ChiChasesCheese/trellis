---
id: leetcode-c-endlesscheng-g0n5iy-grouped-knapsack-dp-invariant
node: dp-linear-knapsack.grouped-knapsack-dp
type: cloze
anki: 1787272478681
tags: [concept-cloze, invariant, leetcode, recall]
---
更新当前组时，新状态应从 {{c1::当前组处理前的 old DP}} 转移。

处理第 g 组后，dp[j] 只使用前 g 组；同一组的两个候选不能在一次转移中被重复选择

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.10%20-%20%E5%88%86%E7%BB%84%E8%83%8C%E5%8C%85)
