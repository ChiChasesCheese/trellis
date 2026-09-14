---
id: isolation-readers-never-deadlock
node: txn.snapshot-isolation
type: qa
source: snowflake-docs
---
## Q
为什么在 Snowflake 中大量并发执行自动提交（autocommit）的 SELECT 查询永远不会产生死锁（deadlock），而显式多语句事务却可能？

## A
SELECT 语句总是只读的，不获取修改资源所需的锁（lock），读的是已提交版本，所以并发读之间、读与写之间都不会互相等待，也就不可能形成循环等待。死锁只可能出现在显式开启、每个事务包含多条修改语句的场景：事务 A 持有表 X 的锁等 Y，事务 B 持有 Y 等 X。
