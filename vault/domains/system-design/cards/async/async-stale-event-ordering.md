---
id: async-stale-event-ordering
node: async.delivery.guarantees
type: qa
---
## Q
Your handler is idempotent and the topic is keyed by entity, yet a profile occasionally reverts to an old address. Why isn't idempotency enough, and what is the fix?

## A
Per-partition ordering only holds for the **stream as stored**, not for the order your handler *observes*. Any of these re-orders events for one key: a failed message retried after backoff while later messages proceed, a DLQ redrive replayed hours later, a rebalance replaying from an older offset, or concurrent handler threads within one partition. Idempotency makes a repeat harmless; it does not make a **stale** write harmless.

Fixes — make the handler **order-insensitive**, not just repeat-insensitive:
- Carry a monotonic **version/sequence from the source** (row version, LSN, event seq) and apply conditionally: `UPDATE ... WHERE version < :v`. Stale events match zero rows.
- Prefer **commutative** state (set union, max, CRDT-ish counters) over "set to this value".
- If neither is possible, you must **park the whole key** on failure (stop the partition or a per-key queue) rather than skipping ahead — that is the real cost of strict per-key ordering.

## Q zh
你的 handler 是幂等的，topic 由 entity keyed，但一个 profile 偶尔恢复到旧地址。为什么幂等性不够，修复是什么？

## A zh
Per-partition 顺序仅对**作为存储的流**成立，不是你的 handler *观察*的顺序。任何这些重新排序一个 key 的事件：失败消息在退避后重试，同时后续消息继续；DLQ redrive 重放小时后；rebalance 从更旧的 offset 重放；或单个 partition 内的并发 handler 线程。幂等性使重复无害；它不会使**陈旧的**写无害。

修复 — 让 handler **顺序不敏感**，不仅仅是重复不敏感：
- 从源携带单调**版本/序列**（行版本、LSN、事件 seq），条件应用：`UPDATE ... WHERE version < :v`。陈旧事件匹配零行。
- 优选**交换律**状态（set union、max、CRDT-ish counter）而不是"设置为这个值"。
- 如果都不可能，失败时你必须**停泊整个 key**（停止 partition 或 per-key 队列）而不是跳过 — 那是严格 per-key 顺序的真正代价。
