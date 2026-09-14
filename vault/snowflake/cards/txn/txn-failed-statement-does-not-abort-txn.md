---
id: txn-failed-statement-does-not-abort-txn
node: txn.acid-guarantees
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 的一个显式事务（transaction）里执行了三条 INSERT，其中第二条因数据类型错误失败，随后仍执行了 COMMIT。表里最终会有哪些行？这说明 Snowflake 的原子性（atomicity）具体保证的是什么？

## A
第一条和第三条 INSERT 的行都会被提交，只有失败的那条语句自己的改动被回滚。Snowflake 保证事务作为一个整体被提交或回滚，但并不等于「整体成功或整体失败」：语句失败后事务仍保持活跃，由调用者决定 COMMIT 还是 ROLLBACK。若希望语句出错时整个事务被中止，需要在会话或账户级设置 `TRANSACTION_ABORT_ON_ERROR` 参数。
