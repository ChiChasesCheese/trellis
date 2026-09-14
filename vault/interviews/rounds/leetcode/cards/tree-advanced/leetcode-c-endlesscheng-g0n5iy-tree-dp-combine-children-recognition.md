---
id: leetcode-c-endlesscheng-g0n5iy-tree-dp-combine-children-recognition
node: tree-advanced.tree-dp-combine-children
type: cloze
anki: 1787272478880
tags: [concept-cloze, leetcode, recall, recognition]
---
节点答案由多个独立子树贡献合并而成时，用 {{c1::树形 DP}}。

以根确定父子关系，先递归求子树状态，再把各子树贡献合并到当前节点；路径题常需保留最优的若干条子链。

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.11%20-%20%E6%A0%91%E5%BD%A2%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
