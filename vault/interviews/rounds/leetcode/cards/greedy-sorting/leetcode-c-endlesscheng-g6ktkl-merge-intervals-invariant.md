---
id: leetcode-c-endlesscheng-g6ktkl-merge-intervals-invariant
node: greedy-sorting.merge-intervals
type: cloze
anki: 1787272434204
tags: [concept-cloze, invariant, leetcode, recall]
---
合并扫描中 current 表示 {{c1::尚未输出的连通区间并集}}。

输出列表中的区间两两不重叠且已完成；current 是所有已扫描但尚未输出、彼此连通区间的并集；之后区间的左端点不小于已扫描区间的左端点

**Evidence**

§2.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.10%20-%20%E5%90%88%E5%B9%B6%E5%8C%BA%E9%97%B4)
