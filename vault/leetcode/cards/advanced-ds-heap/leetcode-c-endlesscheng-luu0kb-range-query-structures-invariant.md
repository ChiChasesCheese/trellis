---
id: leetcode-c-endlesscheng-luu0kb-range-query-structures-invariant
node: advanced-ds-heap.range-query-structures
type: cloze
anki: 1787272460680
tags: [concept-cloze, invariant, leetcode, recall]
---
Fenwick 内部下标从 1 开始，节点 i 覆盖长度为 {{c1::lowbit(i)}} 的区间。

树状数组节点覆盖 lowbit 对应的一段前缀信息；线段树每个节点等于其子区间聚合；堆顶始终是尚未删除候选中的最小键

**Evidence**

四、数据结构：树状数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.17%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E3%80%81%E7%BA%BF%E6%AE%B5%E6%A0%91%E4%B8%8E%E6%9C%80%E5%B0%8F%E5%A0%86)
