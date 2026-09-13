---
id: leetcode-c-endlesscheng-01luak-graph-scc-tarjan-recognition
node: graphs-traversal.graph-scc-tarjan
type: cloze
anki: 1787272410704
tags: [concept-cloze, leetcode, recall, recognition]
---
需要在有向图中找出所有“互相可达”的节点集合（强连通分量），标准做法是 {{c1::Tarjan}} 算法。

用一次 DFS 维护 dfn（发现时间）和 low（能追溯到的最早发现时间），配合栈记录当前搜索路径上的节点；当某节点 low == dfn 时，说明它是一个强连通分量的根，把栈中该节点及以上的所有节点弹出组成一个分量。

**Evidence**

六、强连通分量/双连通分量

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.11%20-%20%E5%BC%BA%E8%BF%9E%E9%80%9A%E5%88%86%E9%87%8F%EF%BC%9ATarjan%20%E7%AE%97%E6%B3%95)
