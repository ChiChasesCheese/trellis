---
id: ddl-own-transaction-implicit-commit
node: txn.ddl-as-transaction
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中执行 `BEGIN; INSERT INTO t VALUES (1); CREATE TABLE t2 (x INT); ROLLBACK;`，最后 t 里有没有这一行？t2 是否存在？为什么？

## A
两者都会保留。每条 DDL 都作为独立的事务执行；在活跃事务中遇到 DDL 时，Snowflake 先隐式提交当前事务（INSERT 因此被提交），再把 DDL 作为单独的事务执行完。等到 ROLLBACK 时，已没有活跃事务可回滚，所以 DDL 本身无法被回滚，INSERT 也已生效。
