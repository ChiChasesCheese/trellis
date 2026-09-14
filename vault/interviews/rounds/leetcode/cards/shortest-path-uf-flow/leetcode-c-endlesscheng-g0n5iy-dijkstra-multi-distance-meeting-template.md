---
id: leetcode-c-endlesscheng-g0n5iy-dijkstra-multi-distance-meeting-template
node: shortest-path-uf-flow.dijkstra-multi-distance-meeting
type: cloze
anki: 1787272482380
tags: [concept-cloze, leetcode, recall, template]
---
加权松弛的核心判断是 {{c1::if nd < dist[v]:}}。

```
import heapq

def dijkstra(graph, start):
    dist = [float('inf')] * len(graph)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.22%20-%20Dijkstra%20%E5%A4%9A%E6%BA%90%E8%B7%9D%E7%A6%BB%E7%BB%84%E5%90%88)
