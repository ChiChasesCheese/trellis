---
id: leetcode-c-endlesscheng-g0n5iy-graph-dfs-state-and-timestamps-invariant
node: graphs-traversal.graph-dfs-state-and-timestamps
type: cloze
anki: 1787272482580
tags: [concept-cloze, invariant, leetcode, recall]
---
使用半开时间区间时，u 是 v 祖先的条件是 {{c1::tin[u] <= tin[v] and tout[v] <= tout[u]}}。

DFS 参数中的状态准确表示从根到当前节点的路径摘要；在树上，u 是 v 祖先当且仅当 tin[u] <= tin[v] 且 tout[v] <= tout[u]

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.23%20-%20DFS%20%E7%8A%B6%E6%80%81%E4%B8%8E%E6%97%B6%E9%97%B4%E6%88%B3)
