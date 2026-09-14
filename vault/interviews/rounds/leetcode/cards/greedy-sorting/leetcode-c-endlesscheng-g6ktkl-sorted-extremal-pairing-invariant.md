---
id: leetcode-c-endlesscheng-g6ktkl-sorted-extremal-pairing-invariant
node: greedy-sorting.sorted-extremal-pairing
type: cloze
anki: 1787272431506
tags: [concept-cloze, invariant, leetcode, recall]
---
极值配对贪心的核心不变式是：已处理的 {{c1::最小或最大元素}} 已在某个最优解中完成处理。

已处理的极值在某个最优解中可与当前选择等价交换；双指针左侧元素均已得到最优且不可被后续元素改善的处理；每次成功配对后，双方指针之前的元素不再参与决策

**Evidence**

§1.1-§1.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.01%20-%20%E6%8E%92%E5%BA%8F%E5%90%8E%E7%9A%84%E6%9E%81%E5%80%BC%E4%B8%8E%E9%85%8D%E5%AF%B9%E8%B4%AA%E5%BF%83)
