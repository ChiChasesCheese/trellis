---
id: tlc-bus-routes-2-code
node: a.bus-routes
type: qa
step: 2
---
## Q
**LC 815 公交路线**｜写出 Python 实现

`routes`（`1..500` 条线路，每条 `1..10^5` 个互不相同的车站，总长 `<= 10^5`，编号 `< 10^6`），`source`、`target`（`< 10^6`）。你从 `source` 出发，一开始不在车上，只能乘公交。返回到达 `target` 最少乘坐的公交车数量，到不了返回 `-1`。

## A
**思路。** 建「车站 → 经过它的线路」反查表。BFS 以车站为队列元素，每一层表示再乘一辆车；取出一个车站，把经过它且没展开过的线路展开：这条线路上所有没到过的车站入队，碰到 `target` 就返回当前层数。

```python
from collections import defaultdict, deque


def num_buses_to_destination(routes: list[list[int]], source: int, target: int) -> int:
    if source == target:
        return 0
    stop_routes: defaultdict[int, list[int]] = defaultdict(list)   # 站 -> 经过它的线路
    for r, stops in enumerate(routes):
        for stop in stops:
            stop_routes[stop].append(r)
    seen_stops = {source}
    seen_routes: set[int] = set()
    queue = deque([source])
    buses = 0
    while queue:
        buses += 1                             # 这一层的所有站，都再多乘一辆车能到的站
        for _ in range(len(queue)):
            stop = queue.popleft()
            for r in stop_routes.get(stop, ()):
                if r in seen_routes:           # 线路只展开一次，总工作量 O(sum(len))
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

运行：示例 1 → `2`，示例 2 → `-1`，`([[1,2]], 5, 5)` → `0`，`([[1,2]], 1, 9)` → `-1`，`([[1,2,3,4,5]], 1, 5)` → `1`。

**复杂度。** 时间 `O(S)`，`S = sum(len(routes[i]))`：建表一遍，每条线路展开一次；空间 `O(S)`。

**写法要点。** `defaultdict(list)` 建反查表；读取时用 `.get(stop, ())` 而不是 `[stop]`，因为 `defaultdict` 的下标访问会悄悄插入空键，污染字典。`for _ in range(len(queue))` 按层处理，层数就是答案，不用在队列里存距离。`target` 在展开线路时才检查，省掉一次出队。`seen_routes` 是复杂度的关键：去掉它，同一条线路会被反复扫描。
