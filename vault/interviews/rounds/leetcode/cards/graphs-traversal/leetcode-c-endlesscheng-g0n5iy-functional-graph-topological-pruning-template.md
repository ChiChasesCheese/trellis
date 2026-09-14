---
id: leetcode-c-endlesscheng-g0n5iy-functional-graph-topological-pruning-template
node: graphs-traversal.functional-graph-topological-pruning
type: cloze
anki: 1787272481480
tags: [concept-cloze, leetcode, recall, template]
---
初始化剥离队列时加入所有 {{c1::indegree == 0}} 的节点。

```
from collections import deque

def cycle_nodes(nxt):
    n = len(nxt)
    indegree = [0] * n
    for v in nxt:
        indegree[v] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    while queue:
        u = queue.popleft()
        v = nxt[u]
        indegree[v] -= 1
        if indegree[v] == 0:
            queue.append(v)
    return [i for i, d in enumerate(indegree) if d > 0]
```

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.19%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91%E6%8B%93%E6%89%91%E5%89%A5%E7%A6%BB)
