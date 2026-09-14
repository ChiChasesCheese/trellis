---
id: leetcode-c-endlesscheng-g6ktkl-median-minimize-l1-invariant
node: greedy-sorting.median-minimize-l1
type: cloze
anki: 1787272436008
tags: [concept-cloze, invariant, leetcode, recall]
---
中位数最优是因为其左右两侧元素数量 {{c1::平衡}}。

目标左侧每向右移动一格会减少左侧距离、增加右侧距离；中位数两侧元素数量平衡，使局部移动不再降低总代价；偶数长度时两个中位数之间的整数都可最优

**Evidence**

§4.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.16%20-%20%E4%B8%AD%E4%BD%8D%E6%95%B0%E8%B4%AA%E5%BF%83)
