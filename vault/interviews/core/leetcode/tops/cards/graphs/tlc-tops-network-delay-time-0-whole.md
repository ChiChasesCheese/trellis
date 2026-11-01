---
id: tlc-tops-network-delay-time-0-whole
node: graphs.network-delay-time
type: qa
---
## Q
**LC 743 网络延迟时间**｜Medium · 全公司热度第 334 名 · NeetCode 150

有 `n` 个网络节点，标记为 `1` 到 `n`。给你一个列表 `times`，表示信号经过有向边的传递时间，`times[i] = (u_i, v_i, w_i)`，其中 `u_i` 是源节点，`v_i` 是目标节点，`w_i` 是信号从源节点传递到目标节点的时间。现在从某个节点 `k` 发出一个信号，需要多久才能使所有节点都收到信号？如果不能使所有节点收到信号，返回 `-1`。`1 <= k <= n <= 100`，`1 <= times.length <= 6000`，`1 <= u_i, v_i <= n`，`u_i != v_i`，`0 <= w_i <= 100`，所有 `(u_i, v_i)` 互不相同。例：`times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2` → `2`；`times = [[1,2,1]], n = 2, k = 1` → `1`；`times = [[1,2,1]], n = 2, k = 2` → `-1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 单源最短路径（single-source shortest path）：Dijkstra 算法 + 最小堆。

**一句话。** 用 Dijkstra 求出 `k` 到每个节点的最短时间，所有节点都能到达时，最大的那个最短时间就是答案；有节点到不了则返回 `-1`。

**识别。** 「从一个源点出发，边权非负，求到所有点的最短距离」是 Dijkstra 的标准场景；信号同时沿所有边传播，所以收到信号的时间就是最短路径长度，全部收到的时间是其中的最大值。`n <= 100`，边 `6000`，`O(E log V)` 绰绰有余。

**推导。** 边权不全为 1，所以不能直接 BFS。Dijkstra 的贪心：每次从堆里取当前距离最小的点，它的距离已经不可能再被更短的路径改进（边权非负），确定下来后再松弛它的出边。一个点可能多次入堆（不同的距离），第一次弹出的一定是最短的，后面再弹出就跳过。

```python
def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    graph: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    dist: dict[int, int] = {}                    # 已确定最短距离的节点
    heap = [(0, k)]                              # (到源点的距离, 节点)
    while heap:
        d, u = heappop(heap)
        if u in dist:                            # 以更小的距离确定过了，这是过期条目
            continue
        dist[u] = d                              # 第一次弹出：距离最短，确定下来
        for v, w in graph[u]:
            if v not in dist:
                heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1   # 有节点没被确定：不连通
```

运行：`([[2,1,1],[2,3,1],[3,4,1]], 4, 2)` → `2`，`([[1,2,1]], 2, 1)` → `1`，`([[1,2,1]], 2, 2)` → `-1`，`([[1,2,0]], 2, 1)` → `0`。

**复杂度。** 时间 `O(E log E)`（每条边最多入堆一次），空间 `O(V + E)`。

**拓展优化。**
- `n <= 100` 时 Bellman-Ford 也行，代码更短、能处理负权（这里没有负权），时间 `O(V * E) = 6 * 10^5`：

```python
def network_delay_time_bf(times: list[list[int]], n: int, k: int) -> int:
    dist = [inf] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):                       # 最短路径最多 n-1 条边，松弛 n-1 轮
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    ans = max(dist[1:])
    return ans if ans < inf else -1
```

- 边数很多、点数很少的稠密图可以用不带堆的 `O(V^2)` Dijkstra；要还原路径时额外记录前驱节点。

**易错点。**
- 没检查是否所有节点都被到达：`([[1,2,1]], 2, 2)` 里只有 `k` 自己，`max(dist.values())` 是 `0`，会返回 `0`（正确 `-1`）。
- 入堆时就标记为已确定（BFS 习惯）：先入堆的路径不一定最短。`times = [[1,2,5],[1,3,1],[3,2,1]]`、`n = 3`、`k = 1` 会得到 `5`（正确 `2`，路径 `1 -> 3 -> 2`）。
- 节点编号从 1 开始，用长度为 `n` 的数组会越界；字典 / 长度 `n + 1` 的数组更省心。

**同模式。** LC 787 K 站中转内最便宜的航班、LC 1631 最小体力消耗路径、LC 1514 概率最大的路径、LC 778 水位上升的泳池中最短时间。
