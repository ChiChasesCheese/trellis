---
id: leetcode-c-endlesscheng-v2rxsn-fenwick-tree-invariant
node: advanced-ds-heap.fenwick-tree
type: cloze
anki: 1787272467879
tags: [concept-cloze, invariant, leetcode, recall]
---
Fenwick Tree 的 tree[i] 覆盖长度为 {{c1::i & -i}} 的块。

tree[i] 聚合覆盖长度 lowbit(i) 的区间；更新沿 i += lowbit(i) 影响所有包含该点的块

**Evidence**

四、数据结构：树状数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.18%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%20Fenwick%20Tree)
