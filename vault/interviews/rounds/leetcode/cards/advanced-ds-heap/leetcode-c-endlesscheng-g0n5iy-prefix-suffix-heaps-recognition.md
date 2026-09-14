---
id: leetcode-c-endlesscheng-g0n5iy-prefix-suffix-heaps-recognition
node: advanced-ds-heap.prefix-suffix-heaps
type: cloze
anki: 1787272479480
tags: [concept-cloze, leetcode, recall, recognition]
---
每个切分点都要比较左右两侧各自最优的固定数量元素时，用 {{c1::前后缀堆}}。

当要在每个分割点比较左侧选最小若干项与右侧选最大若干项时，分别扫描两次，用堆维护固定数量的最佳元素和。

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.13%20-%20%E5%89%8D%E5%90%8E%E7%BC%80%E5%A0%86%E9%80%89%E6%8B%A9)
