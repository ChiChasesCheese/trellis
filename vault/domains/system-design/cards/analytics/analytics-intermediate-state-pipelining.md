---
id: analytics-intermediate-state-pipelining
node: analytics.batch
type: qa
---
## Q
A classic MapReduce workflow chains five jobs, writing every intermediate result to the replicated distributed filesystem; Spark runs the same logic as one job several times faster. What exactly did dataflow engines change about intermediate state, and what new problem did that create?

## A
MapReduce's model: each job **fully materializes** its output to HDFS (replicated 3x) before the next job may start. That buys durability and clean job boundaries, but costs replication I/O for data that lives minutes, and forces the workflow to run in **lock-step** — job N+1 waits for the *last* straggler of job N.

Dataflow engines (Spark, Flink, Tez) treat the workflow as **one DAG of operators**: intermediate results stay in memory or on local disk, are **not replicated**, and where no repartitioning is needed, records **pipeline** straight into the next operator without waiting for the stage to finish. Less I/O, no artificial barriers, and the scheduler sees the whole graph to optimize placement.

The created problem: intermediates are now **lost when a machine dies**. The fix is **recomputation from lineage** — the engine tracks how each partition of data was derived and re-runs just the affected tasks from the still-available ancestors — which is only correct if operators are **deterministic**; nondeterminism (random, time, unordered input dependence) forces cascading recomputation or wrong results.

## Q zh
一个经典的 MapReduce 工作流串联五个作业，把每个中间结果都写进带副本的分布式文件系统；Spark 用一个作业跑同样的逻辑，快好几倍。数据流（dataflow）引擎究竟改变了中间状态的什么？又因此制造了什么新问题？

## A zh
MapReduce 的模型：每个作业把输出**完整物化**到 HDFS（3 副本），下一个作业才能开始。这换来了持久性和干净的作业边界，代价是为只存活几分钟的数据支付副本 I/O，并迫使工作流**齿轮咬合式**推进——第 N+1 个作业要等第 N 个作业*最慢的*落伍者。

数据流引擎（Spark、Flink、Tez）把工作流看作**一张算子 DAG**：中间结果留在内存或本地磁盘，**不做副本**；在不需要重新分区的地方，记录**流水线式**地直接进入下一个算子，无需等整个阶段结束。I/O 更少、没有人为屏障，调度器还能看到全图来优化任务摆放。

制造的新问题：机器一挂，中间结果就**没了**。解法是**按血缘（lineage）重算**——引擎记录每个数据分区是如何派生出来的，只从仍然可用的祖先重跑受影响的任务——而这只有在算子**确定性**时才正确；非确定性（随机数、时间、依赖输入顺序）会导致级联重算或错误结果。
