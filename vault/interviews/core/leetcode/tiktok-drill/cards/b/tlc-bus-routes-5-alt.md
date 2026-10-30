---
id: tlc-bus-routes-5-alt
node: b.bus-routes
type: qa
step: 5
---
## Q
**LC 815 公交路线**｜另一种解法

把“上车”建模成代价 `1` 的边、“下车”建模成代价 `0` 的边，用 0-1 BFS 怎么写？什么时候这样建模更有用？

## A
**建模。** 图有两类结点：车站和线路。`车站 -> 经过它的线路`：代价 `1`（上车，多乘一辆）；`线路 -> 它上面的车站`：代价 `0`（下车）。从 `source` 到 `target` 的最短距离就是答案。边权只有 `0` 和 `1`，用双端队列：代价 `0` 的边把结点放到队首，代价 `1` 的放队尾。

```python
from collections import defaultdict, deque


def num_buses_01bfs(routes: list[list[int]], source: int, target: int) -> int:
    if source == target:
        return 0
    stop_routes: defaultdict[int, list[int]] = defaultdict(list)
    for r, stops in enumerate(routes):
        for stop in stops:
            stop_routes[stop].append(r)
    INF = float('inf')
    dist_stop: dict[int, int] = {source: 0}
    dist_route = [INF] * len(routes)
    dq: deque[tuple[str, int]] = deque([('stop', source)])
    while dq:
        kind, x = dq.popleft()
        if kind == 'stop':
            if x == target:
                return dist_stop[x]
            for r in stop_routes.get(x, ()):
                if dist_stop[x] + 1 < dist_route[r]:      # 上车：代价 1
                    dist_route[r] = dist_stop[x] + 1
                    dq.append(('route', r))
        else:
            for stop in routes[x]:
                if dist_route[x] < dist_stop.get(stop, INF):   # 下车：代价 0，放队首
                    dist_stop[stop] = dist_route[x]
                    dq.appendleft(('stop', stop))
    return -1
```

输出与主解一致：示例 1 → `2`，示例 2 → `-1`。

**取舍。**
- 主解（按层 BFS）：只有一种队列元素，代码短，复杂度 `O(S)`，是标准答案。
- 0-1 BFS：模型更通用——一旦上车代价不再是 `1`（比如票价不同、换乘要等待），就把 `1` 换成权重，0-1 BFS 变成 Dijkstra，结构不变。面试官追问“带权”时，这个建模能直接延伸。
- 实现上 0-1 BFS 的状态更多（站和线路两类结点、两张距离表），写起来更容易出错；没有带权需求时不必选它。
