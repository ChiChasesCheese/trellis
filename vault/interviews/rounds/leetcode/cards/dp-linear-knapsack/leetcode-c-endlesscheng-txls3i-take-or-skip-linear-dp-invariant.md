---
id: leetcode-c-endlesscheng-txls3i-take-or-skip-linear-dp-invariant
node: dp-linear-knapsack.take-or-skip-linear-dp
type: cloze
anki: 1787272412005
tags: [concept-cloze, invariant, leetcode, recall]
---
打家劫舍类 DP 中，选择当前位置必须从 {{c1::不与它冲突的前缀最优值}} 转移。

dp[i] 表示处理前 i 个元素后的最优值；选择 i 时只能从与它兼容的历史状态转移

**Evidence**

§1.2 打家劫舍

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.02%20-%20%E9%80%89%E6%88%96%E4%B8%8D%E9%80%89%E7%BA%BF%E6%80%A7%20DP)
