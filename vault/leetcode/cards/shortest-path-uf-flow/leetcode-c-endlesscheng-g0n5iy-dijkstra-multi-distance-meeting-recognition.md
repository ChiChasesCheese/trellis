---
id: leetcode-c-endlesscheng-g0n5iy-dijkstra-multi-distance-meeting-recognition
node: shortest-path-uf-flow.dijkstra-multi-distance-meeting
type: cloze
anki: 1787272482180
tags: [concept-cloze, leetcode, recall, recognition]
---
非负权多路径题允许在某节点汇合并共享后缀时，可用 {{c1::多次 Dijkstra 加枚举汇合点}}。

非负权图中先从若干关键点分别跑单源最短路，再枚举汇合点组合距离；共享后缀或交汇结构可由同一节点的距离和表达。

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.22%20-%20Dijkstra%20%E5%A4%9A%E6%BA%90%E8%B7%9D%E7%A6%BB%E7%BB%84%E5%90%88)
