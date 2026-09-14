---
id: leetcode-c-endlesscheng-v2rxsn-tree-dp-rerooting-recognition
node: tree-advanced.tree-dp-rerooting
type: cloze
anki: 1787272465381
tags: [concept-cloze, leetcode, recall, recognition]
---
状态由各个子树合并得到时，用 {{c1::树形 DP}}。

先在任意根下自底向上汇总子树信息；若每个节点都可能作根，再把父侧信息在第二次 DFS 中传给子节点。

**Evidence**

二、动态规划：树形 DP、换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.10%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E6%8D%A2%E6%A0%B9%20DP)
