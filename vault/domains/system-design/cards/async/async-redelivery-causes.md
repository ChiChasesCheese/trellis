---
id: async-redelivery-causes
node: async.delivery.guarantees
type: qa
---
## Q
Your consumer code is bug-free and the broker is healthy. Name the concrete events that still cause the same message to be processed twice — and the one that means two consumers run it *at the same time*.

## A
- **Ack/offset commit lost** — you processed, then the ack or commit didn't land (crash, network drop, broker leader change). The broker re-delivers.
- **Lease expiry mid-processing** — SQS visibility timeout elapses, or Kafka `max.poll.interval.ms` is exceeded and the member is evicted. The broker assumes you died and hands the message to **another consumer while yours is still running**: redelivery here is *concurrent*, so idempotency must be race-safe (atomic insert on a unique key), not read-then-check.
- **Rebalance / partition reassignment** between processing and commit — the new owner restarts from the last committed offset.
- **Operational replay** — DLQ redrive, offset reset, or a backfill re-runs a window on purpose.
- **Producer resend after an ambiguous ack** — this one arrives as a *different broker message id* for the same business event, so dedup must key on a **producer-supplied business/event id**, never on the broker's message id or offset.

## Q zh
你的 consumer 代码无缺陷，broker 健康。列出仍然导致相同消息被处理两次的具体事件 — 以及一个表示两个 consumer *同时*运行它的事件。

## A zh
- **Ack/offset commit 丢失** — 你处理后，ack 或 commit 没有落地（崩溃、网络断、broker leader 变化）。Broker 重新投递。
- **处理中的 lease 过期** — SQS visibility timeout 经过，或 Kafka `max.poll.interval.ms` 超过且成员被驱逐。Broker 假设你死了并把消息交给**另一个 consumer，同时你的仍在运行**：重投递这里是*并发的*，所以幂等性必须是竞争安全的（原子插入唯一 key），不是读后检查。
- **处理和提交之间的 rebalance / partition 重新分配** — 新所有者从最后提交的 offset 重新开始。
- **操作重放** — DLQ redrive、offset 重置、或回填有意地重新运行一个窗口。
- **模糊 ack 后的生产者重发** — 这个对相同业务事件以*不同 broker message id* 到达，所以去重必须基于**生产者提供的业务/事件 id** keying，永远不能是 broker 的 message id 或 offset。
