---
id: tlc-bus-routes-0-whole
node: b.bus-routes
type: qa
---
## Q
**LC 815 公交路线**｜Hard · LC TikTok 热度 62/100

给数组 `routes`，`routes[i]` 是第 `i` 条公交线路经过的车站序列，这辆公交车在这条线路上循环往复地行驶（比如 `[1, 5, 7]` 表示 `1 -> 5 -> 7 -> 1 -> 5 -> ...`）。你从车站 `source` 出发（一开始不在车上），要去车站 `target`，期间只能乘坐公交车。求最少需要乘坐的公交车数量，到不了返回 `-1`。`1 <= routes.length <= 500`，`1 <= routes[i].length <= 10^5`，`routes[i]` 中的车站互不相同，`sum(routes[i].length) <= 10^5`，`0 <= routes[i][j] < 10^6`，`0 <= source, target < 10^6`。例：`routes = [[1,2,7],[3,6,7]]`，`source = 1`，`target = 6` → `2`（先乘第一辆到 `7`，再换第二辆到 `6`）；`routes = [[7,12],[4,5,15],[6],[15,19],[9,12,13]]`，`source = 15`，`target = 12` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 求的是「乘车次数」而不是「经过站数」，所以按**换乘次数**做广度优先搜索（BFS）：每一层表示“再多乘一辆车”所能到达的所有车站；用字典 `stop_routes` 反查「某个车站有哪些线路经过」，每条线路只展开一次。`O(sum(len))`。

**识别。** 「最少次数」「每次操作代价相同」是 BFS 的信号；关键是选对图：结点不是车站，边的代价也不是一站。同一条线路上的任意两站，乘一辆车就能到，代价都是 `1`。线路总长 `10^5`、车站编号到 `10^6`：不能开 `10^6` 的邻接矩阵，要用字典；也不能把一条线路的所有车站两两连边（`10^10`）。所以让每条线路只被展开一次。

**推导。** 暴力：以车站为结点，相邻两站连边做 BFS，答案是“经过的站数”，不对——一辆车可以连续坐很多站，只算一次。改成“同一条线路上任意两站都连边”，边数达到 `L^2`，线路长 `10^5` 时放不下。浪费：同一条线路被不同的起点站反复展开，每次都扫一遍这条线路的全部车站。洞察：线路才是代价单位——只要某条线路被乘过，它上面所有车站都在“乘这一辆车”能到的范围里，所以每条线路只需要展开一次，之后再碰到它直接跳过。于是 BFS 里同时记录已访问的车站和已展开的线路，总工作量是 `sum(len(route))`。

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

运行：示例 1 → `2`，示例 2 → `-1`，`([[1,2]], 5, 5)` → `0`，`([[1,2]], 1, 9)` → `-1`，`([[1,2,3,4,5]], 1, 5)` → `1`；`500` 条线路、每条 `201` 个站（含一个公共换乘站）→ `1`，约 `6 ms`。

**复杂度。** 时间 `O(S)`，`S = sum(len(routes[i])) <= 10^5`（建反查表一遍，每条线路展开一次）；空间 `O(S)`：反查表、访问集合和队列。

**易错点。**
- 忘了 `source == target` 直接返回 `0`：`([[1,2]], 1, 1)` 会在展开线路时看到 `nxt == target`，返回 `1`，正确是 `0`（不用乘车）。
- 只标记车站、不标记线路：同一条线路会被它上面每个已到达的车站各展开一次。两条线路各含同样的 `5000` 个站时，内层循环要执行 `50000000` 次，加上线路标记只要 `10000` 次。
- 把答案算成站数：`[[1,2,3,4,5]]` 从 `1` 到 `5` 如果只在相邻站之间连边并按边数计，得到 `4`，正确是 `1`（乘一辆车坐到底）。

**追问。**
- 双向 BFS：同时从 `source` 和 `target` 出发，在中间相遇，线路很多时搜索量更小。
- 把线路当结点：线路之间共享车站就连边，再 BFS 层数 + 1；边数最坏 `R^2 = 250000`，`R <= 500` 可接受。
- 每次换乘有额外代价（等车时间不同）：不再是无权 BFS，改用 Dijkstra。

**同模式。** LC 127 单词接龙、LC 752 打开转盘锁、LC 1129 颜色交替的最短路径、LC 1091 二进制矩阵中的最短路径、LC 787 K 站中转内最便宜的航班。
