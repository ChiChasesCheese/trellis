---
id: leetcode-c-endlesscheng-mor1u6-lazy-dynamic-persistent-segment-tree-invariant
node: advanced-ds-heap.lazy-dynamic-persistent-segment-tree
type: cloze
anki: 1789002115820
tags: [concept-cloze, invariant, leetcode, recall]
---
Lazy 节点下探访问孩子前必须 {{c1::下推懒标记}}。

完整覆盖节点时更新节点值并合并懒标记；访问孩子前先下推影响孩子的标记；持久化更新只复制根到目标叶的一条路径

**Evidence**

§8.4 Lazy 线段树（有区间更新）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.16%20-%20Lazy%E3%80%81%E5%8A%A8%E6%80%81%E5%BC%80%E7%82%B9%E4%B8%8E%E5%8F%AF%E6%8C%81%E4%B9%85%E5%8C%96%E7%BA%BF%E6%AE%B5%E6%A0%91)
