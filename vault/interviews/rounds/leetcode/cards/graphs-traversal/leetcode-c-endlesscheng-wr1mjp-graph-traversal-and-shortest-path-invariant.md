---
id: leetcode-c-endlesscheng-wr1mjp-graph-traversal-and-shortest-path-invariant
node: graphs-traversal.graph-traversal-and-shortest-path
type: cloze
anki: 1787272474181
tags: [concept-cloze, invariant, leetcode, recall]
---
BFS 中节点第一次被访问时记录的距离就是 {{c1::最短边数距离}}。

BFS 中节点首次出队/访问时距离为最短边数；Dijkstra 弹出的未过期最小距离已是最终最短距离；DFS visited 保证每个节点最多展开一次

**Evidence**

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.16%20-%20DFS%E3%80%81BFS%20%E4%B8%8E%E6%9C%80%E7%9F%AD%E8%B7%AF)
