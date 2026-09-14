---
id: async-kafka-transactions-eos
node: async.delivery.exactly-once
type: qa
---
## Q
How does Kafka achieve exactly-once for a consume-transform-produce pipeline (Kafka Streams), and where does the guarantee stop?

## A
The producer opens a **transaction** that atomically commits both the **output records** and the **input consumer offsets** (offsets are just writes to an internal topic). Crash → transaction aborts → offsets not committed → reprocess and rewrite; downstream consumers with `isolation.level=read_committed` never see aborted records. A stable `transactional.id` + epoch **fences zombie producers** — an old instance's commits are rejected.

The guarantee stops at Kafka's edge: any **external side effect** (HTTP call, email, non-transactional DB write) inside the loop can still happen twice. External sinks need their own idempotent or transactional write ([[async-exactly-once-myth]]).

## Q zh
Kafka 如何为 consume-transform-produce 管道（Kafka Streams）实现 exactly-once，保证在哪里停止？

## A zh
生产者打开一个**事务**，原子性地提交**输出记录**和**输入 consumer offset**（offset 只是内部 topic 的写）。崩溃 → 事务中止 → offset 未提交 → 重新处理并重写；下游的 consumer 使用 `isolation.level=read_committed` 永远看不到中止的记录。稳定的 `transactional.id` + epoch **隔离僵尸生产者** — 旧实例的提交被拒绝。

保证在 Kafka 的边界处停止：任何**外部副作用**（HTTP 调用、邮件、非事务性 DB 写）在循环内部仍然可能发生两次。外部 sink 需要自己的幂等或事务性写。
