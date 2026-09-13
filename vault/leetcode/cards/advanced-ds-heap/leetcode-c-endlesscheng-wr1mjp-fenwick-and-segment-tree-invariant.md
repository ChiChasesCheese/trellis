---
id: leetcode-c-endlesscheng-wr1mjp-fenwick-and-segment-tree-invariant
node: advanced-ds-heap.fenwick-and-segment-tree
type: cloze
anki: 1787272473879
tags: [concept-cloze, invariant, leetcode, recall]
---
Fenwick 中 tree[i] 覆盖的区间长度是 {{c1::i & -i}}。

Fenwick 的 tree[i] 聚合长度 lowbit(i) 的末尾区间；线段树每个节点准确聚合它覆盖区间的信息

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.15%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E4%B8%8E%E7%BA%BF%E6%AE%B5%E6%A0%91)
