---
id: leetcode-c-endlesscheng-yixpxw-grid-zero-one-bfs-invariant
node: shortest-path-uf-flow.grid-zero-one-bfs
type: cloze
anki: 1787272404805
tags: [concept-cloze, invariant, leetcode, recall]
---
0-1 BFS 松弛一条 {{c1::0 权边}} 后，目标状态必须加入队首；松弛 1 权边则加入队尾。

双端队列保持待处理状态的距离非递减。；通过 0 权边得到更短距离时放队首，确保它先于更远状态处理。；只有松弛成功时才更新距离并入队。

**Evidence**

三、网格图 0-1 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.03%20-%20%E7%BD%91%E6%A0%BC%200-1%20BFS)
