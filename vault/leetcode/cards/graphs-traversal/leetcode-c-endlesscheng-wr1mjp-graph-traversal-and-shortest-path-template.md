---
id: leetcode-c-endlesscheng-wr1mjp-graph-traversal-and-shortest-path-template
node: graphs-traversal.graph-traversal-and-shortest-path
type: cloze
anki: 1787272474280
tags: [concept-cloze, leetcode, recall, template]
---
BFS 扩展未访问邻居时执行 {{c1::dist[nxt] = dist[node] + 1；queue.append(nxt)}}。

```
from collections import deque

def bfs_distance(graph, start):
    dist = [-1] * len(graph)
    dist[start] = 0
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if dist[nxt] == -1:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist
```

**Evidence**

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.16%20-%20DFS%E3%80%81BFS%20%E4%B8%8E%E6%9C%80%E7%9F%AD%E8%B7%AF)
