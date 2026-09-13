---
id: leetcode-c-endlesscheng-v2rxsn-lazy-segment-tree-recognition
node: advanced-ds-heap.lazy-segment-tree
type: cloze
anki: 1787272468079
tags: [concept-cloze, leetcode, recall, recognition]
---
需要频繁区间更新和区间查询，且两者都不能降为简单前缀操作时，用 {{c1::Lazy 线段树}}。

用树节点维护区间聚合值，并用 lazy 标记延迟向子节点下传整段更新，适合区间更新与区间查询并存。

**Evidence**

四、数据结构：lazy 线段树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.19%20-%20Lazy%20%E7%BA%BF%E6%AE%B5%E6%A0%91)
