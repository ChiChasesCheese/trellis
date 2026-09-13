---
id: leetcode-c-endlesscheng-01luak-graph-topological-sort-kahn-template
node: graphs-traversal.graph-topological-sort-kahn
type: cloze
anki: 1787272408803
tags: [concept-cloze, leetcode, recall, template]
---
Kahn 算法结束后判断图中是否有环的方法是检查 {{c1::len(order) < n}}。

```
from collections import deque

# returns [] if the graph has a cycle
def solve(n: int, edges: list[list[int]]) -> list[int]:
    g = [[] for _ in range(n)]
    in_deg = [0] * n
    for x, y in edges:
        g[x].append(y)
        in_deg[y] += 1

    order = []
    q = deque(i for i in range(n) if in_deg[i] == 0)
    while q:
        x = q.popleft()
        order.append(x)
        for y in g[x]:
            in_deg[y] -= 1
            if in_deg[y] == 0:
                q.append(y)

    if len(order) < n:
        return []
    return order
```

**Evidence**

§2.1 拓扑排序模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.04%20-%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%EF%BC%88Kahn%20%E7%AE%97%E6%B3%95%EF%BC%89)
