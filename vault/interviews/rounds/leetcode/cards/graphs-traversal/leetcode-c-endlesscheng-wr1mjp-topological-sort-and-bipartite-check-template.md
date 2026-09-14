---
id: leetcode-c-endlesscheng-wr1mjp-topological-sort-and-bipartite-check-template
node: graphs-traversal.topological-sort-and-bipartite-check
type: cloze
anki: 1787272474580
tags: [concept-cloze, leetcode, recall, template]
---
若拓扑排序结束后 order 长度小于 n，说明图中存在 {{c1::有向环}}。

```
from collections import deque

def topological_order(n, edges):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for a, b in edges:
        graph[a].append(b)
        indegree[b] += 1
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

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.17%20-%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%E4%B8%8E%E4%BA%8C%E5%88%86%E5%9B%BE%E5%88%A4%E5%AE%9A)
