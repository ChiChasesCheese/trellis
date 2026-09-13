---
id: leetcode-c-endlesscheng-01luak-graph-topological-order-dp-template
node: graphs-traversal.graph-topological-order-dp
type: cloze
anki: 1787272409106
tags: [concept-cloze, leetcode, recall, template]
---
刷表法在拓扑排序过程中的核心操作是，当访问到节点 x 的邻居 y 时，用 {{c1::dp[x]}} 去更新 dp[y]，而不是等 y 出队时再拉取前驱值。

```
from collections import deque

def solve(n: int, edges: list[list[int]], init: list[int]) -> list[int]:
    g = [[] for _ in range(n)]
    in_deg = [0] * n
    for x, y in edges:
        g[x].append(y)
        in_deg[y] += 1

    dp = list(init)
    q = deque(i for i in range(n) if in_deg[i] == 0)
    while q:
        x = q.popleft()
        for y in g[x]:
            # push x's contribution to y (this is the "push-style" DP step)
            dp[y] = max(dp[y], dp[x] + 1)
            in_deg[y] -= 1
            if in_deg[y] == 0:
                q.append(y)
    return dp
```

**Evidence**

§2.2 在拓扑序上 DP

[原文 ↗](obsidian://open?vault=lc&amp;file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.05%20-%20%E6%8B%93%E6%89%91%E5%BA%8F%E4%B8%8A%20DP%EF%BC%88%E5%88%B7%E8%A1%A8%E6%B3%95%EF%BC%89)
