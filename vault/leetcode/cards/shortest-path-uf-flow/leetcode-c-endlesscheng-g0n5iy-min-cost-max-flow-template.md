---
id: leetcode-c-endlesscheng-g0n5iy-min-cost-max-flow-template
node: shortest-path-uf-flow.min-cost-max-flow
type: cloze
anki: 1787272482080
tags: [concept-cloze, leetcode, recall, template]
---
残量网络必须为每条正向边保留一条 {{c1::反向边}}，用于撤销已有流。

```
import heapq

def shortest_path(graph, start):
    dist = [float('inf')] * len(graph)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, cost in graph[u]:
            nd = d + cost
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.21%20-%20%E6%9C%80%E5%B0%8F%E8%B4%B9%E7%94%A8%E6%9C%80%E5%A4%A7%E6%B5%81)
