---
id: leetcode-c-endlesscheng-mor1u6-segment-tree-point-update-invariant
node: advanced-ds-heap.segment-tree-point-update
type: cloze
anki: 1789002115520
tags: [concept-cloze, invariant, leetcode, recall]
---
线段树父节点始终等于左右孩子的 {{c1::merge 结果}}。

每个节点值等于两个子区间值的 merge；查询只合并与目标区间相交的节点；更新叶子后必须向上重新维护祖先

**Evidence**

§8.3 线段树（无区间更新）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.15%20-%20%E7%BA%BF%E6%AE%B5%E6%A0%91%EF%BC%9A%E5%8D%95%E7%82%B9%E6%9B%B4%E6%96%B0%E4%B8%8E%E5%8C%BA%E9%97%B4%E8%81%9A%E5%90%88)
