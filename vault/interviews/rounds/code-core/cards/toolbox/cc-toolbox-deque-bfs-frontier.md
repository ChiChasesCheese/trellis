---
id: cc-toolbox-deque-bfs-frontier
node: toolbox.deque
type: qa
---
## Q
You need distances **by layer**, not just reachability. How do you get the layer boundary out of a single queue?

## A
**Take the layer's size before draining it.**

```python
d = 0
while q:
    for _ in range(len(q)):            # exactly the nodes at distance d
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    d += 1
```

- The alternative is queueing `(node, depth)` pairs — equivalent, and better when only one node's depth is wanted.
- Mark visited on **push**, not on pop, or the frontier duplicates ([[cc-algorithms-graph-traversal-visited-on-push]]).
- `appendleft` turns the same deque into a stack (DFS) or into a 0-1 BFS: zero-weight edges to the front, weight-one edges to the back.
- A hop-limited search is this loop with `for _ in range(k + 1)` around it — layers are the natural place a hop limit attaches ([[cc-algorithms-shortest-path-bounded-hops]]).

## Q zh
你需要**按层**的距离，而不只是可达性。怎么从单个队列里取出层边界？

## A zh
**在排空这一层之前先取它的大小。**

```python
d = 0
while q:
    for _ in range(len(q)):            # 恰好是距离为 d 的那些节点
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    d += 1
```

- 另一种做法是把 `(node, depth)` 成对入队 —— 等价，且只关心某一个节点深度时更合适。
- 在 **push** 时而不是 pop 时标记已访问，否则前沿会重复（[[cc-algorithms-graph-traversal-visited-on-push]]）。
- `appendleft` 能把同一个 deque 变成栈（DFS），或变成 0-1 BFS：零权边入头、单位权边入尾。
- 带跳数限制的搜索就是这个循环外面套一层 `for _ in range(k + 1)` —— 层正是跳数限制天然附着的地方（[[cc-algorithms-shortest-path-bounded-hops]]）。
