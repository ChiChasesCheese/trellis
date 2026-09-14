---
id: concurrency-deadlock-victim-rule
node: txn.optimistic-concurrency-conflicts
type: qa
tags: [grown]
---
## Q
两个显式多语句事务在两张表上交叉加锁形成死锁（deadlock）后，Snowflake 如何处理？应用代码需要做什么？

## A
Snowflake 会检测死锁（检测可能需要一些时间），并选择死锁中最新的那条语句作为牺牲者将其回滚。注意只回滚这条语句，事务本身仍然活跃，应用必须显式决定 COMMIT 还是 ROLLBACK 整个事务，并通常重试。标准表上的自动提交 DML 不会死锁，只有显式开启、包含多条语句的事务才可能发生。
