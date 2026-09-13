---
id: leetcode-c-endlesscheng-g0n5iy-zero-one-bfs-recognition
node: shortest-path-uf-flow.zero-one-bfs
type: cloze
anki: 1787272482780
tags: [concept-cloze, leetcode, recall, recognition]
---
最短路图的边权只为 0 或 1 时，用 {{c1::0-1 BFS}}。

边权仅为 0 或 1 时，用双端队列代替堆：走 0 边加入队首，走 1 边加入队尾，从而在线性时间求最短路。

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.24%20-%20%E5%9B%BE%E8%AE%BA%EF%BC%9A0-1%20BFS)
