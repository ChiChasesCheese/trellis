---
id: cc-algorithms-topological-kahn
node: algorithms.topological
type: qa
---
## Q
Write Kahn's algorithm, and say where the node universe comes from.

## A
```python
indeg = {u: 0 for u in nodes}              # EVERY node, not only those with an edge
for u, v in edges:
    indeg[v] += 1
q = deque(u for u in nodes if indeg[u] == 0)
order = []
while q:
    u = q.popleft(); order.append(u)
    for v in succ[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
```

- Seeding `indeg` from the edge list alone loses every isolated node and every pure source — they never enter the queue and never appear in the order.
- O(V + E), iterative, so no recursion limit ([[cc-algorithms-graph-traversal-iterative]]).
- Watch the index base: relations given 1-based against a 0-based duration array is the classic off-by-one, and it is wrong in both directions.
- The order among simultaneously ready nodes is arbitrary unless you impose one ([[cc-algorithms-topological-deterministic-order]]).

## Q zh
写出 Kahn 算法，并说明节点全集从哪里来。

## A zh
```python
indeg = {u: 0 for u in nodes}              # 每一个节点，不只是有边的那些
for u, v in edges:
    indeg[v] += 1
q = deque(u for u in nodes if indeg[u] == 0)
order = []
while q:
    u = q.popleft(); order.append(u)
    for v in succ[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
```

- 只从边列表初始化 `indeg` 会丢掉所有孤立节点和所有纯源点 —— 它们永远进不了队列，也不会出现在结果顺序里。
- O(V + E)，迭代式，所以没有递归限制（[[cc-algorithms-graph-traversal-iterative]]）。
- 注意下标基准：以 1 为基的关系配上以 0 为基的时长数组是经典 off-by-one，而且两个方向都会错。
- 同时就绪的节点之间顺序是任意的，除非你强加一个（[[cc-algorithms-topological-deterministic-order]]）。
