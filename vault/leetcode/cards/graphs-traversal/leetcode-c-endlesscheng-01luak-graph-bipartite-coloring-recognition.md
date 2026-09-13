---
id: leetcode-c-endlesscheng-01luak-graph-bipartite-coloring-recognition
node: graphs-traversal.graph-bipartite-coloring
type: cloze
anki: 1787272411007
tags: [concept-cloze, leetcode, recall, recognition]
---
需要判断一张图能否被划分成两个互不相邻的集合时，应使用{{c1::二分图染色}}（交替染色法）。

用 DFS/BFS 对图交替染两种颜色，相邻节点必须染不同颜色；若染色过程中发现某条边的两端颜色相同，则该图不是二分图。

**Evidence**

七、二分图染色

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.12%20-%20%E4%BA%8C%E5%88%86%E5%9B%BE%E6%9F%93%E8%89%B2%EF%BC%88%E4%BA%A4%E6%9B%BF%E6%9F%93%E8%89%B2%E6%B3%95%EF%BC%89)
