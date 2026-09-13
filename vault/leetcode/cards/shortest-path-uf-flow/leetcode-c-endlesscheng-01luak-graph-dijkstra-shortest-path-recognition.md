---
id: leetcode-c-endlesscheng-01luak-graph-dijkstra-shortest-path-recognition
node: shortest-path-uf-flow.graph-dijkstra-shortest-path
type: cloze
anki: 1787272409506
tags: [concept-cloze, leetcode, recall, recognition]
---
求单源最短路且所有边权{{c1::非负}}时，应使用 Dijkstra 算法而不是 BFS 或 Bellman-Ford。

用小根堆贪心地每次取出当前离起点最近的未确定节点，松弛其所有邻居；要求图中没有负权边，堆中允许有过期的（懒删除）数据。

**Evidence**

§3.1 单源最短路：Dijkstra 算法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.07%20-%20%E5%8D%95%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%9ADijkstra%20%E7%AE%97%E6%B3%95)
