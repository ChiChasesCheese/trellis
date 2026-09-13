# qA02 · LC 787 至多 K 次中转的最便宜航线

> `problems/qA02_lc787_cheapest_flights_k_stops/` · 4 个 part · LC Stripe tag 频率 56–89
> **主题：跳数上限打破了 Dijkstra 的贪心不变量 —— 必须用按轮松弛。**

## 一句话题意

`n` 个城市、一堆有向带权边、起点 `src`、终点 `dst`、最多 `k` 次中转。求最便宜的价格。

## 解题思路（这道题只有一个难点）

### Part 1 — Bellman-Ford，`k+1` 轮

```python
def find_cheapest_price(n, flights, src, dst, k) -> int:
    INF = float("inf")
    dist = [INF] * n; dist[src] = 0
    for _ in range(k + 1):              # k 次中转 = 最多 k+1 条边
        prev = dist[:]                  # ★★★ 必须用上一轮的副本
        for u, v, w in flights:
            if prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    return -1 if dist[dst] == INF else dist[dst]
```

**`prev = dist[:]` 是整道题的核心。**
不复制的话，同一轮里 `u` 刚被更新的值会立刻被 `v` 用上，**一轮就走了多跳**，跳数限制失效。

**为什么不能用 Dijkstra**：Dijkstra 的贪心不变量是"第一次弹出某点时它已经最优"，
但在跳数受限的问题里，**先到的（更便宜的）路径可能跳数太多而不可用**。
（要用 Dijkstra 就必须把状态扩成 `(city, stops_used)`，堆键 `(cost, stops)` —— 也是合法解法。）

### Part 2 — 按跳数 BFS

第 0 层 `{src: 0}`；第 `h+1` 层 = 第 `h` 层每个点的出邻居中，
新代价**严格低于**该城市**有史以来**最好代价的那些（更早到达且不更贵的路径支配它：跳更少**且**更便宜）。
跑满 `k+1` 层或前沿为空就停。必须与 Part 1 在任何输入上一致。

**剪枝要对"有史以来最好"比较，不是只对当前层。**

### Part 3 — 返回行程

平手规则：**航段少的优先，再按城市 id 列表的字典序最小**。
不可达 → `None`；`src == dst` → `[src]`。

### Part 4 — 带承运商（与 q22 打通）

路线是 `FROM:TO:CARRIER:price` 字符串。指定承运商时只能飞它的航段；`"*"` 时任意混飞。
其余同 Part 1（`<= k` 次中转）。未知城市 → `-1`。

## 坑

1. **轮内原地松弛**（不复制）→ 一轮走多跳 → 样例 1 就错。
2. `k = 0` = 只有直飞；`k = n-1` = 无限制。
3. `src == dst` → 0 / `[src]`；完全没有航班 → -1；即使不限跳数也不可达。
4. **更便宜的路线需要的中转次数超过上限**（样例 1 考的就是这个）。
5. **环（`2 -> 0`）不能帮上忙。**
6. Part 2 的剪枝要用"有史以来最好"。
7. Part 3 的平手：**先比航段数，再比字典序**。

## 变体

- q22 的 P1–3（直达 / 恰好一次中转 / 任意跳数最便宜）—— 字符串路线版 + 承运商过滤。
- 状态扩展的 Dijkstra `(city, stops_used)`，堆键 `(cost, stops)`。
- "先比跳数再比价格"（q21 的汇率）—— 先 BFS，价格当 tie-break。

## Code Core 节点

**`algorithms.shortest-path`**（Bellman-Ford 按轮） · `algorithms.graph-traversal` ·
`algorithms.recognition`（识别出跳数上限） · `toolbox.graph-repr` · `output.ordering`

## 自测清单

- [ ] 把 `prev = dist[:]` 去掉，确认样例 1 变错（**这是必做的验证**）
- [ ] `k = 0` / `k = n-1`
- [ ] `src == dst` / 无航班 / 完全不可达
- [ ] 更便宜但中转过多的路线
- [ ] 含环的图
- [ ] Part 1 与 Part 2 在随机图上一致
- [ ] Part 3 的两级平手
