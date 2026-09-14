---
id: leetcode-c-endlesscheng-txls3i-subset-enumeration-dp-invariant
node: dp-grid-interval-string.subset-enumeration-dp
type: cloze
anki: 1787272415307
tags: [concept-cloze, invariant, leetcode, recall]
---
SOS 子集和传播只在 mask 的某位为 {{c1::1}} 时进行。

子集枚举中 sub 始终是 mask 的子集；SOS 每次只沿一个 bit 从相邻掩码传播

**Evidence**

§9.6 SOS DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.13%20-%20%E5%AD%90%E9%9B%86%E6%9E%9A%E4%B8%BE%E4%B8%8E%20SOS%20DP)
