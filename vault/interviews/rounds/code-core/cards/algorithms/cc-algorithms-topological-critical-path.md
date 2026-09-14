---
id: cc-algorithms-topological-critical-path
node: algorithms.topological
type: qa
---
## Q
You must also report *which* chain of jobs sets the finish time, deterministically. How?

## A
**Keep the arg-max predecessor while relaxing, then walk back from the latest finisher.**

```python
if cand > finish[v] or (cand == finish[v] and pred[v] != -1 and u < pred[v]):
    finish[v], pred[v] = cand, u
```

- A strict `>` alone keeps whichever predecessor happened to come first in topological order — not a stated rule, and not reproducible if the input is reordered. The explicit `==` branch makes "smallest id wins the tie" real ([[cc-algorithms-prefix-argmin-tiebreak]]).
- Start the walk at `max(nodes, key=lambda j: (finish[j], -j))` — largest finish, smallest id on ties — then follow `pred` and reverse.
- The critical path is **not** necessarily the path through the single longest job; it is the longest *sum*.
- Every job on it has zero slack: delaying any one of them delays the whole schedule, which is what makes the path worth reporting.

## Q zh
你还必须确定性地报告*哪一条*作业链决定了完成时间。怎么做？

## A zh
**在松弛时记录取到最大值的前驱，然后从最晚完成者回溯。**

```python
if cand > finish[v] or (cand == finish[v] and pred[v] != -1 and u < pred[v]):
    finish[v], pred[v] = cand, u
```

- 只用严格 `>` 会保留恰好在拓扑序中先出现的那个前驱 —— 这不是被规定的规则，而且输入重排后不可复现。显式的 `==` 分支才让「并列取 id 最小」真正成立（[[cc-algorithms-prefix-argmin-tiebreak]]）。
- 从 `max(nodes, key=lambda j: (finish[j], -j))` 开始回溯 —— 完成时间最大、并列取 id 最小 —— 然后沿 `pred` 走并反转。
- 关键路径**未必**经过那个单独最长的作业；它是最长的*总和*。
- 路径上的每个作业都没有余量：任何一个延迟都会拖慢整个计划，这正是这条路径值得报告的原因。
