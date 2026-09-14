---
id: txn-detached-transaction-auto-abort
node: txn.acid-guarantees
type: qa
source: snowflake-docs
---
## Q
客户端在事务提交前网络断开，事务留在「分离（detached）」状态并继续持有表上的锁。Snowflake 什么时候会自动中止它？在那之前怎么处理？

## A
如果该事务阻塞了其他事务对同一张表获取锁、并且空闲了 5 分钟，会被自动中止并回滚；如果它没有阻塞别人，则在存活超过 4 小时后被自动中止回滚（访问混合表（hybrid table）的事务空闲 5 分钟即中止）。在自动中止之前，发起该事务的用户或账户管理员可以调用 `SYSTEM$ABORT_TRANSACTION` 手动中止它，释放锁。
