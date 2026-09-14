---
id: cc-algorithms-shortest-path-dijkstra-heap
node: algorithms.shortest-path
type: qa
---
## Q
Non-negative weights, 10^5 edges. Write Dijkstra and justify the one line that looks redundant.

## A
```python
dist, pq = {src: 0}, [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist.get(u, INF): continue        # stale entry: u was finalized cheaper already
    for v, w in adj[u]:
        nd = d + w
        if nd < dist.get(v, INF):
            dist[v] = nd
            heapq.heappush(pq, (nd, v))
```

- `heapq` has no decrease-key, so an improvement is pushed as a *new* entry and the old one is skipped on pop ([[cc-toolbox-heap-lazy-invalidation]]). Without the skip you re-relax from a worse distance — still correct, but slower, and it destroys the "first pop finalizes" reasoning you rely on for early exit.
- O(E log E). Requires **non-negative** weights: a single negative edge invalidates the finalize-on-pop argument, and the answer can be wrong, not merely slow.
- A node is final the first time it is popped — that is where to record the answer or `break` on reaching the target.
- Ties need a second key in the tuple if the *path* is graded ([[cc-algorithms-shortest-path-reconstruct]]).

## Q zh
非负权，10^5 条边。写出 Dijkstra，并说明那一行看似多余的代码为什么必要。

## A zh
```python
dist, pq = {src: 0}, [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist.get(u, INF): continue        # 过期条目：u 已以更低代价被确定
    for v, w in adj[u]:
        nd = d + w
        if nd < dist.get(v, INF):
            dist[v] = nd
            heapq.heappush(pq, (nd, v))
```

- `heapq` 没有 decrease-key，所以改进是 push 一个*新*条目、pop 时跳过旧的（[[cc-toolbox-heap-lazy-invalidation]]）。不跳过就会从更差的距离重新松弛 —— 仍然正确但更慢，而且会毁掉你用于提前退出的「首次 pop 即确定」这一论证。
- O(E log E)。要求权重**非负**：只要有一条负边，「pop 即确定」的论证就失效，答案可能是错的而不只是慢。
- 节点在第一次被 pop 时即确定 —— 那里正是记录答案、或到达目标就 `break` 的位置。
- 如果*路径*会被判分，tuple 里需要第二个 key 来定并列（[[cc-algorithms-shortest-path-reconstruct]]）。
