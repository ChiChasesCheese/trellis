---
id: leetcode-c-endlesscheng-mor1u6-queue-bfs-and-deque-template
node: stack-queue-monotonic.queue-bfs-and-deque
type: cloze
anki: 1789002113571
tags: [concept-cloze, leetcode, recall, template]
---
Python 的 BFS 队列应使用 {{c1::collections.deque}} 和 popleft()。

```
from collections import deque

def bfs(graph, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

**Evidence**

§4.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.07%20-%20%E9%98%9F%E5%88%97%E3%80%81BFS%20%E4%B8%8E%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97)
