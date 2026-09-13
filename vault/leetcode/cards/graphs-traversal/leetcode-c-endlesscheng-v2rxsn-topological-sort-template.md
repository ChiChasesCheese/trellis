---
id: leetcode-c-endlesscheng-v2rxsn-topological-sort-template
node: graphs-traversal.topological-sort
type: cloze
anki: 1787272466481
tags: [concept-cloze, leetcode, recall, template]
---
最终输出长度小于节点数，说明图中存在 {{c1::环}}。

```
from collections import deque

def topo_sort(graph):
    n = len(graph)
    indegree = [0] * n
    for node in range(n):
        for nxt in graph[node]:
            indegree[nxt] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else []
```

**Evidence**

三、图论：拓扑排序

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.13%20-%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F)
