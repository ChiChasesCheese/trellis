---
id: leetcode-c-endlesscheng-g6ktkl-minimum-interval-cover-recognition
node: greedy-sorting.minimum-interval-cover
type: cloze
anki: 1787272433804
tags: [concept-cloze, leetcode, recall, recognition]
---
最少区间连续覆盖目标线段时，在所有左端点不超过当前前沿的区间中选 {{c1::右端点最远}} 的。

覆盖目标线段时，从当前未覆盖位置出发，在所有可接上的区间中选择右端点最远者；若不能推进则无解。

**Evidence**

§2.4

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.09%20-%20%E6%9C%80%E5%B0%91%E5%8C%BA%E9%97%B4%E8%A6%86%E7%9B%96)
