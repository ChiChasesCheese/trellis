---
slug: number-of-possible-sets-of-closing-branches
---
## Q
**LC 2959 关闭分部的可行集合数目**｜Hard

`n <= 10` 个分部，带权无向道路（可有重边）。关闭若干分部（可以不关、也可以全关），要求留下的分部两两最短距离都 `<= maxDistance`，求方案数。

## A
**一句话。** `n` 很小，枚举留下的点集 `mask`（`2^n` 种），每种只在保留点上跑一遍 Floyd，检查所有点对距离。

```python
def number_of_sets(n, max_distance, roads):
    ans = 0
    for mask in range(1 << n):
        keep = [i for i in range(n) if mask >> i & 1]
        d = [[inf] * n for _ in range(n)]
        for i in keep:
            d[i][i] = 0
        for u, v, w in roads:
            if mask >> u & 1 and mask >> v & 1:
                d[u][v] = d[v][u] = min(d[u][v], w)  # 重边取小
        for k in keep:          # Floyd：只经过保留的点
            for i in keep:
                for j in keep:
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
        ok = all(d[i][j] <= max_distance
                 for i in keep for j in keep)
        ans += ok
    return ans
```

**复杂度。** 时间 `O(2^n·(n³ + m))`，空间 `O(n²)`。

**易错点。**
- 重边直接覆盖：后来的长边会把短边冲掉，要取 `min`。
- Floyd 经过被关闭的点：中转点也必须是保留的点。

**追问。**
- 空集和单点算吗？：算，空集没有点对，单点距离为 0，都合法。
- `n` 再大一些？：没有多项式解法的明显结构，靠的就是 `n <= 10` 的枚举。

**同模式。** LC 743 网络延迟时间、LC 1334 阈值距离内邻居最少的城市、LC 1462 课程表 IV
