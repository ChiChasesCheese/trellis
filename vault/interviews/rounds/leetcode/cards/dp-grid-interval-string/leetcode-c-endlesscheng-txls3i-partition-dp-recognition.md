---
id: leetcode-c-endlesscheng-txls3i-partition-dp-recognition
node: dp-grid-interval-string.partition-dp
type: cloze
anki: 1787272413705
tags: [concept-cloze, leetcode, recall, recognition]
---
把序列划成连续段时，常通过枚举 {{c1::最后一段的左端点}} 转移。

固定最后一段，枚举其左端点；前缀状态与末段是否合法或得分共同决定当前状态。

**Evidence**

五、划分型 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.08%20-%20%E5%88%92%E5%88%86%E5%9E%8B%20DP)
