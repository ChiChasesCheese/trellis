---
id: leetcode-c-endlesscheng-txls3i-partition-dp-invariant
node: dp-grid-interval-string.partition-dp
type: cloze
anki: 1787272413806
tags: [concept-cloze, invariant, leetcode, recall]
---
划分 DP 的 dp[i] 通常对应前缀 {{c1::a[:i]}}。

dp[i] 只描述前缀 a[:i]；枚举 L 时，最后一段严格是 a[L:i]

**Evidence**

五、划分型 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.08%20-%20%E5%88%92%E5%88%86%E5%9E%8B%20DP)
