---
id: leetcode-c-endlesscheng-01luak-graph-euler-path-hierholzer-template
node: graphs-traversal.graph-euler-path-hierholzer
type: cloze
anki: 1787272410604
tags: [concept-cloze, leetcode, recall, template]
---
Hierholzer 算法必须用 {{c1::边的唯一 id}}（而不是节点）来标记是否已经使用，否则重边会被错误处理。

```
def solve(n: int, edges: list[tuple[int, int]]) -> list[int]:
    # undirected multigraph; edges given as (u, v) pairs
    g = [[] for _ in range(n)]
    used = [False] * len(edges)
    for i, (u, v) in enumerate(edges):
        g[u].append((v, i))
        g[v].append((u, i))

    start = 0
    for i in range(n):
        if g[i]:
            start = i
            break

    ptr = [0] * n
    stack = [start]
    path = []
    while stack:
        x = stack[-1]
        while ptr[x] < len(g[x]) and used[g[x][ptr[x]][1]]:
            ptr[x] += 1
        if ptr[x] == len(g[x]):
            path.append(stack.pop())
        else:
            y, eid = g[x][ptr[x]]
            used[eid] = True
            stack.append(y)

    path.reverse()
    return path
```

**Evidence**

五、欧拉路径/欧拉回路

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.10%20-%20%E6%AC%A7%E6%8B%89%E8%B7%AF%E5%BE%84-%E6%AC%A7%E6%8B%89%E5%9B%9E%E8%B7%AF%EF%BC%9AHierholzer%20%E7%AE%97%E6%B3%95)
