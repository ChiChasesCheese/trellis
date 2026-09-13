---
id: leetcode-c-endlesscheng-luu0kb-regret-greedy-with-heap-invariant
node: greedy-sorting.regret-greedy-with-heap
type: cloze
anki: 1787272462179
tags: [concept-cloze, invariant, leetcode, recall]
---
反悔贪心的堆应保存当前选择中 {{c1::最值得撤销}} 的元素。

堆保存当前已选且未来可撤销的候选；每次替换只在新方案严格更优时执行；已处理前缀上维护的方案满足当前资源约束

**Evidence**

六、思维题：反悔贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.22%20-%20%E5%8F%8D%E6%82%94%E8%B4%AA%E5%BF%83)
