---
id: tlc-min-cost-to-connect-all-points-4-followup
node: b.min-cost-to-connect-all-points
type: qa
step: 4
---
## Q
**LC 1584 连接所有点的最小费用**｜追问

面试官接着问：（1）用 Kruskal 怎么写，什么时候比 Prim 好？（2）要返回 MST 的具体边？（3）点数到 `10^5`，`O(n^2)` 不行了？

## A
1. **Kruskal**：枚举所有点对作为边，按权重排序，用并查集（Union-Find）依次尝试加入，端点已连通就跳过，加够 `n - 1` 条就停。

```python
from itertools import combinations


def min_cost_kruskal(points: list[list[int]]) -> int:
    n = len(points)
    edges = sorted(
        (abs(x1 - x2) + abs(y1 - y2), i, j)
        for (i, (x1, y1)), (j, (x2, y2)) in combinations(enumerate(points), 2)
    )
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径折半
            x = parent[x]
        return x

    total = used = 0
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            total += w
            used += 1
            if used == n - 1:
                break
    return total
```

   五个示例得到 `20`、`18`、`4`、`4000000`、`0`，`1000` 个随机点约 `0.17 s`（Prim 约 `0.04 s`）。Kruskal 是 `O(E log E)`，稠密图 `E ≈ n^2 / 2` 时比 Prim 慢；边是显式给出的稀疏图（`E` 接近 `n`）时，Kruskal 更自然。
2. **返回 MST 的边**：Prim 里更新 `dist[v] = d` 时同时记 `parent[v] = u`；循环结束后，`(parent[v], v)` 对所有 `v != 0` 就是 MST 的边。Kruskal 里每次合并成功的那条边就是 MST 的边。
3. **`n = 10^5`**：不能建完全图。曼哈顿距离有几何性质：MST 里的边一定出现在“每个点、在它周围八个方向扇区中的最近点”所构成的边集里，总共 `O(n)` 条候选边。用扫描线加树状数组找这些候选边，`O(n log n)`，再对它们跑 Kruskal。

**Python 提醒**：生成器里的 `enumerate(points)` 要在 `combinations` 外层，才能同时拿到下标和坐标；元组 `(w, i, j)` 按字典序比较，权重相同时用下标打破平局，结果可复现。
