---
id: leetcode-c-endlesscheng-luu0kb-tree-dp-and-rerooting-template
node: tree-advanced.tree-dp-and-rerooting
type: cloze
anki: 1787272458380
tags: [concept-cloze, leetcode, recall, template]
---
无递归树形 DP 常先建立 parent 与遍历 order，再按 {{c1::reversed(order)}} 做后序汇总。

```
def subtree_sizes(graph, root=0):
    n = len(graph)
    parent = [-1] * n
    order = [root]
    for node in order:
        for nxt in graph[node]:
            if nxt != parent[node]:
                parent[nxt] = node
                order.append(nxt)
    size = [1] * n
    for node in reversed(order):
        if parent[node] != -1:
            size[parent[node]] += size[node]
    return size
```

**Evidence**

二、动态规划：树形 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.09%20-%20%E6%A0%91%E5%BD%A2%20DP%20%E4%B8%8E%E6%8D%A2%E6%A0%B9%20DP)
