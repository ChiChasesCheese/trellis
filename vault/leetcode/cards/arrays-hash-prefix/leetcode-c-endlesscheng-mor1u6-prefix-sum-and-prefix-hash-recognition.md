---
id: leetcode-c-endlesscheng-mor1u6-prefix-sum-and-prefix-hash-recognition
node: arrays-hash-prefix.prefix-sum-and-prefix-hash
type: cloze
anki: 1789002112696
tags: [concept-cloze, leetcode, recall, recognition]
---
子数组条件能写成两个累计状态之差时，用 {{c1::前缀和或前缀状态}}。

把区间累计量表示为两个前缀状态之差；用哈希表记录此前状态的频次、位置或聚合值。距离和可在排序后用前缀和快速计算左右贡献。

**Evidence**

§1.1-§1.4

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.03%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%89%8D%E7%BC%80%E7%8A%B6%E6%80%81%E5%93%88%E5%B8%8C)
