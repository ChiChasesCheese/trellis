---
id: leetcode-c-endlesscheng-01luak-graph-floyd-warshall-recognition
node: shortest-path-uf-flow.graph-floyd-warshall
type: cloze
anki: 1787272409804
tags: [concept-cloze, leetcode, recall, recognition]
---
需要一次性求出任意两点间最短路（全源最短路），且节点数不大时，应使用 {{c1::Floyd}} 算法。

本质是三维 DP：f[k][i][j] 表示只允许经过前 k 个中转点时 i 到 j 的最短路，通过空间优化滚动掉第一维得到经典的三重循环写法；允许负权边，但结果中若存在 f[i][i] < 0 说明有负环。

**Evidence**

§3.2 全源最短路：Floyd 算法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.08%20-%20%E5%85%A8%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%9AFloyd%20%E7%AE%97%E6%B3%95)
