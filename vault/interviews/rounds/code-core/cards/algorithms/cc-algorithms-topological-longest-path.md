---
id: cc-algorithms-topological-longest-path
node: algorithms.topological
type: qa
---
## Q
Every job has a duration and prerequisites, and parallelism is unlimited. Earliest time everything is finished?

## A
**Longest path in the DAG, computed in topological order** so that each node is processed only after every predecessor is final.

```python
finish = {u: dur[u] for u in nodes}          # no prerequisites ⇒ own duration
for u in kahn_order:
    for v in succ[u]:
        finish[v] = max(finish[v], finish[u] + dur[v])
answer = max(finish.values(), default=0)
```

- Initialising `finish[v]` to `dur[v]` is what makes a source node correct without a special case.
- Longest path is NP-hard on a general graph and **linear on a DAG** — the topological order is precisely what buys that ([[cc-algorithms-topological-kahn]]).
- No relations at all → `max(dur)`. A single chain → `sum(dur)`, which can be orders of magnitude larger than any one duration; both are the standard sanity checks.
- With a worker limit the answer is no longer the longest path — that is list scheduling with a heap, a different problem.

## Q zh
每个作业有时长和前置依赖，并行度不受限。最早什么时候全部完成？

## A zh
**DAG 上的最长路径，按拓扑序计算**，从而保证每个节点只在其所有前驱确定之后才被处理。

```python
finish = {u: dur[u] for u in nodes}          # 无前置 ⇒ 就是自身时长
for u in kahn_order:
    for v in succ[u]:
        finish[v] = max(finish[v], finish[u] + dur[v])
answer = max(finish.values(), default=0)
```

- 把 `finish[v]` 初始化为 `dur[v]`，正是让源节点无需特判就正确的原因。
- 最长路径在一般图上是 NP-hard，在 **DAG 上是线性的** —— 拓扑序买来的正是这一点（[[cc-algorithms-topological-kahn]]）。
- 完全没有依赖 → `max(dur)`。单条链 → `sum(dur)`，可能比任何单个时长大几个数量级；这两个是标准的自检。
- 一旦有工人数上限，答案就不再是最长路径 —— 那是带堆的列表调度，是另一个问题。
