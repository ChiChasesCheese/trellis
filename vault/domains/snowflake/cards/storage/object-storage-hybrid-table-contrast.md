---
id: object-storage-hybrid-table-contrast
node: storage.object-storage-backend
type: qa
source: snowflake-docs
---
## Q
需要低延迟单行读写、行锁和唯一性约束的事务型负载，为什么不适合用普通 Snowflake 表的压缩列式存储？Snowflake 提供了什么替代？

## A
普通 Snowflake 表把数据组织成压缩列式格式、自动切分为微分区（micro-partition）存放在云存储中，这种布局为批量扫描的分析型查询优化，而不是为按键随机读写单行设计。替代方案是 hybrid table（混合表）：它使用基于索引的随机读写，优化低延迟和高吞吐，支持行锁（row locking），并强制唯一性和参照完整性约束，可与普通表配合用于事务与分析合一的 Unistore 负载。
