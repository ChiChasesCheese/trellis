---
id: leetcode-c-endlesscheng-01luak-graph-network-flow-max-flow-template
node: shortest-path-uf-flow.graph-network-flow-max-flow
type: cloze
anki: 1787272411505
tags: [concept-cloze, leetcode, recall, template]
---
Edmonds-Karp 每次找到增广路后，除了减少正向边残余容量，还必须{{c1::增加反向边的残余容量}}以支持流量撤销。

```
from collections import deque

def solve(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    # build residual graph: graph[u][v] = residual capacity from u to v
    graph = [dict() for _ in range(n)]
    for u, v, cap in edges:
        graph[u][v] = graph[u].get(v, 0) + cap
        graph[v].setdefault(u, 0)

    max_flow = 0
    while True:
        parent = [-1] * n
        parent[s] = s
        q = deque([s])
        while q:
            x = q.popleft()
            for y, cap in graph[x].items():
                if cap > 0 and parent[y] == -1:
                    parent[y] = x
                    q.append(y)
        if parent[t] == -1:
            break  # no augmenting path found

        path_flow = float('inf')
        y = t
        while y != s:
            x = parent[y]
            path_flow = min(path_flow, graph[x][y])
            y = x

        y = t
        while y != s:
            x = parent[y]
            graph[x][y] -= path_flow
            graph[y][x] += path_flow
            y = x

        max_flow += path_flow

    return max_flow
```

**Evidence**

八、网络流

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.13%20-%20%E7%BD%91%E7%BB%9C%E6%B5%81%EF%BC%9A%E6%9C%80%E5%A4%A7%E6%B5%81%EF%BC%88Edmonds-Karp%20%E5%A2%9E%E5%B9%BF%E8%B7%AF%EF%BC%89)
