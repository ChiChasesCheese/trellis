---
slug: bus-routes
---
## Q
**LC 815 公交路线**｜Hard

`routes[i]` 是第 `i` 条循环公交线路经过的站。从站 `source` 出发到站 `target`，求最少乘几辆公交，到不了返回 `-1`。

## A
**一句话。** 按乘车次数做 BFS，每层多乘一辆车；用「站到线路」的反查表，每条线路只展开一次。

```python
def num_buses_to_destination(routes, source, target):
    if source == target:
        return 0
    stop_routes = defaultdict(list)   # 站 -> 经过它的线路
    for r, stops in enumerate(routes):
        for stop in stops:
            stop_routes[stop].append(r)
    seen_stops, seen_routes = {source}, set()
    queue = deque([source])
    buses = 0
    while queue:
        buses += 1                    # 这一层多乘一辆车
        for _ in range(len(queue)):
            stop = queue.popleft()
            for r in stop_routes[stop]:
                if r in seen_routes:
                    continue
                seen_routes.add(r)
                for nxt in routes[r]:
                    if nxt == target:
                        return buses
                    if nxt not in seen_stops:
                        seen_stops.add(nxt)
                        queue.append(nxt)
    return -1
```

**复杂度。** 时间 `O(S)`，空间 `O(S)`（`S` 为所有线路站数之和）。

**易错点。**
- 漏掉 `source == target`：`([[1,2]], 1, 1)` 会返回 `1`，应为 `0`。
- 只标记站、不标记线路：同一条线路被其上每个站各展开一次，会超时。
- 把答案当站数：`[[1,2,3,4,5]]` 从 `1` 到 `5` 应为 `1`，不是 `4`。

**追问。**
- 换乘有不同代价？：不再是无权图，改用 Dijkstra。
- 如何加速搜索？：双向 BFS，从 `source` 和 `target` 同时出发，中间相遇。

**同模式。** LC 127 单词接龙、LC 752 打开转盘锁、LC 1091 二进制矩阵中的最短路径、LC 787 K 站中转内最便宜的航班
