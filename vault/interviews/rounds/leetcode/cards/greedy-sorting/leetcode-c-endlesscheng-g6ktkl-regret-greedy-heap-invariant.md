---
id: leetcode-c-endlesscheng-g6ktkl-regret-greedy-heap-invariant
node: greedy-sorting.regret-greedy-heap
type: cloze
anki: 1787272433004
tags: [concept-cloze, invariant, leetcode, recall]
---
反悔贪心处理每个前缀后，应保持已选集合 {{c1::可行且在同等数量下资源占用最优}}。

处理每个前缀后，当前集合可行；在相同选择数量下，当前集合的总代价最小或资源占用最少；堆顶始终是最值得反悔的历史选择

**Evidence**

§1.9

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.06%20-%20%E5%8F%8D%E6%82%94%E8%B4%AA%E5%BF%83)
