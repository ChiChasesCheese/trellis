---
id: hi-c-sd-dealing-with-contention-n12-other-stores
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 12
---
## Q
**处理竞争 · 这些技术在 SQL 之外的对应物与适用边界**｜摘要 · 必会

这五种手段在 DynamoDB、Redis、etcd 里分别对应什么？什么情况下它们都不管用？

## A
- **条件写：** DynamoDB `ConditionExpression`、Redis `SET NX`、Cassandra 轻量事务、HTTP `If-Match`。
- **乐观并发：** HTTP ETag、etcd revision、DynamoDB 版本属性。
- **悲观锁：** 互斥锁，或持有期间做决定的分布式锁。
- **可串行化：** 基本只有关系数据库提供，别处要把约束折叠到一个可检查的单元。
- **分布式锁：** 带 TTL 的预留行、Redis `SET NX EX`、ZooKeeper / etcd 租约。
- **前提：** 争抢的资源必须放在同一个权威存储里，九成情况下做得到。两种情况出了这个模式：一次操作必须原子地跨多个服务或分片（分布式事务）；同一条记录能在多处写入（多主或无主复制），要靠最后写入胜出、向量时钟或 CRDT 解决冲突。
