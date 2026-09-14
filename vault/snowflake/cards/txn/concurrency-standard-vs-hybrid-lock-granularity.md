---
id: concurrency-standard-vs-hybrid-lock-granularity
node: txn.optimistic-concurrency-conflicts
type: qa
tags: [grown]
---
## Q
两个会话分别 UPDATE 同一张表里完全不同的两行。在 Snowflake 标准表和混合表（hybrid table）上，结果分别是什么？

## A
标准表上，UPDATE/DELETE/MERGE 的锁作用在整张表这一资源上，第二个 UPDATE 通常要等第一个事务提交或回滚才能继续，即使行不重叠。混合表面向 OLTP（联机事务处理），锁加在单独的行上，只有操作同一行的 UPDATE/DELETE/MERGE 才会互相阻塞，改不同行的语句可以并行推进。
