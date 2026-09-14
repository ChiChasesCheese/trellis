---
id: async-eos-sink-determinism
node: async.delivery.exactly-once
type: qa
---
## Q
A Flink job runs with exactly-once checkpointing and writes each result to Postgres. What are the only two sink designs that make the end-to-end result exactly-once, and what silently breaks both?

## A
On recovery the job rewinds to the last checkpoint and **re-emits** everything after it, so the sink must absorb the replay:

- **Idempotent sink** — an upsert on a deterministic primary key (e.g. `(entity_id, window_end)` or `(topic, partition, offset)`), so a re-applied write converges. Cheapest and the usual answer.
- **Two-phase-commit sink** — write into an open sink transaction, *pre-commit* on checkpoint barrier, *commit* only when the checkpoint is confirmed complete; on restart, re-open and commit pending transactions by a recoverable transaction id. Fragile in practice: the sink's transaction timeout must exceed your longest checkpoint interval + recovery, or the pre-committed data is silently rolled back.

What breaks both: **non-determinism in the replayed path** — `uuid4()` keys, `now()` in the key or payload, or ordering that depends on arrival — because the replay then produces *different* rows instead of overwriting the old ones. Sinks with no key and no transaction (append-only HTTP calls, emails, payment APIs) can never be more than at-least-once without their own idempotency key.

## Q zh
一个 Flink 任务使用 exactly-once checkpointing 运行，每个结果写入 Postgres。什么是唯二能使端到端结果 exactly-once 的 sink 设计，什么会无声破坏两者？

## A zh
恢复时任务会回卷到最后一个 checkpoint，**重新发出**之后的所有内容，所以 sink 必须吸收重放：

- **幂等 sink** — 基于确定性主键的 upsert（例如 `(entity_id, window_end)` 或 `(topic, partition, offset)`），所以重新应用的写会收敛。成本最低且是通常的答案。
- **两阶段提交 sink** — 写入开放的 sink 事务，在 checkpoint barrier 时*预提交*，只在 checkpoint 确认完成时*提交*；重启时，通过可恢复的事务 id 重新打开并提交待定事务。实践中很脆弱：sink 的事务超时必须超过你最长的 checkpoint 间隔 + 恢复时间，否则预提交的数据会无声回滚。

破坏两者的是：**重放路径中的非确定性** — `uuid4()` key、key 或负载中的 `now()`，或依赖到达顺序 — 因为重放会产生*不同的*行而不是覆盖旧行。没有 key 也没有事务的 sink（仅追加 HTTP 调用、邮件、支付 API）如果没有自己的 idempotency key，永远只能是 at-least-once。
