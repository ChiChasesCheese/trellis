---
id: leetcode-c-endlesscheng-v2rxsn-tree-dp-rerooting-invariant
node: tree-advanced.tree-dp-rerooting
type: cloze
anki: 1787272465481
tags: [concept-cloze, invariant, leetcode, recall]
---
换根传递给孩子的父侧信息必须 {{c1::排除该孩子子树}}。

第一次 DFS 中子节点状态先于父节点完成；换根时传给孩子的 outside 信息排除了该孩子子树

**Evidence**

二、动态规划：换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.10%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E6%8D%A2%E6%A0%B9%20DP)
