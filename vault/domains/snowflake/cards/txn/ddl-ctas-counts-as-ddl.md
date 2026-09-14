---
id: ddl-ctas-counts-as-ddl
node: txn.ddl-as-transaction
type: qa
source: snowflake-docs
---
## Q
把 `CREATE TABLE AS SELECT`（CTAS，建表并写入查询结果）放进一个显式事务中，指望出错时可以整体回滚，这为什么行不通？

## A
在 Snowflake 的事务语义里 CTAS 属于 DDL（数据定义语句），而每条 DDL 都会先隐式提交当前活跃事务，然后作为自己独立的事务执行。因此 CTAS 之前的改动会被提前提交，CTAS 本身也无法被后续 ROLLBACK 撤销。显式事务应只包含 DML 和查询语句。
