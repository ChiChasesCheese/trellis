---
id: leetcode-c-endlesscheng-01luak-graph-mst-kruskal-invariant
node: shortest-path-uf-flow.graph-mst-kruskal
type: cloze
anki: 1787272410204
tags: [concept-cloze, invariant, leetcode, recall]
---
Kruskal 算法依赖并查集保证每次加入的边{{c1::不会形成环}}，从而始终维持一棵森林直到合并为一棵树。

并查集保证不会加入形成环的边（贪心 + 无环性）；按边权从小到大处理时，每次成功合并的边一定是当前局部最优选择（贪心的正确性由割性质保证）

**Evidence**

四、最小生成树

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.09%20-%20%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91%EF%BC%9AKruskal%20%E7%AE%97%E6%B3%95)
