---
id: leetcode-c-endlesscheng-yixpxw-grid-dijkstra-recognition
node: shortest-path-uf-flow.grid-dijkstra
type: cloze
anki: 1787272405005
tags: [concept-cloze, leetcode, recall, recognition]
---
网格最短路的边权 {{c1::非负但可能大于 1}} 时，选择 Dijkstra；不是普通 BFS。

当网格移动代价非负但不再局限于 0 或 1 时，把格子或扩展状态当作图顶点，用最小堆持续取出当前距离最小的未定状态并松弛邻边。

**Evidence**

四、网格图 Dijkstra

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.04%20-%20%E7%BD%91%E6%A0%BC%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF)
