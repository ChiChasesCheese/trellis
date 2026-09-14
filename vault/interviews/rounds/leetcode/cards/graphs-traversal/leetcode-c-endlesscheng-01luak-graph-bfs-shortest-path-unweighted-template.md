---
id: leetcode-c-endlesscheng-01luak-graph-bfs-shortest-path-unweighted-template
node: graphs-traversal.graph-bfs-shortest-path-unweighted
type: cloze
anki: 1787272408205
tags: [concept-cloze, leetcode, recall, template]
---
BFS 最短路模板中，判断节点 y 是否首次被访问的条件是 {{c1::dis[y] < 0}}，满足则更新 dis[y] = dis[x] + 1 并入队。

```
from collections import deque

# dis[x] = -1 means x is unreachable from start
def solve(n: int, edges: list[list[int]], start: int) -> list[int]:
    g = [[] for _ in range(n)]
    for x, y in edges:
        g[x].append(y)
        g[y].append(x)

    dis = [-1] * n
    dis[start] = 0
    q = deque([start])
    while q:
        x = q.popleft()
        for y in g[x]:
            if dis[y] < 0:
                dis[y] = dis[x] + 1
                q.append(y)
    return dis
```

**Evidence**

§1.2 广度优先搜索（BFS）模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.02%20-%20BFS%20%E6%B1%82%E5%8D%95%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%88%E6%97%A0%E6%9D%83%E5%9B%BE%EF%BC%89)
