---
id: multistmt-best-practice-explicit-with-autocommit
node: txn.multi-statement-transactions
type: qa
source: snowflake-docs
---
## Q
为什么推荐「保持 AUTOCOMMIT 开启 + 用显式 BEGIN TRANSACTION」，而不是关闭 AUTOCOMMIT 依靠隐式事务？

## A
显式事务让人一眼看出事务从哪里开始、到哪里结束，便于把 BEGIN 与 COMMIT/ROLLBACK 配对。关闭 AUTOCOMMIT 后，任何一条 DML 都会悄悄开启隐式事务，若在存储过程末尾忘记提交，事务会被隐式回滚，造成意外丢数据。另外应避免连续写多个 BEGIN TRANSACTION：事务已活跃时多余的 BEGIN 会被忽略，只会让配对更难读懂。
