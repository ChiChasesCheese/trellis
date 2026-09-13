---
id: leetcode-c-endlesscheng-g6ktkl-merge-intervals-recognition
node: greedy-sorting.merge-intervals
type: cloze
anki: 1787272434104
tags: [concept-cloze, leetcode, recall, recognition]
---
要求合并重叠区间或求区间并集时，先按 {{c1::左端点升序}} 排序。

按左端点排序后，维护当前合并块；下一个区间重叠则扩展右端点，否则输出当前块并开始新块。

**Evidence**

§2.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.10%20-%20%E5%90%88%E5%B9%B6%E5%8C%BA%E9%97%B4)
