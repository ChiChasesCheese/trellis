---
id: craft-dependency-graph-cycle-detection-5-across-problems-and-scales
node: craft.patterns.dependency-graph-cycle-detection
type: qa
step: 5
---
## Q
**依赖图与环检测 · 课程表、任务执行器、电子表格、账单规则里的同一个图**｜模式

Course Schedule II、任务执行器（DAG runner）、电子表格、账单规则排序，数据完全不同。它们用的图技巧有几种？放大到构建系统和工作流引擎，什么变了？

## A
**要点。** 同一个有向图，三个问题：①给一个合法顺序（Kahn / 后序 DFS）；②这条新边会不会成环（可达性，改之前查）；③遍历时有没有走回路径上的点（祖先链）。差别只在图是一次建好的，还是随用户操作不断改。

```python
# Course Schedule II（LeetCode）：一次建好，没排完就是有环
return out if len(out) == n else []

# amz-dag-runner：同一个判断，抛具体的环
if len(out) != len(names): raise CycleError(self._find_cycle(stuck))

# billing-tax-engine：规则很少，直接用 O(n²) 的稳定拓扑排序
ready = next((r for r in pending if all(n in done for n in r.needs)), None)
if ready is None:                       # 剩下的每条都在等别的剩下的：有环
    raise InvalidRuleSet(f"规则依赖成环: {[r.rule_id for r in pending]}")
```

**不变的。** 「排不下去 = 有环」这个判据；以及都要在使用图之前拒绝，而不是执行到一半才发现。**变化的。** 规则只有十来条时，反复扫 `pending` 找下一条能跑的，比维护入度更短、顺序天然稳定（保留输入顺序）；节点成千上万时，必须上入度和堆。

**见于。** course-schedule-ii、amz-dag-runner、spreadsheet-engine、billing-tax-engine、amz-linux-find。

**信号。** 需求里出现「先……才能……」「依赖」「引用」「重算受影响的」「符号链接」；输入里有「A 需要 B」这类二元关系。

**尺度对照。** 力扣：一次性拓扑排序。低层设计：增量改图 + 改前查环。分布式：构建系统（Bazel、Make）和工作流引擎（Airflow 的 DAG）。变化：图跨机器后，「环」要在提交 DAG 时静态检查（运行时才发现就晚了）；执行序不再是一个线性列表，而是「所有依赖都完成的节点可以并行跑」，Kahn 的 ready 队列就是调度队列；节点失败后，只需要重跑它和它的下游，和电子表格「只重算下游」是同一个思路。
