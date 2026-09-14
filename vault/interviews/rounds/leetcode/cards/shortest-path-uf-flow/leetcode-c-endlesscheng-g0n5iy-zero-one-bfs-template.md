---
id: leetcode-c-endlesscheng-g0n5iy-zero-one-bfs-template
node: shortest-path-uf-flow.zero-one-bfs
type: cloze
anki: 1787272482980
tags: [concept-cloze, leetcode, recall, template]
---
0-1 BFS 的分支是 w == 0 时 {{c1::queue.appendleft(v)}}，否则 append(v)。

```
from collections import deque

def zero_one_bfs(graph, start):
    dist = [float('inf')] * len(graph)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    queue.appendleft(v)
                else:
                    queue.append(v)
    return dist
```

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.24%20-%20%E5%9B%BE%E8%AE%BA%EF%BC%9A0-1%20BFS)
