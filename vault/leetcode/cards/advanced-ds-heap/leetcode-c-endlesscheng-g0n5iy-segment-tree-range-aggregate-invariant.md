---
id: leetcode-c-endlesscheng-g0n5iy-segment-tree-range-aggregate-invariant
node: advanced-ds-heap.segment-tree-range-aggregate
type: cloze
anki: 1787272480480
tags: [concept-cloze, invariant, leetcode, recall]
---
线段树父节点值必须等于左右子节点按 {{c1::同一聚合规则}} 合并的结果。

每个节点保存其覆盖区间的准确聚合值；父节点值始终由两个子节点按同一 combine 规则得到

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.16%20-%20%E7%BA%BF%E6%AE%B5%E6%A0%91%E5%8C%BA%E9%97%B4%E8%81%9A%E5%90%88%E4%B8%8E%E5%AE%9A%E4%BD%8D)
