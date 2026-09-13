---
id: leetcode-c-endlesscheng-k0n2go-tree-prune-by-returning-root-invariant
node: trees.tree-prune-by-returning-root
type: cloze
anki: 1787272442004
tags: [concept-cloze, invariant, leetcode, recall]
---
剪枝递归中必须执行 node.left = dfs(node.left)，以维持 {{c1::父节点连接已处理子树}}。

右子树同理。

**Evidence**

§2.4 自底向上 DFS：删点

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F11.07%20-%20%E9%80%92%E5%BD%92%E5%88%A0%E7%82%B9%E4%B8%8E%E5%AD%90%E6%A0%91%E5%89%AA%E6%9E%9D)
