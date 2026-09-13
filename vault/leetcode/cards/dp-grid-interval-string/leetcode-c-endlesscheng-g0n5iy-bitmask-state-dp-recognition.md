---
id: leetcode-c-endlesscheng-g0n5iy-bitmask-state-dp-recognition
node: dp-grid-interval-string.bitmask-state-dp
type: cloze
anki: 1787272478280
tags: [concept-cloze, leetcode, recall, recognition]
---
对象数很小且“已选集合”足以描述历史时，用 {{c1::状态压缩 DP}}。

当对象数很小且子集本身就是完整历史摘要时，用位掩码编码已选集合，再枚举加入、删除或划分的位。

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.09%20-%20%E7%8A%B6%E6%80%81%E5%8E%8B%E7%BC%A9%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
