---
id: tlc-patterns-shortest-path-2-template
node: patterns.shortest-path
type: qa
step: 2
---
## Q
**最短路（Shortest Path）｜模板：Dijkstra（最小堆 + 过期记录）**

写出 Dijkstra 的标准实现，说明为什么弹出时要检查 `d > dist[u]`。

## A
```python
import heapq
import math
def dijkstra(n: int, edges: list[tuple[int, int, int]], src: int) -> list[float]:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [math.inf] * n
    dist[src] = 0
    h = [(0, src)]                         # (到源点的距离, 节点)
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue                       # 过期记录：u 已被更短的路径处理过
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(h, (nd, v))  # 不删旧记录，留给上面的检查跳过
    return dist
```

运行：`dijkstra(4, [(0,1,2),(0,2,5),(1,2,1),(2,3,1)], 0)` → `[0, 2, 3, 4]`；`dijkstra(3, [(0,1,1)], 0)` → `[0, 1, inf]`（`2` 不可达）。时间 `O((V + E) log V)`，空间 `O(V + E)`。

- `heapq` 不支持改键，所以同一个点会多次入堆（懒删除）。弹出时若 `d > dist[u]`，说明堆里这条是旧的、更长的路径，直接跳过。
- 跳过检查的作用是效率：在一个 `60` 个点、每个点连向所有后继点的图上，不检查要展开 `1771` 次，检查后只展开 `60` 次，答案相同。
- 想要路径本身：再开 `prev[v] = u`，在更新 `dist[v]` 时记录，最后回溯。
- 只求到某个目标的距离：弹出目标节点时就可以返回。
- 堆元素是 `(距离, 节点)` 元组，距离相同时比较节点编号，都是整数，不会出现不可比较的问题。
