---
id: leetcode-c-endlesscheng-01luak-graph-dijkstra-shortest-path-invariant
node: shortest-path-uf-flow.graph-dijkstra-shortest-path
type: cloze
anki: 1787272409603
tags: [concept-cloze, invariant, leetcode, recall]
---
Dijkstra 正确性的核心不变量是：节点 x 第一次从堆中弹出时，dis[x] 就是{{c1::最终最短路}}，之后不会再被更新更小。

每个节点第一次从堆中弹出时，其 dis 值就是最终最短路（贪心选择性质）；堆中可能存在同一节点的多条过期记录，用 dis_x > dis[x] 判断并跳过

**Evidence**

§3.1 单源最短路：Dijkstra 算法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.07%20-%20%E5%8D%95%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%9ADijkstra%20%E7%AE%97%E6%B3%95)
