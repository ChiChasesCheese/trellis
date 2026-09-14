---
id: leetcode-q-graph-valid-tree-pattern
node: graphs-traversal.graph-theory
type: qa
anki: 1787102262057
tags: [lc::261, leetcode, pattern, recall]
---
## Q
如何判断一个无向图（n个节点，edges边表）是否构成一棵合法的树？核心不变量和步骤是什么？

## A
树的两个充要条件：①恰好 n-1 条边；②连通（无孤立分量）。做法：先判断 len(edges) != n-1 直接返回 False（边数不对，必然有环或不连通）；再建邻接表，从任意一个节点（如0）出发做 DFS/BFS（或用并查集逐条边合并），标记访问过的节点；最后检查 visited 集合大小是否等于 n，等于则说明图连通，结合边数已满足 n-1，即可判定为树。时间复杂度 O(n)。

**Evidence**

代码：`if len(edges) != n - 1: return False` 先做边数检查；随后建图 `g[a].append(b); g[b].append(a)`；从节点0开始 `dfs(0, -1)` 遍历并用 `visited` 记录访问过的节点；最终 `return len(visited) == n` 判断是否全部连通。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F261%20-%20Graph%20Valid%20Tree)
