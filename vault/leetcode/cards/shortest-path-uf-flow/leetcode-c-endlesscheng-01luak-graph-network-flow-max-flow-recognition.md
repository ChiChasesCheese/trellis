---
id: leetcode-c-endlesscheng-01luak-graph-network-flow-max-flow-recognition
node: shortest-path-uf-flow.graph-network-flow-max-flow
type: cloze
anki: 1787272411304
tags: [concept-cloze, leetcode, recall, recognition]
---
当问题可以抽象成源点到汇点在容量限制下的最大可行流量时，应考虑用 {{c1::网络流（最大流）}} 建模。

在残量网络上反复用 BFS 寻找从源点到汇点的增广路径，沿路径推送等于路径最小残余容量的流量，并同步更新正反向边的残余容量，直到找不到增广路为止，累计流量即为最大流。

**Evidence**

八、网络流

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.13%20-%20%E7%BD%91%E7%BB%9C%E6%B5%81%EF%BC%9A%E6%9C%80%E5%A4%A7%E6%B5%81%EF%BC%88Edmonds-Karp%20%E5%A2%9E%E5%B9%BF%E8%B7%AF%EF%BC%89)
