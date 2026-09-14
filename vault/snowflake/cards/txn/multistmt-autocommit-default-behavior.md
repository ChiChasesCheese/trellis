---
id: multistmt-autocommit-default-behavior
node: txn.multi-statement-transactions
type: qa
source: snowflake-docs
---
## Q
Snowflake 默认 `AUTOCOMMIT = TRUE`。在这种设置下，显式事务之外的一条 UPDATE 如何被提交？如果它位于 `BEGIN TRANSACTION … ROLLBACK` 之间又会怎样？

## A
在显式事务之外，每条语句都被当作一个隐式的单语句事务：成功就自动提交，失败就自动回滚。AUTOCOMMIT（自动提交）不影响显式事务内部的语句：放在 `BEGIN TRANSACTION … ROLLBACK` 之间的 UPDATE 会随 ROLLBACK 一起被撤销，即使 AUTOCOMMIT 为 TRUE。
