---
id: leetcode-c-endlesscheng-txls3i-grid-path-dp-invariant
node: dp-grid-interval-string.grid-path-dp
type: cloze
anki: 1787272412603
tags: [concept-cloze, invariant, leetcode, recall]
---
网格 DP 的遍历顺序必须保证 {{c1::所有前驱先于当前格}}。

dp[r][c] 是到达该格子的题目要求值；障碍格或不可达格必须保持单位元/无穷值

**Evidence**

二、网格图 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.04%20-%20%E7%BD%91%E6%A0%BC%E8%B7%AF%E5%BE%84%20DP)
