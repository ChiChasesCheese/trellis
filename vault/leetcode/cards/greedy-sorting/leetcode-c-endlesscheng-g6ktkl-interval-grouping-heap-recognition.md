---
id: leetcode-c-endlesscheng-g6ktkl-interval-grouping-heap-recognition
node: greedy-sorting.interval-grouping-heap
type: cloze
anki: 1787272433504
tags: [concept-cloze, leetcode, recall, recognition]
---
所有区间都要分配，且同组不能重叠、要求组数最少时，用 {{c1::左端点排序加最小堆}}。

按左端点处理区间，把当前区间分给结束最早且已空闲的组；同时活跃区间数的最大值就是最少组数。

**Evidence**

§2.2

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.08%20-%20%E5%8C%BA%E9%97%B4%E5%88%86%E7%BB%84)
