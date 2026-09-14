---
id: leetcode-c-endlesscheng-wr1mjp-graph-traversal-and-shortest-path-recognition
node: graphs-traversal.graph-traversal-and-shortest-path
type: cloze
anki: 1787272474079
tags: [concept-cloze, leetcode, recall, recognition]
---
无权图中求起点到各点最少边数，应使用 {{c1::BFS}}。

DFS 用于连通块、遍历和树形结构；BFS 在无权图中按层保证最短边数；带非负权图用 Dijkstra 按当前最小距离扩展。

**Evidence**

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.16%20-%20DFS%E3%80%81BFS%20%E4%B8%8E%E6%9C%80%E7%9F%AD%E8%B7%AF)
