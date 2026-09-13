---
id: leetcode-c-endlesscheng-01luak-graph-dijkstra-shortest-path-template
node: shortest-path-uf-flow.graph-dijkstra-shortest-path
type: cloze
anki: 1787272409705
tags: [concept-cloze, leetcode, recall, template]
---
Dijkstra 模板中用于跳过堆中过期数据的判断是 {{c1::dis_x > dis[x]}}。

```
import math
from heapq import heappush, heappop

# returns dis[x] = math.inf if x is unreachable; no negative edge weights allowed
def solve(n: int, edges: list[list[int]], start: int) -> list[float]:
    g = [[] for _ in range(n)]
    for x, y, wt in edges:
        g[x].append((y, wt))
        # g[y].append((x, wt))  # uncomment for undirected graph

    dis = [math.inf] * n
    dis[start] = 0
    h = [(0, start)]

    while h:
        dis_x, x = heappop(h)
        if dis_x > dis[x]:
            continue  # x was already finalized with a smaller distance
        for y, wt in g[x]:
            new_dis_y = dis_x + wt
            if new_dis_y < dis[y]:
                dis[y] = new_dis_y
                heappush(h, (new_dis_y, y))

    return dis
```

**Evidence**

§3.1 单源最短路：Dijkstra 算法模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.07%20-%20%E5%8D%95%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%9ADijkstra%20%E7%AE%97%E6%B3%95)
