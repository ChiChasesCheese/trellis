---
id: leetcode-c-endlesscheng-01luak-graph-mst-kruskal-recognition
node: shortest-path-uf-flow.graph-mst-kruskal
type: cloze
anki: 1787272410104
tags: [concept-cloze, leetcode, recall, recognition]
---
求连通所有节点的最小总边权（最小生成树），且图比较稀疏时，优先使用 {{c1::Kruskal}} 算法。

把所有边按权值从小到大排序，用并查集贪心地依次加入不会形成环的边，直到连通所有节点；若最终连通块数大于 1，说明原图不连通，无生成树。适合稀疏图；稠密图更适合 Prim。

**Evidence**

四、最小生成树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.09%20-%20%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91%EF%BC%9AKruskal%20%E7%AE%97%E6%B3%95)
