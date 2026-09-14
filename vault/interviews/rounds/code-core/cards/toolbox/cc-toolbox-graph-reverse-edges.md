---
id: cc-toolbox-graph-reverse-edges
node: toolbox.graph-repr
type: qa
---
## Q
You have `succ` (prerequisite → dependent). Two later parts need indegrees and "the longest chain *after* this node". What do you build?

## A
**Both directions and the indegree in one pass over the edges.**

```python
succ, pred, indeg = defaultdict(list), defaultdict(list), {u: 0 for u in nodes}
for u, v in edges:
    succ[u].append(v); pred[v].append(u); indeg[v] += 1
```

- Indegree must be initialised for **every** node, not only those with an incoming edge, or Kahn's start set silently misses the isolated ones ([[cc-algorithms-topological-kahn]]).
- "Longest tail from a node" is the longest path in the **reversed** graph — the same DP with `succ` and `pred` swapped, not a new algorithm.
- Reachability *to* a target is BFS on the reversed graph, not a repeated forward search from every node.
- Reversing after the fact costs another O(E) pass and a second copy in memory; building both up front is cheaper and removes a class of "which direction is this dict?" bugs.

## Q zh
你有 `succ`（前置 → 后继）。后面两个 part 需要入度，以及「该节点*之后*最长的链」。要构造什么？

## A zh
**在对边的一趟遍历里同时得到两个方向和入度。**

```python
succ, pred, indeg = defaultdict(list), defaultdict(list), {u: 0 for u in nodes}
for u, v in edges:
    succ[u].append(v); pred[v].append(u); indeg[v] += 1
```

- 入度必须为**每个**节点初始化，而不只是有入边的那些，否则 Kahn 的起始集合会悄悄漏掉孤立节点（[[cc-algorithms-topological-kahn]]）。
- 「从某节点出发的最长尾」就是**反向**图上的最长路径 —— 是把 `succ` 和 `pred` 对调的同一个 DP，而不是新算法。
- 「能到达目标」的可达性是在反向图上做 BFS，而不是从每个节点重复做正向搜索。
- 事后再反转要多一趟 O(E) 和一份内存副本；一开始就同时建好更便宜，还消灭了一整类「这个 dict 是哪个方向」的 bug。
