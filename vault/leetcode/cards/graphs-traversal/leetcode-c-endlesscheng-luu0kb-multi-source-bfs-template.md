---
id: leetcode-c-endlesscheng-luu0kb-multi-source-bfs-template
node: graphs-traversal.multi-source-bfs
type: cloze
anki: 1787272459579
tags: [concept-cloze, leetcode, recall, template]
---
多源 BFS 的初始化是把所有源点 distance 设为 {{c1::0}} 并全部入队。

```
from collections import deque

def nearest_source(graph, sources):
    n = len(graph)
    dist = [-1] * n
    queue = deque()
    for source in sources:
        dist[source] = 0
        queue.append(source)
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if dist[nxt] == -1:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist
```

**Evidence**

三、图论：多源 BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.13%20-%20%E5%A4%9A%E6%BA%90%20BFS)
