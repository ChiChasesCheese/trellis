---
id: tlc-cheapest-flights-within-k-stops-4-followup
node: a.cheapest-flights-within-k-stops
type: qa
step: 4
---
## Q
**LC 787 K 站中转内最便宜的航班**｜追问

面试官接着问：（1）用 Dijkstra 能不能做？（2）`k` 很大（接近 `n`）时怎么省时间？（3）要返回具体路线？（4）表太大怎么办？

## A
1. **Dijkstra。** 堆元素 `(价格, 边数, 城市)`，价格小的先出；弹出终点时直接返回；边数已超限则丢弃；若该城市之前已经以「不更多的边数」弹出过（价格自然不更高），当前状态被支配，跳过：
```python
from heapq import heappop, heappush
from math import inf

def find_cheapest_dijkstra(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in flights:
        graph[u].append((v, w))
    best_stops = [inf] * n                  # 到每个城市见过的最少边数
    heap: list[tuple[int, int, int]] = [(0, 0, src)]   # (价格, 边数, 城市)
    while heap:
        cost, edges, u = heappop(heap)
        if u == dst:
            return cost
        if edges > k or edges >= best_stops[u]:
            continue                        # 边数用尽，或已有“更便宜且边数不多”的到达方式
        best_stops[u] = edges
        for v, w in graph[u]:
            heappush(heap, (cost + w, edges + 1, v))
    return -1
```
示例 1 → `700`，示例 3 → `500`。注意顺序：先判断 `u == dst` 再检查 `edges > k`，因为到达终点允许用满 `k + 1` 条边，而中途节点用了 `k + 1` 条边就不能再出发了。状态数至多 `n * (k + 1)`，每个状态按出度扩展，堆操作 `O(log)`。
2. **提前结束。** 若某一行和上一行完全相同（`dp[t] == dp[t-1]`），说明已经收敛，之后各行不会再变，直接 `break`。最多 `n - 1` 行就收敛，`k` 再大也不超过 `n - 1` 行有效。
3. **返回路线。** 松弛时同时记录前驱表 `parent[t][v] = u`，和 `dp` 同样按行保留，最后从 `parent[k+1][dst]` 沿行号逐行回溯。
4. 空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**Python 提醒**：堆元素是元组 `(价格, 边数, 城市)`，前两项相同时会比较城市编号，整数可比较，没有问题；但如果元组里放了不可比较的对象（字典、自定义类），价格相同时会抛 `TypeError`。
