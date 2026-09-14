---
id: concurrency-many-small-updates-antipattern
node: txn.optimistic-concurrency-conflicts
type: qa
tags: [grown]
---
## Q
一个微服务为每条业务事件对同一张 Snowflake 标准表发起一条小的 UPDATE，并发几十路。吞吐为什么上不去？有哪些改法？

## A
标准表上的 UPDATE 会锁住表，几十路小 UPDATE 实际上被串行化，每条还要改写整个受影响的微分区（micro-partition），吞吐受限于一次一条。常见改法：把事件先 INSERT 进暂存表（追加写可以并行），再周期性地用一条批量 MERGE 合并；或者对真正需要高并发单行读写的场景改用行级锁的混合表（hybrid table）。
