---
id: leetcode-c-endlesscheng-g0n5iy-bitmask-state-dp-invariant
node: dp-grid-interval-string.bitmask-state-dp
type: cloze
anki: 1787272478380
tags: [concept-cloze, invariant, leetcode, recall]
---
状态压缩 DP 中 mask 的每一位必须对应 {{c1::固定的一个对象}}。

mask 的每一位与一个固定对象一一对应；dp[mask] 只表示该集合，不混入未编码的历史

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.09%20-%20%E7%8A%B6%E6%80%81%E5%8E%8B%E7%BC%A9%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
