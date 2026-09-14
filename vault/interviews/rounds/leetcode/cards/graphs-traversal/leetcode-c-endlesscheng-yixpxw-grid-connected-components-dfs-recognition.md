---
id: leetcode-c-endlesscheng-yixpxw-grid-connected-components-dfs-recognition
node: graphs-traversal.grid-connected-components-dfs
type: cloze
anki: 1787272404105
tags: [concept-cloze, leetcode, recall, recognition]
---
网格题要求统计岛屿、区域或房间的数量/面积，且只沿相邻可通行格移动时，优先考虑 {{c1::从每个未访问格启动一次 DFS 枚举连通块}}。

把可通行格子视为顶点、上下左右相邻视为边；从每个未访问格子出发进行 DFS，即可枚举连通块并统计其大小。

**Evidence**

一、网格图 DFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.01%20-%20%E7%BD%91%E6%A0%BC%E8%BF%9E%E9%80%9A%E5%9D%97%20DFS)
