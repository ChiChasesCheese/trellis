---
slug: find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance
---
## Q
**LC 1334 阈值距离内邻居最少的城市**｜Medium

`n` 个城市由带权无向边相连。对每个城市，数出最短路径距离不超过 `distance_threshold` 的其他城市个数，返回个数最少的城市；个数并列时返回编号最大的。

## A
**一句话。** 用 Floyd–Warshall 求出任意两城市的最短距离，再对每个城市数阈值内的邻居。

```python
def find_the_city(n, edges, distance_threshold):
    d = [[inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = d[v][u] = w
    for k in range(n):             # 中转点放最外层
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    best, ans = inf, -1
    for i in range(n):
        cnt = sum(d[i][j] <= distance_threshold
                  for j in range(n) if j != i)
        if cnt <= best:            # 并列取编号大的
            best, ans = cnt, i
    return ans
```

**复杂度。** 时间 `O(n^3)`，空间 `O(n^2)`。

**易错点。**
- 中转点 `k` 放在内层：Floyd 要求 `k` 在最外层，否则最短路不完整。
- 并列时写成 `<`：题目要编号最大，要用 `<=` 让后来者覆盖。
- 把自己算进邻居：要排除 `j == i`。

**追问。**
- 点多边少怎么办？：对每个点跑一次 Dijkstra，`O(n · m log n)`，稀疏图更快。
- Floyd 为什么能用滚动数组？：第 `k` 轮只依赖第 `k - 1` 轮的同一个矩阵，原地更新也正确。

**同模式。** LC 743 网络延迟时间、LC 1462 课程表 IV、LC 787 K 站中转内最便宜的航班、LC 399 除法求值
