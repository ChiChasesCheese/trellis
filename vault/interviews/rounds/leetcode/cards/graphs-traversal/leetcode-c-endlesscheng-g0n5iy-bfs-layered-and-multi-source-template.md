---
id: leetcode-c-endlesscheng-g0n5iy-bfs-layered-and-multi-source-template
node: graphs-traversal.bfs-layered-and-multi-source
type: cloze
anki: 1787272481779
tags: [concept-cloze, leetcode, recall, template]
---
多源 BFS 初始化时，每个源点都设为 {{c1::dist[s] = 0}} 并入队。

```
from collections import deque

def nearest_source(graph, sources):
    dist = [-1] * len(graph)
    queue = deque()
    for s in sources:
        dist[s] = 0
        queue.append(s)
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist
```

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.20%20-%20%E5%88%86%E5%B1%82%E4%B8%8E%E5%A4%9A%E6%BA%90%20BFS)
