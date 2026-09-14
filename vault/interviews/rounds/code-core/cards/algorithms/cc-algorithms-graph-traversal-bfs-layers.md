---
id: cc-algorithms-graph-traversal-bfs-layers
node: algorithms.graph-traversal
type: qa
---
## Q
Unweighted graph: you need the distance from `src` to every node, and the actual shortest chain to one of them.

## A
**BFS assigns final distances in dequeue order** — the first time a node is reached *is* its shortest distance, because the queue is always in non-decreasing distance order.

```python
dist, prev, q = {src: 0}, {src: None}, deque([src])
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist:
            dist[v] = dist[u] + 1; prev[v] = u; q.append(v)
```

- Reconstruct by walking `prev` back from the target and reversing.
- Valid for **unit weights only**. With weights it is Dijkstra ([[cc-algorithms-shortest-path-dijkstra-heap]]), and BFS silently answers a different question ([[cc-algorithms-shortest-path-longer-can-win]]).
- Neighbour iteration order decides *which* shortest path you get when several tie — sort the adjacency lists if the path itself is graded.
- Distances by layer, when you do not need `prev`, come from taking `len(q)` at the top of each round ([[cc-toolbox-deque-bfs-frontier]]).

## Q zh
无权图：你需要 `src` 到每个节点的距离，以及到其中某个节点的实际最短链。

## A zh
**BFS 按出队顺序确定最终距离** —— 第一次到达某节点*就是*它的最短距离，因为队列始终按距离非递减排列。

```python
dist, prev, q = {src: 0}, {src: None}, deque([src])
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist:
            dist[v] = dist[u] + 1; prev[v] = u; q.append(v)
```

- 从目标节点沿 `prev` 回溯再反转，即可重建路径。
- **只对单位权有效**。带权时应当用 Dijkstra（[[cc-algorithms-shortest-path-dijkstra-heap]]），而 BFS 会悄悄回答另一个问题（[[cc-algorithms-shortest-path-longer-can-win]]）。
- 邻居遍历顺序决定并列时你得到*哪一条*最短路 —— 如果路径本身会被判分，就给邻接表排序。
- 不需要 `prev`、只要按层距离时，在每轮开头取 `len(q)` 即可（[[cc-toolbox-deque-bfs-frontier]]）。
