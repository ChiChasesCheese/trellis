---
slug: maximum-path-quality-of-a-graph
---
## Q
**LC 2065 最大化一张图中的路径价值**｜Hard

无向图，点有价值、边有耗时（`>= 10`），每点度数 `<= 4`，`maxTime <= 100`。从 0 出发回到 0、总时间不超过 `maxTime` 的路径中，不同点的价值和最大是多少（点可重复经过，价值只算一次）。

## A
**一句话。** 每条边至少 10 秒，路径最多 10 条边，度数 `<= 4`，直接回溯所有路径；用计数数组记点在路径上出现几次，首次到达才加价值。

```python
def maximal_path_quality(values, edges, max_time):
    g = defaultdict(list)
    for u, v, t in edges:
        g[u].append((v, t))
        g[v].append((u, t))
    cnt = [0] * len(values)      # 点在当前路径上出现的次数
    cnt[0] = 1
    ans = 0

    def dfs(u, time, val):
        nonlocal ans
        if u == 0:
            ans = max(ans, val)  # 回到 0 就是一条合法路径
        for v, t in g[u]:
            if time + t <= max_time:
                gain = values[v] if cnt[v] == 0 else 0
                cnt[v] += 1
                dfs(v, time + t, val + gain)
                cnt[v] -= 1      # 回溯

    dfs(0, 0, values[0])
    return ans
```

**复杂度。** 时间 `O(4^{maxTime/10})`，约 `10^6`；空间 `O(n + m)`。

**易错点。**
- 用 `visited` 布尔数组禁止重复经过：题目允许重复走，只是价值不重复算。
- 回溯时直接设 `cnt[v] = 0`：同一点可能在路径上出现多次，要减一。

**追问。**
- 怎么剪枝？：先用 Dijkstra 求各点回到 0 的最短时间，`time + t + back[v] > maxTime` 就不走。
- 为什么能暴力？：数据范围卡死了路径长度和分支数，是看约束选算法的典型。

**同模式。** LC 79 单词搜索、LC 1219 黄金矿工、LC 787 K 站中转内最便宜的航班
