---
id: leetcode-c-endlesscheng-luu0kb-greedy-interval-coverage-invariant
node: greedy-sorting.greedy-interval-coverage
type: cloze
anki: 1787272461879
tags: [concept-cloze, invariant, leetcode, recall]
---
处理到某一步时，reach 表示所有 [1, {{c1::reach}}] 都可表示。

当前已能覆盖全部目标区间 [1, reach]；若下一个数 x<=reach+1，加入后覆盖扩至 reach+x；若 x>reach+1，必须补一个不大于 reach+1 的资源，取 reach+1 扩张最快

**Evidence**

六、思维题：贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.21%20-%20%E8%B4%AA%E5%BF%83%E8%A6%86%E7%9B%96%E4%B8%8E%E6%9E%84%E9%80%A0)
