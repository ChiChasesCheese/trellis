---
id: async-eos-boundary-choice
node: async.delivery.exactly-once
type: qa
---
## Q
Broker transactions or a transactional outbox? State the rule for choosing, and one place people wrongly assume broker EOS extends.

## A
The rule follows from **where the atomic boundary can physically be** — a transaction only spans one system:

- **System of record is the broker** (consume → transform → produce, offsets are just another topic write): use **broker transactions**. Input offsets and output records commit together inside Kafka.
- **System of record is your database** (an HTTP command mutates rows and must emit an event): the broker cannot enlist in your DB commit, so the atomic unit must be the **DB transaction** — write state + event row together (outbox) and publish from that row afterwards. Broker transactions are useless for this half.

Where it wrongly gets assumed to extend: **across clusters**. Replication (MirrorMaker 2, cross-region mirroring) re-produces records and is at-least-once with new offsets — transactional guarantees and offsets do not survive the hop. Same for a second broker of a different type in the chain: each boundary needs its own dedup.

## Q zh
Broker transactions 还是事务性 outbox？说出选择的规则，以及人们错误地假设 broker EOS 拓展到的一个地方。

## A zh
规则来自**原子边界在物理上能落在哪里** — 一个事务只能跨越一个系统：

- **真实来源是 broker**（消费 → 转换 → 生产，offset 只是另一个 topic 写）：使用 **broker transactions**。输入 offset 和输出记录在 Kafka 内部一起提交。
- **真实来源是你的数据库**（一个 HTTP 命令改变行且必须发出事件）：broker 不能登记在你的 DB 提交中，所以原子单元必须是 **DB 事务** — 一起写状态+事件行（outbox），然后从该行发布。Broker transactions 对这一半没有用。

错误地假设它拓展到的地方：**跨集群**。复制（MirrorMaker 2、跨区域镜像）重新生成记录，是新 offset 的 at-least-once — 事务性保证和 offset 不会在跳跃中存活。链中不同类型的第二个 broker 也是如此：每个边界需要自己的去重。
