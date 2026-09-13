---
id: leetcode-c-endlesscheng-txls3i-subset-enumeration-dp-recognition
node: dp-grid-interval-string.subset-enumeration-dp
type: cloze
anki: 1787272415205
tags: [concept-cloze, leetcode, recall, recognition]
---
对每个集合都要枚举其子集，整体复杂度通常是 {{c1::O(3^n)}}。

子集 DP 枚举 mask 的子集来分组；SOS DP 则沿每一位传播，使每个 mask 聚合其全部子集或超集的信息。

**Evidence**

§9.4 子集状压 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.13%20-%20%E5%AD%90%E9%9B%86%E6%9E%9A%E4%B8%BE%E4%B8%8E%20SOS%20DP)
