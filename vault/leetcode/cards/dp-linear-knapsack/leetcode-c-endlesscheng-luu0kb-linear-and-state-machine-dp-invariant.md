---
id: leetcode-c-endlesscheng-luu0kb-linear-and-state-machine-dp-invariant
node: dp-linear-knapsack.linear-and-state-machine-dp
type: cloze
anki: 1787272457380
tags: [concept-cloze, invariant, leetcode, recall]
---
DP 状态必须包含所有会影响未来决策的 {{c1::最少历史信息}}。

dp[i][s] 表示处理完前 i 个元素且处于 s 的最优值；转移只从已经完成的前缀读取；每个状态定义覆盖所有合法历史且不混入非法历史

**Evidence**

二、动态规划：线性 DP、状态机 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.06%20-%20%E7%BA%BF%E6%80%A7%20DP%20%E4%B8%8E%E7%8A%B6%E6%80%81%E6%9C%BA%20DP)
