---
id: leetcode-c-endlesscheng-g0n5iy-fenwick-tree-prefix-counts-invariant
node: advanced-ds-heap.fenwick-tree-prefix-counts
type: cloze
anki: 1787272479879
tags: [concept-cloze, invariant, leetcode, recall]
---
Fenwick 的 bit[i] 覆盖长度为 {{c1::i & -i}} 的末尾区间。

bit[i] 存储长度为 lowbit(i) 的区间和；prefix(i) 累加的块恰好不重不漏地覆盖 [1, i]

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.14%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E5%89%8D%E7%BC%80%E8%AE%A1%E6%95%B0)
