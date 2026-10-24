---
id: tlc-patterns-shortest-path-4-bellman-ford
node: patterns.shortest-path
type: qa
step: 4
---
## Q
**最短路（Shortest Path）｜限制边数：K 站中转内最便宜的航班（LC 787）**

"最多经过 `k` 站"为什么不能直接用 Dijkstra？Bellman-Ford 怎样按轮数限制边数，为什么每轮要用上一轮的数组？

## A
最多 `k` 站中转 = 最多 `k + 1` 条航班。Bellman-Ford 的第 `i` 轮松弛后，`dist[v]` 表示**最多用 `i` 条边**到 `v` 的最小花费。

```python
import math
def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    inf = math.inf
    dist = [inf] * n
    dist[src] = 0
    for _ in range(k + 1):                 # k + 1 轮 = 最多 k + 1 条航班
        nxt = dist[:]                      # 只用上一轮的结果松弛，保证每轮恰好多走一条边
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == inf else dist[dst]
```

运行：`(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1)` → `700`；`(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1)` → `200`，`k=0` → `500`；无航班 → `-1`。时间 `O(k · E)`，空间 `O(n)`。

**反例：原地更新（不拷贝）。** 航班 `0→1`、`1→2`、`2→3`（各 `100`），`k = 0`（只允许直飞，一条边），求 `0→3`：
- 原地更新、航班顺序恰好是 `0→1, 1→2, 2→3`：一轮之内 `dist` 被连续传递，得到 `300`。
- 正确答案是 `-1`（直飞不可达）。

**为什么不用普通 Dijkstra**：Dijkstra 保留每个点的最小花费，但最便宜的路径可能经过很多站，超出限制；而一条稍贵但站数少的路径才合法。要用 Dijkstra，状态必须是 `(城市, 已用站数)`，一个城市在不同站数下各自记录最小花费，也能得到正确答案。

`n <= 100`，边数最多 `4950`，`k < n` 时总计算量 `5 * 10^5` 量级。
