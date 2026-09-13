---
id: leetcode-c-endlesscheng-01luak-graph-topological-order-dp-invariant
node: graphs-traversal.graph-topological-order-dp
type: cloze
anki: 1787272409005
tags: [concept-cloze, invariant, leetcode, recall]
---
拓扑序 DP 正确性的关键不变量是：节点 x 被弹出队列处理时，{{c1::x 的所有前驱}}都已经完成了对 x 的 dp 贡献。

处理节点 x 时，x 的所有前驱都已经完成过对 x 的贡献（因为 in_deg[x] 归零才会入队）；dp 值在拓扑序中单调地从前驱推向后继，不会出现前驱晚于后继被处理的情况

**Evidence**

§2.2 在拓扑序上 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.05%20-%20%E6%8B%93%E6%89%91%E5%BA%8F%E4%B8%8A%20DP%EF%BC%88%E5%88%B7%E8%A1%A8%E6%B3%95%EF%BC%89)
