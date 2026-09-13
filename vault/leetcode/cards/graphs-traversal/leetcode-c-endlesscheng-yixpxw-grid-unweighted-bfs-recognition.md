---
id: leetcode-c-endlesscheng-yixpxw-grid-unweighted-bfs-recognition
node: graphs-traversal.grid-unweighted-bfs
type: cloze
anki: 1787272404405
tags: [concept-cloze, leetcode, recall, recognition]
---
网格中每一步代价都相同，并要求最少步数时，应使用 {{c1::BFS}}，而不是普通 DFS。

当每次移动代价相同（通常为 1）时，用 FIFO 队列按距离层扩展。首次到达某个格子的距离就是从起点到它的最短距离。

**Evidence**

二、网格图 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.02%20-%20%E7%BD%91%E6%A0%BC%E6%97%A0%E6%9D%83%E6%9C%80%E7%9F%AD%E8%B7%AF%20BFS)
