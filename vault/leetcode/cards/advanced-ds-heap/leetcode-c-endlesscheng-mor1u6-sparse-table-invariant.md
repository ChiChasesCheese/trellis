---
id: leetcode-c-endlesscheng-mor1u6-sparse-table-invariant
node: advanced-ds-heap.sparse-table
type: cloze
anki: 1787272423707
tags: [concept-cloze, invariant, leetcode, recall]
---
ST 表 O(1) 双块查询依赖操作是 {{c1::幂等}} 的。

st[k][i] 覆盖 [i,i+2^k)；查询区间长度 L 取 k=floor(log2 L)；两个长度 2^k 块覆盖查询区间两端

**Evidence**

§8.7 ST 表（Sparse Table）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.20%20-%20ST%20%E8%A1%A8%EF%BC%88Sparse%20Table%EF%BC%89)
