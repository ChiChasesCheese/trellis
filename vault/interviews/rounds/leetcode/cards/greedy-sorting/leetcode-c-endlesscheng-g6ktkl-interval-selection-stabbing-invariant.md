---
id: leetcode-c-endlesscheng-g6ktkl-interval-selection-stabbing-invariant
node: greedy-sorting.interval-selection-stabbing
type: cloze
anki: 1787272433304
tags: [concept-cloze, invariant, leetcode, recall]
---
区间选择中，已选最后区间的结束位置应尽量 {{c1::靠左}}。

已选区间两两兼容，或已放点命中所有已扫描区间；记录的位置是当前已选对象的最小可能右边界；按右端点最早选择不会减少后续可选区间数

**Evidence**

§2.1

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.07%20-%20%E4%B8%8D%E7%9B%B8%E4%BA%A4%E5%8C%BA%E9%97%B4%E4%B8%8E%E5%8C%BA%E9%97%B4%E9%80%89%E7%82%B9)
