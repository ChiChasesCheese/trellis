---
id: tlc-cheapest-flights-within-k-stops-0-whole
node: p2.cheapest-flights-within-k-stops
type: qa
---
## Q
**LC 787 K 站中转内最便宜的航班**｜Medium · LC TikTok 近 30 天热度 82/100（全时段 50）

有 `n` 个城市通过一些航班连接。给数组 `flights`，`flights[i] = [from_i, to_i, price_i]` 表示从城市 `from_i` 到 `to_i` 的航班，价格 `price_i`。给定出发城市 `src`、目的地 `dst` 和整数 `k`，找出一条**最多经过 `k` 站中转**的路线，使从 `src` 到 `dst` 的价格最便宜，返回该价格；不存在则返回 `-1`。`2 <= n <= 100`，`0 <= flights.length <= n * (n - 1) / 2`，`0 <= from_i, to_i < n`，`from_i != to_i`，`1 <= price_i <= 10^4`，航班没有重复，没有自环，`0 <= src, dst, k < n`，`src != dst`。例：`n = 4`，`flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`，`src = 0`，`dst = 3`，`k = 1` → `700`（`0 → 1 → 3`；`0 → 1 → 2 → 3` 更便宜但中转了 2 站，无效）；`n = 3`，`flights = [[0,1,100],[1,2,100],[0,2,500]]`，`src = 0`，`dst = 2`，`k = 1` → `200`，`k = 0` → `500`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 带步数限制的最短路：最多 `k` 站中转 = 最多 `k + 1` 趟航班。二维 DP：`dp[t][v]` 表示最多坐 `t` 趟航班、从 `src` 到城市 `v` 的最小价格，`dp[t][v] = min(dp[t-1][v], min over (u→v) dp[t-1][u] + w)`，边界 `dp[0][src] = 0`、其余为无穷，答案是 `dp[k+1][dst]`。这就是 Bellman-Ford 的「第 `t` 轮」，只是把每一轮都留在表里。`O(k * E)` 时间，`O(k * n)` 空间。

**识别。** 「最便宜」是最短路；但「最多 `k` 站」给路径加了**边数限制**，这是最短路里最容易踩坑的变体：普通 Dijkstra 只关心价格，会选出价格最低但中转太多的路线（示例 1 里不限站数是 `400`）。边数限制天然对应 DP 表的行：第 `t` 行恰好是「至多 `t` 条边」。`n <= 100`，边至多 `4950`，`k * E` 约 `5 * 10^5`，轻松通过。

**推导。** 暴力：深度优先枚举所有至多 `k + 1` 条边的路径，指数级。想要多项式解，用动态规划：状态是（边数 `t`，城市 `v`），只有 `(k + 2) * n` 个。第 `t` 行的最优路线，要么不需要第 `t` 趟航班（沿用 `dp[t-1][v]`），要么最后一趟是 `u → v`，前面是至多 `t - 1` 趟到 `u` 的最优（`dp[t-1][u] + w`），两者取小。所以一行只读上一行、写本行。

**简单解法。** 按层 BFS：第 `r` 层是「坐了 `r` 趟航班能到的城市」，只保留变便宜的到达，扩展 `k + 1` 层，答案是 `best[dst]`。

```python
from collections import defaultdict
from math import inf


def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    graph: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
    best = [inf] * n                                # best[v]：目前见过的到 v 的最低价格
    best[src] = 0
    level = [(src, 0)]                              # 当前层：(城市, 到这里的价格)
    for _ in range(k + 1):                          # 最多 k 个中转 = 最多 k + 1 趟航班
        nxt: list[tuple[int, int]] = []
        for u, cost in level:
            for v, w in graph[u]:
                if cost + w < best[v]:              # 只有更便宜才值得继续走：航班数更多且更贵的路径被占优
                    best[v] = cost + w
                    nxt.append((v, cost + w))
        level = nxt
    return -1 if best[dst] == inf else int(best[dst])
```

时间最坏 `O(k * E)`，空间 `O(n + E)`；约束内够用，也是常见的面试写法，只是「为什么可以丢掉更贵的到达」需要说清楚。

最优解：

```python
from math import inf


def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    # dp[t][v]：最多坐 t 趟航班，从 src 到城市 v 的最小价格
    dp: list[list[float]] = [[inf] * n for _ in range(k + 2)]
    dp[0][src] = 0                          # 0 趟航班：只在出发地，价格 0
    for t in range(1, k + 2):               # 最多 k 个中转 = 最多 k + 1 趟航班
        dp[t] = dp[t - 1][:]                # 少坐一趟也算（"最多 t 趟"）
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:  # 只读上一行：这一行多坐的恰好一趟
                dp[t][v] = dp[t - 1][u] + w
    return -1 if dp[k + 1][dst] == inf else int(dp[k + 1][dst])
```

运行：示例 1（`k = 1`）→ `700`；示例 2（`k = 1`）→ `200`；示例 3（`k = 0`）→ `500`；`n = 3`，`flights = [[0,1,5]]`，`src = 0`，`dst = 2`，`k = 2` → `-1`；`n = 100` 的完全图、`k = 98` 轻松跑完。

**复杂度。** 时间 `O(k * E)`，其中 `E = len(flights)`；空间 `O(k * n)`：`(k + 2) × n` 的表。

**拓展优化。**
- Dijkstra 带上航班数：堆元素 `(价格, 航班数, 城市)`；同一城市只要之前以不更多的航班数弹出过，就被占优，丢掉；第一次弹出 `dst` 就是答案：
```python
import heapq
from math import inf


def find_cheapest_price_dijkstra(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in flights:
        graph[u].append((v, w))
    fewest = [inf] * n                              # fewest[u]：已弹出的、到 u 用过的最少航班数
    heap: list[tuple[int, int, int]] = [(0, 0, src)]
    while heap:
        cost, legs, u = heapq.heappop(heap)
        if u == dst:
            return cost                             # 价格最小的合法到达最先弹出
        if legs >= fewest[u] or legs == k + 1:      # 被更便宜且航班不更多的到达占优，或已用完航班
            continue
        fewest[u] = legs
        for v, w in graph[u]:
            heapq.heappush(heap, (cost + w, legs + 1, v))
    return -1
```
- 提前结束：若某一轮松弛后 `dp[t] == dp[t-1]`，后面的行不会再变，直接 `break`；`k` 接近 `n` 时省掉大量行。

**易错点。**
- 转移读了本行：`dp[t][u] + w` 而不是 `dp[t-1][u] + w`，同一行里刚更新的值又被后面的航班读到，一行可以连坐多趟，限制失效。`flights = [[0,1,100],[1,2,100],[0,2,500]]`，`k = 0` 得到 `200`（坐了 2 趟），正确是 `500`。
- 表只开 `k + 1` 行（行号 `0..k`）：`k` 站中转对应 `k + 1` 趟航班，需要 `k + 2` 行。`k = 0` 时表里只有第 0 行，直达航班根本没填，同一组航班得到 `-1`，正确是 `500`。
- 新的一行没有从上一行复制，而是全部重新填无穷：变成「恰好坐 `t` 趟」，直达更便宜时选不到。`flights = [[0,1,100],[1,2,100],[0,2,150]]`，`k = 1` 得到 `200`，正确是 `150`（直达，坐 1 趟也满足「最多 2 趟」）。
- 用不限步数的 Dijkstra：示例 1 得到 `400`，正确是 `700`。
- 终点不可达时 `dist[dst]` 仍是 `inf`，要转成 `-1`，不能直接 `int(inf)`（会抛 `OverflowError`）。

**追问。**
- 要输出具体的路线：松弛时同时记录前驱表 `parent[t][v]`，从 `parent[k+1][dst]` 沿行号逐行往回走。
- 空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**同模式。** LC 743 网络延迟时间、LC 1631 最小体力消耗路径、LC 1514 概率最大的路径、LC 1928 规定时间内到达终点的最小花费（同样带一个资源上限）。
