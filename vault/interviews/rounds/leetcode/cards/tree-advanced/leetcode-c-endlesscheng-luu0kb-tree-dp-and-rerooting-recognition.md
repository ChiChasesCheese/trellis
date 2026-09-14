---
id: leetcode-c-endlesscheng-luu0kb-tree-dp-and-rerooting-recognition
node: tree-advanced.tree-dp-and-rerooting
type: cloze
anki: 1787272458180
tags: [concept-cloze, leetcode, recall, recognition]
---
子问题天然是子树，且父节点只需汇总孩子信息时，用 {{c1::树形 DP}}。

树上先固定根并汇总子树；若每个节点作为根的答案都需要，利用父子答案的增量关系再做一次换根传播。

**Evidence**

二、动态规划：树形 DP、换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.09%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E6%8D%A2%E6%A0%B9%20DP)
