---
id: txn-never-nested
node: txn.acid-guarantees
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中，外层事务能否回滚一个已经提交的「内层」事务？为什么？

## A
不能。Snowflake 的事务从不嵌套（nested）：每条 SQL 语句只属于一个事务，存储过程里开启的事务是独立的「作用域事务（scoped transaction）」，而不是外层事务的子事务。因此外围的 ROLLBACK 不会撤销被包含事务已完成的 COMMIT，外围的 COMMIT 也不会让一个已回滚的内部事务生效。
