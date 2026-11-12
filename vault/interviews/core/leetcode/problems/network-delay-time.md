---
slug: network-delay-time
---
## Q
**LC 743 网络延迟时间**｜Medium

带权有向图，从节点 `k` 发信号。求所有节点都收到信号所需的时间，有节点到不了返回 `-1`。

## A
**一句话。** Dijkstra 求 `k` 到各点的最短时间，全部可达时取最大值。

```python
def network_delay_time(times, n, k):
    g = defaultdict(list)
    for u, v, w in times:
        g[u].append((v, w))
    dist = {}                      # 已确定最短距离的节点
    h = [(0, k)]
    while h:
        d, u = heappop(h)
        if u in dist:              # 过期条目
            continue
        dist[u] = d                # 首次弹出即最短
        for v, w in g[u]:
            if v not in dist:
                heappush(h, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
```

**复杂度。** 时间 `O(E log E)`，空间 `O(V + E)`。

**易错点。**
- 没检查是否全部可达：`([[1,2,1]], 2, 2)` 会返回 `0`，应为 `-1`。
- 入堆时就标记已确定：先入堆的路径不一定最短，`[[1,2,5],[1,3,1],[3,2,1]]` 会得 `5`，应为 `2`。

**追问。**
- 为什么权重非负才能用 Dijkstra？：弹出时距离才最终确定，负权会让后弹出的更短。
- 边权全为 `1` 怎么办？：直接 BFS 即可。

**同模式。** LC 787 K 站中转内最便宜的航班、LC 1631 最小体力消耗路径、LC 1514 概率最大的路径、LC 778 水位上升的泳池中最短时间
