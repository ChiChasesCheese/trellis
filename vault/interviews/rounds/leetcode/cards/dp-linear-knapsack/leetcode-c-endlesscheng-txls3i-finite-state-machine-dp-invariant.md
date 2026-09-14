---
id: leetcode-c-endlesscheng-txls3i-finite-state-machine-dp-invariant
node: dp-linear-knapsack.finite-state-machine-dp
type: cloze
anki: 1787272414104
tags: [concept-cloze, invariant, leetcode, recall]
---
状态机 DP 中每个状态必须代表 {{c1::处理完当前前缀后的合法模式}}。

dp[state] 是处理当前前缀且处于该状态的最优值；非法状态保持负无穷或不更新

**Evidence**

六、状态机 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.09%20-%20%E7%8A%B6%E6%80%81%E6%9C%BA%20DP)
