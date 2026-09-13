---
id: leetcode-c-endlesscheng-iyt3ss-moore-voting-invariant
node: arrays-hash-prefix.moore-voting
type: cloze
anki: 1787272431207
tags: [concept-cloze, invariant, leetcode, recall]
---
摩尔投票的正确性来自不同元素的 {{c1::两两抵消}} 不会消灭严格多数。

不同元素两两抵消不会改变严格多数元素是否存在；计数器为正时，候选在未抵消剩余元素中领先；第一遍得到的是候选，未保证时还需验证

**Evidence**

§7.8 摩尔投票法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.22%20-%20%E6%91%A9%E5%B0%94%E6%8A%95%E7%A5%A8%E6%B3%95)
