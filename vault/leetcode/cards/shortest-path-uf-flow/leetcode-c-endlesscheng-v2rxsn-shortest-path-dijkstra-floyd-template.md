---
id: leetcode-c-endlesscheng-v2rxsn-shortest-path-dijkstra-floyd-template
node: shortest-path-uf-flow.shortest-path-dijkstra-floyd
type: cloze
anki: 1787272466781
tags: [concept-cloze, leetcode, recall, template]
---
Dijkstra 弹出堆项后，用 {{c1::if cost != dist[node]: continue}} 跳过旧条目。

```
import heapq

def dijkstra(graph, start):
    inf = float('inf')
    dist = [inf] * len(graph)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        cost, node = heapq.heappop(heap)
        if cost != dist[node]:
            continue
        for nxt, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < dist[nxt]:
                dist[nxt] = new_cost
                heapq.heappush(heap, (new_cost, nxt))
    return dist
```

**Evidence**

三、图论：Dijkstra

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.14%20-%20Dijkstra%20%E4%B8%8E%20Floyd%20%E6%9C%80%E7%9F%AD%E8%B7%AF)
