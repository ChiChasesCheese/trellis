---
id: leetcode-c-endlesscheng-wr1mjp-functional-graph-cycle-and-lca-invariant
node: graphs-traversal.functional-graph-cycle-and-lca
type: cloze
anki: 1787272474780
tags: [concept-cloze, invariant, leetcode, recall]
---
函数图中节点再次出现在 {{c1::同一条当前路径}} 上时，才确定找到了环。

函数图单次走访中，time[node] 记录该节点在当前路径首次出现的步数；LCA 是两个节点共同祖先中深度最大的节点

**Evidence**

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.18%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91%E6%97%B6%E9%97%B4%E6%88%B3%E4%B8%8E%20LCA)
