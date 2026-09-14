---
id: async-log-ordering-partitions
node: async.log
type: qa
---
## Q
What ordering does Kafka actually guarantee, and how do you use that to keep per-entity ordering at scale?

## A
Ordering is guaranteed **only within a partition** — there is no total order across a topic.

- Choose the **partition key = entity id** (user id, account id, order id) so all events for one entity land in one partition, in order.
- Cross-entity order is undefined; if you need it, you have a design problem, not a config problem.
- Beware: changing partition count re-maps keys, breaking per-key ordering across the boundary — plan partitions up front or migrate deliberately.

## Q zh
Kafka 实际上保证什么顺序，如何使用它来保持大规模的 per-entity 顺序？

## A zh
顺序**只在 partition 内保证** — topic 中没有全局顺序。

- 选择 **partition key = entity id**（user id、account id、order id），所以一个实体的所有事件落入一个 partition，按顺序排列。
- 跨实体顺序未定义；如果需要，你有设计问题而不是配置问题。
- 警告：改变 partition 数量会重新映射 key，破坏边界处的 per-key 顺序 — 提前规划 partition 或故意迁移。
