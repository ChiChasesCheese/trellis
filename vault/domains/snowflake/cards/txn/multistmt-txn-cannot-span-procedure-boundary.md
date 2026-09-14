---
id: multistmt-txn-cannot-span-procedure-boundary
node: txn.multi-statement-transactions
type: qa
source: snowflake-docs
---
## Q
开发者在调用存储过程（stored procedure）之前执行 `BEGIN TRANSACTION`，打算在存储过程内部 COMMIT。为什么这样会报错？正确的写法有哪两种？

## A
Snowflake 要求一个事务不能一部分在存储过程内、一部分在外，也不能在一个过程里开始、在另一个过程里结束；每个 BEGIN 必须在同一作用域内配对 COMMIT 或 ROLLBACK。过程内没有配对 BEGIN 的 COMMIT 会报错；过程结束时仍活跃的事务会报错并被回滚。正确做法：要么 BEGIN 在调用前、COMMIT 在调用后，整个过程包在事务里；要么 BEGIN 和 COMMIT 都写在过程内部。
