---
id: leetcode-c-endlesscheng-g6ktkl-interval-grouping-heap-invariant
node: greedy-sorting.interval-grouping-heap
type: cloze
anki: 1787272433604
tags: [concept-cloze, invariant, leetcode, recall]
---
区间分组堆顶表示 {{c1::最早结束的已占用组}}。

堆中每个元素对应一个已使用组的最后结束时间；处理当前左端点前，堆大小等于仍与当前位置重叠的组数；若最早结束组不可复用，则其他组也不可复用

**Evidence**

§2.2

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.08%20-%20%E5%8C%BA%E9%97%B4%E5%88%86%E7%BB%84)
