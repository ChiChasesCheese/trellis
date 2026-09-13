---
id: leetcode-c-endlesscheng-01luak-graph-network-flow-max-flow-invariant
node: shortest-path-uf-flow.graph-network-flow-max-flow
type: cloze
anki: 1787272411405
tags: [concept-cloze, invariant, leetcode, recall]
---
网络流增广路算法的核心不变量由{{c1::最大流最小割定理}}保证：当残量网络中不再存在从源到汇的路径时，当前累计流量就是最大流。

每次增广后，路径上瓶颈边的残余容量归零，反向边的残余容量增加相应流量（保证可撤销）；算法终止时，残量网络中不存在从源点到汇点的路径，此时累计流量即为最大流（最大流最小割定理）

**Evidence**

八、网络流

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.13%20-%20%E7%BD%91%E7%BB%9C%E6%B5%81%EF%BC%9A%E6%9C%80%E5%A4%A7%E6%B5%81%EF%BC%88Edmonds-Karp%20%E5%A2%9E%E5%B9%BF%E8%B7%AF%EF%BC%89)
