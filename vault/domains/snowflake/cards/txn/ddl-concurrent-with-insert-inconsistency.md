---
id: ddl-concurrent-with-insert-inconsistency
node: txn.ddl-as-transaction
type: qa
source: snowflake-docs
---
## Q
一个会话在显式事务中持续向表 `events` INSERT 数据，另一个会话同时执行 `ALTER TABLE events ALTER COLUMN ... SET DATA TYPE ...`。这有什么风险？

## A
INSERT 和 COPY 大多只写新的微分区（micro-partition），通常可以与其他写入并行；但与同一对象上的 DDL 在不同会话中并发执行可能导致不一致。当 INSERT/COPY 处于显式事务中时，整个事务期间都应避免其他会话对同一对象执行 DDL，例如一边插入一边修改列的数据类型。
