---
id: leetcode-c-endlesscheng-01luak-graph-bfs-state-space-modeling-recognition
node: graphs-traversal.graph-bfs-state-space-modeling
type: cloze
anki: 1787272408304
tags: [concept-cloze, leetcode, recall, recognition]
---
当问题要求“从状态 A 变到状态 B 的最少操作次数”而非显式给出图结构时，应先做 {{c1::状态到图节点}} 的建模，再跑 BFS。

把问题中的“状态”抽象成图上的节点，状态间的合法转移抽象成边，再用 BFS 求从初始状态到目标状态的最少步数；关键在于设计状态表示和转移函数。

**Evidence**

§1.3 图论建模 + BFS 最短路

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.03%20-%20%E5%9B%BE%E8%AE%BA%E5%BB%BA%E6%A8%A1%20%2B%20BFS%20%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%88%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%90%9C%E7%B4%A2%EF%BC%89)
