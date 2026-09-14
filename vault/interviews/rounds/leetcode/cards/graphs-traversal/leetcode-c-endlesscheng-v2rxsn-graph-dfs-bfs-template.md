---
id: leetcode-c-endlesscheng-v2rxsn-graph-dfs-bfs-template
node: graphs-traversal.graph-dfs-bfs
type: cloze
anki: 1787272466179
tags: [concept-cloze, leetcode, recall, template]
---
BFS 用 {{c1::deque}}，从左侧 popleft 并把未访问邻居 append。

```
from collections import deque

def bfs(graph, start):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return dist
```

**Evidence**

三、图论：BFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.12%20-%20DFS%20%E4%B8%8E%20BFS%20%E5%9B%BE%E9%81%8D%E5%8E%86)
