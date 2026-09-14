---
id: concurrency-lock-timeout-failure
node: txn.optimistic-concurrency-conflicts
type: qa
tags: [grown]
---
## Q
夜间的 MERGE 作业偶尔报「锁等待超时」失败。背后发生了什么？排查时应该看哪些视图？

## A
被阻塞的语句会一直等待所需的锁，直到拿到锁或超过 `LOCK_TIMEOUT` 参数设定的秒数后超时失败；锁只在持有者事务 COMMIT 或 ROLLBACK 时释放。典型原因是另一个长事务（或客户端断开后遗留的分离事务）在同一张表上持有 UPDATE/DELETE/MERGE 锁。排查时先在 `QUERY_HISTORY` 中找 `TRANSACTION_BLOCKED_TIME` 高的查询，再用 `LOCK_WAIT_HISTORY` 找出持锁的阻塞事务及其语句。
