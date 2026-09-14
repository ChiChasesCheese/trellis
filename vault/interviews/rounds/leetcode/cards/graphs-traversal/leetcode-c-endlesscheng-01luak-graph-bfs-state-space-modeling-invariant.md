---
id: leetcode-c-endlesscheng-01luak-graph-bfs-state-space-modeling-invariant
node: graphs-traversal.graph-bfs-state-space-modeling
type: cloze
anki: 1787272408404
tags: [concept-cloze, invariant, leetcode, recall]
---
状态空间 BFS 能正确求最少步数的前提是每个状态必须{{c1::可哈希且可判重}}，否则无法保证每个状态只入队一次。

状态必须可哈希且能判重，否则 BFS 会重复展开导致超时或死循环；起点到任意状态的距离仍满足 BFS 分层单调性

**Evidence**

§1.3 图论建模 + BFS 最短路

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.03%20-%20%E5%9B%BE%E8%AE%BA%E5%BB%BA%E6%A8%A1%20%2B%20BFS%20%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%88%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%90%9C%E7%B4%A2%EF%BC%89)
