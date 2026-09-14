---
id: leetcode-c-endlesscheng-txls3i-permutation-bitmask-dp-recognition
node: dp-grid-interval-string.permutation-bitmask-dp
type: cloze
anki: 1787272414905
tags: [concept-cloze, leetcode, recall, recognition]
---
n 不大且要枚举访问顺序时，考虑 {{c1::排列型状压 DP}}。

用位掩码记录已选集合；若相邻代价有关，再记录最后一个元素。TSP 是该模式的典型实例。

**Evidence**

§9.1 排列型状压 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.12%20-%20%E6%8E%92%E5%88%97%E5%9E%8B%E7%8A%B6%E6%80%81%E5%8E%8B%E7%BC%A9%20DP%20%E4%B8%8E%20TSP)
