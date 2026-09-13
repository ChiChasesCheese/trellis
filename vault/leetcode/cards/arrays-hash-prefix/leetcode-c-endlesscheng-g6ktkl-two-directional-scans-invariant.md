---
id: leetcode-c-endlesscheng-g6ktkl-two-directional-scans-invariant
node: arrays-hash-prefix.two-directional-scans
type: cloze
anki: 1787272437805
tags: [concept-cloze, invariant, leetcode, recall]
---
两次扫描中，左状态只能使用 {{c1::当前位置之前}} 的信息，右状态同理。

左扫数组只依赖当前位置左侧已处理信息；右扫数组只依赖当前位置右侧已处理信息；合并时每个位置使用同一语义下的左右状态

**Evidence**

§5.6

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.22%20-%20%E4%B8%A4%E6%AC%A1%E6%89%AB%E6%8F%8F)
