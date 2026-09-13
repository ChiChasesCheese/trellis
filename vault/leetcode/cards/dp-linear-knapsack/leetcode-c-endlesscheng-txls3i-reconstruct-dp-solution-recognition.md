---
id: leetcode-c-endlesscheng-txls3i-reconstruct-dp-solution-recognition
node: dp-linear-knapsack.reconstruct-dp-solution
type: cloze
anki: 1787272417606
tags: [concept-cloze, leetcode, recall, recognition]
---
DP 题要求输出一个最优方案时，额外记录 {{c1::前驱/决策}}。

在求最优值的同时记录每个状态选择的前驱；从目标状态沿前驱反向走即可恢复一个最优方案。

**Evidence**

专题：输出具体方案（打印方案）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.21%20-%20DP%20%E6%96%B9%E6%A1%88%E8%BF%98%E5%8E%9F)
