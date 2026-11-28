---
id: hi-c-sd-postgres-x10-choose-store
node: sd.deep-dives.postgres.exam
type: qa
step: 9
---
## Q
**PostgreSQL · 三个场景该不该离开 PostgreSQL**｜考点 · 必会

(1) 全球实时多人游戏的玩家位置每秒产生数百万次写入；(2) 一个中型电商的订单、库存、用户；(3) 一个只按会话 ID 存取会话数据的服务。分别选什么？

## A
- **(1) 离开 PostgreSQL：** 每秒数百万写入，WAL 和索引更新是瓶颈，分片协调也复杂。内存键值存储或 Cassandra 更合适，位置这类数据也可以容忍丢最近的更新。
- **(2) 留在 PostgreSQL：** 订单、库存、用户有明确关系，需要事务和外键，也要复杂查询。规模用复制、索引和分区足够。
- **(3) 用键值存储：** 只按键存取，用不到关系、连接和查询规划器，PostgreSQL 的 MVCC 和 WAL 开销是浪费；Redis 或 DynamoDB 都可以。
- **判断顺序：** 数据关系与一致性需求，其次访问模式，最后规模。仅仅因为"会长大"不是换库的理由。
