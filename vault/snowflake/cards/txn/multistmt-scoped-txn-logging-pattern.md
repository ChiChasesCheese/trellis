---
id: multistmt-scoped-txn-logging-pattern
node: txn.multi-statement-transactions
type: qa
source: snowflake-docs
---
## Q
如何在 Snowflake 中实现「无论业务事务成功还是回滚，都要保留一条尝试记录」的审计日志？依赖的是什么机制？

## A
把写日志的 INSERT 放进一个单独的存储过程事务里。Snowflake 把存储过程内部开启的事务视为独立的作用域事务（scoped transaction，又称自治作用域事务），而不是外层事务的嵌套子事务：它自己的 COMMIT 不会被外层的 ROLLBACK 撤销。于是业务数据表因回滚保持为空，日志表中的记录却被保留下来。
