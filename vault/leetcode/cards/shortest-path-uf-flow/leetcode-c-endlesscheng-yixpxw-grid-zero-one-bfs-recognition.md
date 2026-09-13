---
id: leetcode-c-endlesscheng-yixpxw-grid-zero-one-bfs-recognition
node: shortest-path-uf-flow.grid-zero-one-bfs
type: cloze
anki: 1787272404704
tags: [concept-cloze, leetcode, recall, recognition]
---
网格最短路的每次转移代价严格属于 0 和 1 时，使用 {{c1::0-1 BFS 加双端队列}} 可替代 Dijkstra 的堆。

当移动代价只可能为 0 或 1 时，用双端队列替代堆：0 权边从队首加入，1 权边从队尾加入，以线性复杂度求单源最短路。

**Evidence**

三、网格图 0-1 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.03%20-%20%E7%BD%91%E6%A0%BC%200-1%20BFS)
