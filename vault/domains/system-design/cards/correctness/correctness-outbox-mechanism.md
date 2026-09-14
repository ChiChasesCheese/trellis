---
id: correctness-outbox-mechanism
node: correctness.outbox
type: qa
---
## Q
Walk through the transactional outbox pattern: what happens in the transaction, how do events reach the broker, and what guarantee do you end up with?

## A
1. In **one local transaction**: apply the state change AND insert the event row into an `outbox` table. Atomic — either both exist or neither.
2. A **relay** moves outbox rows to the broker: either a poller (`SELECT ... FOR UPDATE SKIP LOCKED`, publish, mark sent) or **CDC tailing the WAL** (Debezium outbox routing — lower latency, no polling load).
3. Relay marks/deletes rows only *after* broker ack → a crash re-publishes → guarantee is **at-least-once**, so consumers dedup by the event id stored in the outbox row.

You've traded "maybe lost" for "maybe duplicated" — which idempotency can fix, whereas a lost event is unrecoverable.

## Q zh
走过事务型 outbox 模式：交易内发生什么，事件怎样到达 broker，最终什么保证？

## A zh
1. **一个本地事务**内：应用状态改变 AND 将事件行插入 `outbox` 表。原子 — 要么都存在要么都不存在。
2. **relay** 移动 outbox 行到 broker：要么轮询器（`SELECT ... FOR UPDATE SKIP LOCKED`、发布、标记已发送）要么 **CDC 追踪 WAL**（Debezium outbox 路由 — 低延迟、无轮询负载）。
3. relay 仅*在*broker ack 后标记/删除行 → 崩溃重新发布 → 保证是**至少一次**，所以消费者按 outbox 行存储的事件 id 去重。

你用"可能重复"换了"可能丢失" — 幂等性能修复重复，但丢失事件无法恢复。
