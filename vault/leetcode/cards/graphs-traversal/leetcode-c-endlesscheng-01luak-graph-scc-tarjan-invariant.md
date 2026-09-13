---
id: leetcode-c-endlesscheng-01luak-graph-scc-tarjan-invariant
node: graphs-traversal.graph-scc-tarjan
type: cloze
anki: 1787272410804
tags: [concept-cloze, invariant, leetcode, recall]
---
Tarjan 算法中，当 {{c1::low[x] == dfn[x]}} 时，说明 x 是其所在强连通分量在 DFS 树中的根。

low[x] 始终等于 x 通过树边和至少一条返祖边能到达的最小 dfn 值；当且仅当 low[x] == dfn[x] 时，x 是其所在强连通分量在 DFS 树中的根，栈中从栈顶到 x 的所有节点构成该分量

**Evidence**

六、强连通分量/双连通分量

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.11%20-%20%E5%BC%BA%E8%BF%9E%E9%80%9A%E5%88%86%E9%87%8F%EF%BC%9ATarjan%20%E7%AE%97%E6%B3%95)
