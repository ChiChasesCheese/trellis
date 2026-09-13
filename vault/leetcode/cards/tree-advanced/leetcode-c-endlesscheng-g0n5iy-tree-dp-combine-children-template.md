---
id: leetcode-c-endlesscheng-g0n5iy-tree-dp-combine-children-template
node: tree-advanced.tree-dp-combine-children
type: cloze
anki: 1787272479078
tags: [concept-cloze, leetcode, recall, template]
---
无向树递归遍历子节点时必须跳过 {{c1::parent}}。

```
def tree_diameter(graph):
    best = 0
    def dfs(node, parent):
        nonlocal best
        top1 = 0
        top2 = 0
        for nxt in graph[node]:
            if nxt == parent:
                continue
            length = dfs(nxt, node) + 1
            if length > top1:
                top1, top2 = length, top1
            elif length > top2:
                top2 = length
        best = max(best, top1 + top2)
        return top1
    dfs(0, -1)
    return best
```

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.11%20-%20%E6%A0%91%E5%BD%A2%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
