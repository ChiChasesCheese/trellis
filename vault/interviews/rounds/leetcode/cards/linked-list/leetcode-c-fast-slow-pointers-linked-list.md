---
id: leetcode-c-fast-slow-pointers-linked-list
node: linked-list.fast-slow-pointers-linked-list
type: cloze
anki: 1787102264060
tags: [concept-cloze, leetcode, recall]
---
在快慢指针模式中，慢指针每次走1步，快指针每次走{{c1::2}}步；当快指针到达链表末尾（fast为None或fast.next为None）时，慢指针恰好停在{{c2::中点（偶数长度时为前中点）}}。

该不变量成立的前提是两指针都从head出发；若fast误初始化为head.next会导致步长错位，破坏这一不变量。

**Evidence**

fast永远不会"落后"于slow；当fast到达末尾时，slow恰好在中点（奇数长）或前中点（偶数长）。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E9%93%BE%E8%A1%A8%E5%BF%AB%E6%85%A2%E6%8C%87%E9%92%88)
