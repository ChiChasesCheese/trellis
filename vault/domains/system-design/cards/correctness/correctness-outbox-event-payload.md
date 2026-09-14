---
id: correctness-outbox-event-payload
node: correctness.outbox
type: qa
---
## Q
Fat events vs thin events in an outbox: what does each carry, and what race does the thin style cause?

## A
- **Fat (event-carried state)**: the outbox row snapshots all needed state *as of the transaction* (`OrderPlaced` + items, amounts, addresses). Consumers are self-sufficient; no read-back. Cost: bigger rows, schema is a public contract you must version.
- **Thin (notification)**: just `order_id` + type; consumers call back to fetch details. Race: by the time the consumer reads, the entity has **changed or vanished** — it sees state from a *later* version than the event describes, or reads the same state twice across different events. It also re-couples consumers to the producer's API and adds read load.

Fintech default: **fat events** — the snapshot-at-commit is exactly what audit and downstream ledgers need.

## Q zh
outbox 中的胖事件 vs 瘦事件：各自携带什么，瘦方式导致什么竞态？

## A zh
- **胖（事件携带状态）**：outbox 行快照*交易时*所有需要的状态（`OrderPlaced` + 商品、金额、地址）。消费者自给自足；无回读。代价：更大的行，schema 是你必须版本化的公共契约。
- **瘦（通知）**：仅 `order_id` + 类型；消费者回调获取细节。竞态：消费者读时，实体**改变或消失** — 它看到*比事件描述更晚*版本的状态，或跨不同事件读同一状态两次。它也重新耦合消费者到生产者 API，加读负载。

Fintech 默认：**胖事件** — 提交时快照正是审计和下游账本需要的。
