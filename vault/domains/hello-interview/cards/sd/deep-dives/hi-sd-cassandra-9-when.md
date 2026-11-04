---
id: hi-sd-cassandra-9-when
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 9
---
## Q
**何时选 Cassandra，何时不选**｜系统设计 · 深入专题

面试里什么时候该用 Cassandra？什么时候不该？

## A
**要点。** 适合：

- 优先可用性而非一致性，且需要极高扩展性。
- 写吞吐很高（LSM 树写优化），读也能保持快。
- 宽列、稀疏或灵活 schema。
- 有几个明确的访问模式，schema 可以围绕它们设计。

不适合：

- **严格一致或事务不适合：** 要求严格一致或需要事务（只有分区内单行原子性，没有 ACID）。
- 需要复杂查询：多表 JOIN、临时聚合（ad hoc aggregation）。

**对照。** 与 DynamoDB 血缘相近（都源于 Dynamo 论文，键模型类似）：后者全托管并有事务选项，前者可自己运维、有更多调节旋钮。

**面试用法。** 说出它时要立刻说清分区键怎么选、分区会多大、聚簇键怎么排，这是它的建模风险所在；被追问内部原理时，能讲清一致性哈希、LSM 树、QUORUM 三件事就足够。
