---
id: leetcode-c-endlesscheng-txls3i-interval-dp-invariant
node: dp-grid-interval-string.interval-dp
type: cloze
anki: 1787272414704
tags: [concept-cloze, invariant, leetcode, recall]
---
区间 DP 必须保证 {{c1::短区间先于长区间}} 被计算。

dp[l][r] 只依赖更短区间；遍历必须先计算短区间再计算长区间

**Evidence**

八、区间 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.11%20-%20%E5%8C%BA%E9%97%B4%20DP%20%E4%B8%8E%E5%8F%AF%E6%B6%88%E9%99%A4%E5%8C%BA%E9%97%B4)
