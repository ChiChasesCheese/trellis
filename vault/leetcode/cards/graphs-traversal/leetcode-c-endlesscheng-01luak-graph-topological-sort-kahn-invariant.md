---
id: leetcode-c-endlesscheng-01luak-graph-topological-sort-kahn-invariant
node: graphs-traversal.graph-topological-sort-kahn
type: cloze
anki: 1787272408706
tags: [concept-cloze, invariant, leetcode, recall]
---
拓扑排序的核心不变量是：对任意有向边 x→y，在排序结果中 {{c1::x 一定排在 y 之前}}。

对任意有向边 x→y，x 一定排在 y 之前；入度为 0 的节点集合始终代表“当前可以立即处理”的节点

**Evidence**

§2.1 拓扑排序

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.04%20-%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%EF%BC%88Kahn%20%E7%AE%97%E6%B3%95%EF%BC%89)
