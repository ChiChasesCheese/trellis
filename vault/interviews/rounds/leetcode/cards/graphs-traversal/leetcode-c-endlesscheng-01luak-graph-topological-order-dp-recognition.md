---
id: leetcode-c-endlesscheng-01luak-graph-topological-order-dp-recognition
node: graphs-traversal.graph-topological-order-dp
type: cloze
anki: 1787272408904
tags: [concept-cloze, leetcode, recall, recognition]
---
在 DAG 上做依赖顺序明确的 DP（如求最长路径），且想用非递归方式实现时，可以在{{c1::拓扑排序}}的同时进行刷表法 DP。

在做 Kahn 拓扑排序的同时，把当前节点的 DP 值“推送”给所有后继节点（刷表法），保证每个节点在被处理时其所有前驱都已经贡献完毕。

**Evidence**

§2.2 在拓扑序上 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.05%20-%20%E6%8B%93%E6%89%91%E5%BA%8F%E4%B8%8A%20DP%EF%BC%88%E5%88%B7%E8%A1%A8%E6%B3%95%EF%BC%89)
