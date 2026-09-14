---
id: leetcode-c-endlesscheng-txls3i-permutation-bitmask-dp-invariant
node: dp-grid-interval-string.permutation-bitmask-dp
type: cloze
anki: 1787272415004
tags: [concept-cloze, invariant, leetcode, recall]
---
相邻代价相关的状压状态必须额外保存 {{c1::最后一个元素}}。

mask 精确表示已使用元素集合；dp[mask][last] 是以 last 收尾且使用 mask 的最优值

**Evidence**

§9.2 排列型状压 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.12%20-%20%E6%8E%92%E5%88%97%E5%9E%8B%E7%8A%B6%E6%80%81%E5%8E%8B%E7%BC%A9%20DP%20%E4%B8%8E%20TSP)
