---
id: leetcode-c-endlesscheng-01luak-graph-bfs-shortest-path-unweighted-recognition
node: graphs-traversal.graph-bfs-shortest-path-unweighted
type: cloze
anki: 1787272408005
tags: [concept-cloze, leetcode, recall, recognition]
---
当图的边权全部相同（或视为单位权重）且要求最短路径长度时，应使用 {{c1::BFS}} 而不是 Dijkstra。

当所有边权相同（视为 1）时，BFS 按层扩展天然给出从起点到各点的最短跳数，用队列保证先到达的节点距离更短。

**Evidence**

§1.2 广度优先搜索（BFS）

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.02%20-%20BFS%20%E6%B1%82%E5%8D%95%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%88%E6%97%A0%E6%9D%83%E5%9B%BE%EF%BC%89)
