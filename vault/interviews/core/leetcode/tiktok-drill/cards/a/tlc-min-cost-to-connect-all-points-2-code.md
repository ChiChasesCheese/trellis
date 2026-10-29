---
id: tlc-min-cost-to-connect-all-points-2-code
node: a.min-cost-to-connect-all-points
type: qa
step: 2
---
## Q
**LC 1584 连接所有点的最小费用**｜写出 Python 实现

`points` 是平面上互不相同的点（`1 <= points.length <= 1000`，坐标绝对值至多 `10^6`），连接两点的费用是曼哈顿距离。返回连接所有点（任意两点之间恰有一条路径）的最小总费用。

## A
**思路。** 完全图上的最小生成树，用 Prim 的数组版。`dist[i]` 是 `i` 到已选集合的最短距离，起点 `dist[0] = 0`。每轮选出未选点中 `dist` 最小的 `u`，把 `dist[u]` 加进总费用，再用 `u` 到每个未选点的距离去更新它们的 `dist`。

```python
def min_cost_connect_points(points: list[list[int]]) -> int:
    n = len(points)
    INF = 1 << 60
    dist = [INF] * n                       # dist[i]：i 到已选集合的最短曼哈顿距离
    dist[0] = 0
    used = [False] * n
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=dist.__getitem__)   # 离集合最近的未选点
        used[u] = True
        total += dist[u]
        ux, uy = points[u]
        for v in range(n):
            if not used[v]:
                d = abs(ux - points[v][0]) + abs(uy - points[v][1])
                if d < dist[v]:
                    dist[v] = d
    return total
```

运行：`[[0,0],[2,2],[3,10],[5,2],[7,0]]` → `20`，`[[3,12],[-2,5],[-4,1]]` → `18`，`[[0,0],[1,1],[1,0],[-1,1]]` → `4`，`[[-1000000,-1000000],[1000000,1000000]]` → `4000000`，`[[0,0]]` → `0`；`1000` 个随机点约 `40 ms`。

**复杂度。** 时间 `O(n^2)`：`n` 轮，每轮扫描选点和更新各 `O(n)`；空间 `O(n)`。

**写法要点。** `min(生成器, key=dist.__getitem__)` 是“按另一个数组的值取最小下标”的惯用写法，不需要写手动循环；`INF = 1 << 60` 比 `float("inf")` 好，保证 `total` 始终是整数；点到点的距离现算，不预先建 `n × n` 的矩阵，省 `10^6` 个元素的空间；`ux, uy = points[u]` 把内层循环里的重复下标提到外面。
