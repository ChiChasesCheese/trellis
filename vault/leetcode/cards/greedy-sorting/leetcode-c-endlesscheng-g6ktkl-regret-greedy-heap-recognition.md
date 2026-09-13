---
id: leetcode-c-endlesscheng-g6ktkl-regret-greedy-heap-recognition
node: greedy-sorting.regret-greedy-heap
type: cloze
anki: 1787272432906
tags: [concept-cloze, leetcode, recall, recognition]
---
按序选择但后来的元素可能替换旧选择，并且需快速删掉最差旧选择时，用 {{c1::堆维护反悔贪心}}。

先接受当前看似有利的选择；当约束被破坏时，用堆撤销或替换此前代价最大的选择，使已选集合在当前前缀下保持最佳。

**Evidence**

§1.9

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.06%20-%20%E5%8F%8D%E6%82%94%E8%B4%AA%E5%BF%83)
