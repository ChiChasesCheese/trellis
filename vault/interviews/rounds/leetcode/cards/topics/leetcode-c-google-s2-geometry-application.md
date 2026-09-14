---
id: leetcode-c-google-s2-geometry-application
node: topics.uncategorised
type: qa
anki: 1787361362123
tags: [algorithm::bit-interleaving, algorithm::computational-geometry, algorithm::hilbert-curve, application, case, case::google-s2-geometry, category::developer-infrastructure, chapter::09, chapter::16, leetcode, system::google-s2-geometry]
---
## Q
S2 CellID 如何把球面层级网格变成可做 range scan 的 64-bit key？

## A
先选 cube face，再递归四分 cell，并把 Hilbert curve position 与 level 编码进 ID。一个层级 cell 的 descendants 对应连续或少量连续范围，索引先筛候选再做精确几何判断。

**Evidence**

S2 官方开发指南说明六个 faces、Hilbert traversal、64-bit CellID 与 cell hierarchy。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FGoogle%20S2%EF%BC%9A%E7%90%83%E9%9D%A2%E5%87%A0%E4%BD%95%E4%B8%8E%20Hilbert%20Cell%20ID)
