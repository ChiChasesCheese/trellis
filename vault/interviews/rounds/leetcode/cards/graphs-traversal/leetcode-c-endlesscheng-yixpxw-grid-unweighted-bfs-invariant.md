---
id: leetcode-c-endlesscheng-yixpxw-grid-unweighted-bfs-invariant
node: graphs-traversal.grid-unweighted-bfs
type: cloze
anki: 1787272404506
tags: [concept-cloze, invariant, leetcode, recall]
---
无权 BFS 中，某格第一次被发现并写入距离时，该距离就是 {{c1::从起点到该格的最短距离}}。

队列中的状态按非递减距离出队。；格子第一次被赋值距离时，该距离已是最短距离。；只把尚未发现的合法邻居入队，避免重复入队。

**Evidence**

二、网格图 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.02%20-%20%E7%BD%91%E6%A0%BC%E6%97%A0%E6%9D%83%E6%9C%80%E7%9F%AD%E8%B7%AF%20BFS)
