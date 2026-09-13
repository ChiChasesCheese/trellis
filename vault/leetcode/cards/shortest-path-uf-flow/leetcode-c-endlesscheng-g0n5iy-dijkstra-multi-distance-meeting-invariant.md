---
id: leetcode-c-endlesscheng-g0n5iy-dijkstra-multi-distance-meeting-invariant
node: shortest-path-uf-flow.dijkstra-multi-distance-meeting
type: cloze
anki: 1787272482279
tags: [concept-cloze, invariant, leetcode, recall]
---
Dijkstra 弹出的条目 d 只有在 {{c1::d == dist[u]}} 时才是当前有效最短距离。

Dijkstra 中从堆取出的最新最小距离不会再被改善；对每个候选汇合点，所组合的每一段距离都对应独立最短路径

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.22%20-%20Dijkstra%20%E5%A4%9A%E6%BA%90%E8%B7%9D%E7%A6%BB%E7%BB%84%E5%90%88)
