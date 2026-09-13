---
id: leetcode-c-endlesscheng-g0n5iy-graph-dfs-state-and-timestamps-template
node: graphs-traversal.graph-dfs-state-and-timestamps
type: cloze
anki: 1787272482680
tags: [concept-cloze, leetcode, recall, template]
---
DFS 进入节点时先记录 {{c1::tin[u] = timer}}，退出时记录 tout[u]。

```
def timestamps(graph, root):
    tin = [0] * len(graph)
    tout = [0] * len(graph)
    timer = 0
    def dfs(u, parent):
        nonlocal timer
        tin[u] = timer
        timer += 1
        for v in graph[u]:
            if v != parent:
                dfs(v, u)
        tout[u] = timer
    dfs(root, -1)
    return tin, tout
```

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.23%20-%20DFS%20%E7%8A%B6%E6%80%81%E4%B8%8E%E6%97%B6%E9%97%B4%E6%88%B3)
