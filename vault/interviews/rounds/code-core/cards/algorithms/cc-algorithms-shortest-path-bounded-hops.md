---
id: cc-algorithms-shortest-path-bounded-hops
node: algorithms.shortest-path
type: qa
---
## Q
Cheapest route using at most K stops. Why does Dijkstra get this wrong, and what replaces it?

## A
**Dijkstra finalizes a node at its cheapest cost regardless of hop count**, so a cheap 5-hop route to an intermediate city can block the only 2-hop route that satisfies the limit. Cost and hops are two dimensions and one heap key cannot order both.

**Bellman-Ford by rounds — K+1 rounds, each relaxing from a snapshot of the previous round:**

```python
dist = [INF] * n; dist[src] = 0
for _ in range(k + 1):
    prev = dist[:]                        # snapshot ⇒ one round adds at most ONE edge
    for u, v, w in edges:
        if prev[u] + w < dist[v]:
            dist[v] = prev[u] + w
```

- **Relaxing in place is the classic bug**: one round then chains several edges and the hop limit is not enforced at all.
- Cost O(K·E), which is fine for the usual K ≤ n and needs only an edge list ([[cc-toolbox-graph-representation-choice]]).
- The alternative is Dijkstra over the *state* `(node, hops)` — correct, more code, and only worth it when K is large.

## Q zh
最多经停 K 次的最便宜路线。为什么 Dijkstra 会做错，用什么替代？

## A zh
**Dijkstra 会不管跳数地按最低代价确定一个节点**，所以一条便宜的 5 跳路线可能挡住唯一满足限制的 2 跳路线。代价和跳数是两个维度，一个堆的 key 无法同时排它们。

**按轮次的 Bellman-Ford —— K+1 轮，每轮都从上一轮的快照松弛：**

```python
dist = [INF] * n; dist[src] = 0
for _ in range(k + 1):
    prev = dist[:]                        # 快照 ⇒ 一轮最多增加一条边
    for u, v, w in edges:
        if prev[u] + w < dist[v]:
            dist[v] = prev[u] + w
```

- **原地松弛是经典 bug**：那样一轮就能串起好几条边，跳数限制形同虚设。
- 代价 O(K·E)，在常见的 K ≤ n 下没问题，而且只需要边列表（[[cc-toolbox-graph-representation-choice]]）。
- 另一种做法是在*状态* `(node, hops)` 上跑 Dijkstra —— 正确、代码更多，只在 K 很大时才值得。
