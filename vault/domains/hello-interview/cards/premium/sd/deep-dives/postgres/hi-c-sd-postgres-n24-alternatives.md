---
id: hi-c-sd-postgres-n24-alternatives
node: sd.deep-dives.postgres.notes
type: qa
step: 24
---
## Q
**PostgreSQL · 什么时候该考虑别的数据库**｜摘要 · 必会

哪三种情况下 PostgreSQL 不是最好的选择？分别该换什么？

## A
- **极端写吞吐（每秒百万级）：** 每次写都要 WAL 和索引更新，I/O 成为瓶颈，即使分片，跨很多节点协调写入也增加复杂度与延迟。可考虑 Cassandra（事件流）或 Redis（实时计数）。
- **全球多区域主动-主动：** PostgreSQL 是单主架构，一个区域是主，其余只能当只读副本；多主写入会带来一致性和冲突解决难题，跨区域同步复制延迟又高。可考虑 CockroachDB（全球 ACID）、Cassandra（全球最终一致）、DynamoDB 全局表。
- **纯键值访问：** 只按键存取，没有连接和复杂查询，MVCC、WAL 和查询规划器的开销就是浪费。可考虑 Redis、DynamoDB、Cassandra。
- **注意：** 仅仅因为"要扩展"不是换库的好理由，PostgreSQL 靠合理设计能撑很大规模。
