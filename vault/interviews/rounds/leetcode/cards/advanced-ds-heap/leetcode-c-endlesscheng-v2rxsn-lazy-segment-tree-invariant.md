---
id: leetcode-c-endlesscheng-v2rxsn-lazy-segment-tree-invariant
node: advanced-ds-heap.lazy-segment-tree
type: cloze
anki: 1787272468182
tags: [concept-cloze, invariant, leetcode, recall]
---
线段树节点的值必须已经包含 {{c1::所有作用到该节点区间的更新}}。

节点值已经包含该节点区间上所有已接收更新；lazy 记录尚未下传但已计入节点值的更新

**Evidence**

四、数据结构：lazy 线段树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.19%20-%20Lazy%20%E7%BA%BF%E6%AE%B5%E6%A0%91)
