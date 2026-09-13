---
id: leetcode-c-endlesscheng-yixpxw-grid-dijkstra-invariant
node: shortest-path-uf-flow.grid-dijkstra
type: cloze
anki: 1787272405105
tags: [concept-cloze, invariant, leetcode, recall]
---
Dijkstra 从最小堆弹出条目后，只有当其距离 {{c1::等于当前 distance 状态值}} 时才处理；否则它是旧条目。

从最小堆取出的、且仍等于 distance 的状态，其最短距离已确定。；每条边按 candidate = current_distance + weight 进行松弛。；堆中允许旧条目；弹出时跳过距离不匹配的条目即可。

**Evidence**

四、网格图 Dijkstra

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.04%20-%20%E7%BD%91%E6%A0%BC%20Dijkstra%20%E6%9C%80%E7%9F%AD%E8%B7%AF)
