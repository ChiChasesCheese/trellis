---
slug: min-cost-to-connect-all-points
---
## Q
**LC 1584 连接所有点的最小费用**｜Medium

平面上 `n` 个点，连两点的费用是曼哈顿距离。求把所有点连通的最小总费用。

## A
**一句话。** 完全图的最小生成树，稠密图用数组版 Prim：每轮选离已选集合最近的点，再更新其余点的距离。

```python
def min_cost_connect_points(points):
    n = len(points)
    INF = 1 << 60
    dist = [INF] * n        # 到已选集合的最短距离
    dist[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]),
                key=dist.__getitem__)
        used[u] = True
        total += dist[u]
        ux, uy = points[u]
        for v in range(n):
            if not used[v]:
                vx, vy = points[v]
                d = abs(ux - vx) + abs(uy - vy)
                dist[v] = min(dist[v], d)
    return total
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 取最短的 `n-1` 条边不查成环：`[[0,0],[2,2],[3,10],[5,2],[7,0]]` 得 `18`，应为 `20`。
- 把 Prim 写成 Dijkstra，`dist[v] = dist[u] + d`：同一例子得 `31`，`dist` 只是连到集合的那一条边的权重。
- 漏了 `dist[0] = 0`：第一轮选点不定，`total` 会加上 `INF`。

**追问。**
- 点很多（`10^5`）？：每点只向 8 个方向扇区里最近的点连候选边，再 Kruskal，`O(n log n)`。
- 边已显式给出的稀疏图？：Kruskal 加并查集，`O(E log E)`。

**同模式。** LC 1135 最低成本联通所有城市、LC 1489 找到最小生成树里的关键边和伪关键边、LC 1168 水资源分配优化、LC 1631 最小体力消耗路径
