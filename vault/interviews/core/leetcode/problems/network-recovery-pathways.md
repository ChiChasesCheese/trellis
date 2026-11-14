---
slug: network-recovery-pathways
---
## Q
**LC 3620 恢复网络路径**｜Hard

有向无环图，边有成本，部分节点离线。从 `0` 到 `n-1` 的路径要求中间节点都在线、总成本 `≤ k`，分数是路上最小边成本，求最大分数，没有返回 `-1`。

## A
**一句话。** 最大化最小值，二分阈值 `t`：只用成本 `≥ t` 的边，在拓扑序上 DP 求最短路，看是否 `≤ k`；候选阈值就是所有边成本。

```python
def find_max_path_score(edges, online, k):
    n = len(online)
    g = [[] for _ in range(n)]
    deg = [0] * n
    for u, v, c in edges:
        if online[u] and online[v]:     # 离线点的边没用
            g[u].append((v, c))
            deg[v] += 1
    order, q = [], deque(i for i in range(n) if deg[i] == 0)
    while q:                            # 拓扑序
        u = q.popleft()
        order.append(u)
        for v, _ in g[u]:
            deg[v] -= 1
            if deg[v] == 0:
                q.append(v)

    def ok(t):                          # 只走 >= t 的边
        dist = [inf] * n
        dist[0] = 0
        for u in order:
            for v, c in g[u]:
                if c >= t and dist[u] + c < dist[v]:
                    dist[v] = dist[u] + c
        return dist[-1] <= k

    cand = sorted({c for _, _, c in edges})
    lo, hi = 0, len(cand)           # 第一个不可行的下标
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(cand[mid]):
            lo = mid + 1
        else:
            hi = mid
    return cand[lo - 1] if lo else -1
```

**复杂度。** 时间 `O((n + m) log m)`，空间 `O(n + m)`。

**易错点。**
- 在 DAG 上用 Dijkstra：能做但多一个 `log`；拓扑序松弛一遍就是最短路。
- 二分的是任意整数：答案一定是某条边的成本，在去重排序的成本上二分。

**追问。**
- 为什么单调？：阈值越高可用的边越少，最短路只会变长或不存在。
- 不是 DAG？：判定换成 Dijkstra，`O((n + m) log n · log m)`。

**同模式。** LC 778 水位上升的泳池中游泳、LC 1631 最小体力消耗路径、LC 207 课程表
