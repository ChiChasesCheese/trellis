---
id: leetcode-c-endlesscheng-v2rxsn-tree-dp-rerooting-template
node: tree-advanced.tree-dp-rerooting
type: cloze
anki: 1787272465580
tags: [concept-cloze, leetcode, recall, template]
---
无向树 DFS 用参数 parent，并跳过 {{c1::nxt == parent}}。

```
def subtree_sizes(graph):
    n = len(graph)
    size = [0] * n
    def dfs(node, parent):
        size[node] = 1
        for nxt in graph[node]:
            if nxt != parent:
                dfs(nxt, node)
                size[node] += size[nxt]
    dfs(0, -1)
    return size
```

**Evidence**

二、动态规划：树形 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.10%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E6%8D%A2%E6%A0%B9%20DP)
