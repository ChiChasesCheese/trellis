---
id: leetcode-c-endlesscheng-wr1mjp-tree-dp-and-center-expansion-invariant
node: tree-advanced.tree-dp-and-center-expansion
type: cloze
anki: 1787272472080
tags: [concept-cloze, invariant, leetcode, recall]
---
树形 DFS 访问邻居时必须跳过 {{c1::parent}}，使每个状态只处理自己的子树。

树形 DP 中 child 的状态只代表其子树，父子合并不重复经过父边；中心扩展每次检查的区间保持回文，扩一层只验证新两端

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.09%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95)
