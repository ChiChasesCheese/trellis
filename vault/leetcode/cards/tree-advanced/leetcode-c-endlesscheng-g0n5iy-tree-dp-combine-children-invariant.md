---
id: leetcode-c-endlesscheng-g0n5iy-tree-dp-combine-children-invariant
node: tree-advanced.tree-dp-combine-children
type: cloze
anki: 1787272478980
tags: [concept-cloze, invariant, leetcode, recall]
---
树形 DP 的 dfs 返回值应只描述 {{c1::当前节点子树}}。

dfs(u, parent) 返回的值只描述 u 的子树；合并子树时不重复经过父边；全局答案在每个节点都考虑经过该节点的组合

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.11%20-%20%E6%A0%91%E5%BD%A2%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
