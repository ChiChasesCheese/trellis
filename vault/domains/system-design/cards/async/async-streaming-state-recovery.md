---
id: async-streaming-state-recovery
node: async.streaming.processing
type: qa
---
## Q
A stream job has been running for a month, holding large windowed aggregates in memory, when a worker dies. Restarting from scratch would mean replaying a month of input. How do frameworks like Flink make recovery cheap, and what's special about how a consistent snapshot is taken while the stream keeps flowing?

## A
**Periodic checkpoints of operator state + input positions.** Recovery = restore the last completed checkpoint's state, rewind the source to the offsets recorded *in that same checkpoint*, and reprocess only the gap — minutes, not a month. This requires a **replayable source** (a log like Kafka, not an ephemeral push feed).

The consistency trick (Chandy-Lamport style, Flink's barriers): the source injects a **checkpoint barrier** into the stream; each operator snapshots its state exactly when the barrier passes through it, then forwards the barrier. Since the barrier flows *with* the data, every operator's snapshot reflects exactly the same prefix of the input — a consistent cut — without ever pausing the whole pipeline; state itself goes to durable storage asynchronously.

Boundary to state: checkpointing makes **internal state** exactly-once (each event's effect on state counted once). Output emitted after the checkpoint is **re-emitted on recovery**, so end-to-end correctness still needs an idempotent or transactional sink. Triad to quote: replayable source + checkpointed state + dedupable sink.

## Q zh
一个流处理任务已连续运行一个月，内存里持有大量窗口聚合，此时一个 worker 挂了。从头重启意味着回放一个月的输入。Flink 这类框架如何让恢复变得廉价？在数据流不停的情况下取一致快照，特殊在哪里？

## A zh
**周期性地对算子状态 + 输入位点做 checkpoint。** 恢复 = 载入最近一次完成的 checkpoint 的状态，把 source 倒回*同一个 checkpoint 里记录的* offset，只重放这段缺口——几分钟，而不是一个月。这要求 **source 可回放**（Kafka 这样的 log，而不是转瞬即逝的推送流）。

一致性的技巧（Chandy-Lamport 风格，Flink 的 barrier）：source 向流中注入一个 **checkpoint barrier**；每个算子恰好在 barrier 穿过它的那一刻对自身状态做快照，然后把 barrier 继续向下游转发。因为 barrier 是*随着*数据流动的，所有算子的快照反映的是完全相同的输入前缀——一个一致的切面——而整条流水线从未整体暂停；状态本身异步写入持久存储。

要讲清的边界：checkpoint 让**内部状态**做到 exactly-once（每个事件对状态的影响只计一次）。checkpoint 之后发出的输出会在恢复时**重新发出**，所以端到端正确性仍需要幂等或事务性的 sink。可引用的三件套：可回放的 source + 有 checkpoint 的状态 + 可去重的 sink。
