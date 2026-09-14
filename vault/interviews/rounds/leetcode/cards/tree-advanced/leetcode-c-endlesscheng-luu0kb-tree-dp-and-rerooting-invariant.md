---
id: leetcode-c-endlesscheng-luu0kb-tree-dp-and-rerooting-invariant
node: tree-advanced.tree-dp-and-rerooting
type: cloze
anki: 1787272458280
tags: [concept-cloze, invariant, leetcode, recall]
---
换根 DP 从父到子传播时，应从父答案中 {{c1::移除子树贡献}} 后再加入外侧贡献。

后序 DP 完成后，子节点信息已完整；换根时从父答案移除子树贡献并加入外部贡献；每条树边的两个方向都被一致处理

**Evidence**

二、动态规划：换根 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.09%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E6%8D%A2%E6%A0%B9%20DP)
