---
id: leetcode-q-find-if-path-exists-in-graph-pattern
node: graphs-traversal.graph-theory
type: qa
anki: 1787102261731
tags: [lc::1971, leetcode, pattern, recall]
---
## Q
如何判断无向图中两个节点 source 和 destination 是否连通？

## A
用邻接表建图（每条无向边正反各加一次），从 source 出发做 DFS/BFS，用 visited 集合去重防止死循环，遍历中一旦碰到 destination 就返回 True；遍历结束仍未碰到则返回 False。

**Evidence**

```
g = [[] for _ in range(n)]
for a, b in edges:
    g[a].append(b)
    g[b].append(a)
visited = set()

def dfs(node: int) -> bool:
    if node == destination:
        return True
    visited.add(node)
    return any(dfs(nxt) for nxt in g[node] if nxt not in visited)

return dfs(source)
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1971%20-%20Find%20if%20Path%20Exists%20in%20Graph)
