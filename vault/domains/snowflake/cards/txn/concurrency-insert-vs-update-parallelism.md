---
id: concurrency-insert-vs-update-parallelism
node: txn.optimistic-concurrency-conflicts
type: qa
tags: [grown]
---
## Q
在 Snowflake 标准表上，为什么多个会话并发 INSERT 或 COPY 通常能同时进行，而并发的 UPDATE、DELETE、MERGE 却会互相排队？

## A
Snowflake 的微分区（micro-partition，不可变的列式数据文件）从不就地修改。INSERT 和 COPY 大多只是写出新分区，再把它们加进新的表版本，不改写任何已有分区，因此彼此之间没有需要协调的重叠。UPDATE、DELETE、MERGE 则要读出现有分区、写出替换后的新分区并移除旧分区；两个这样的写入者若同时基于同一旧版本各自改写，后提交的会覆盖掉前者的结果，所以它们持有锁（lock），通常不能与其他 UPDATE/DELETE/MERGE 并行。
