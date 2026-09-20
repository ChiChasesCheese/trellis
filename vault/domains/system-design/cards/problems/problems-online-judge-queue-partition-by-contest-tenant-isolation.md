---
id: problems-online-judge-queue-partition-by-contest-tenant-isolation
node: problems.realtime.online-judge
type: qa
step: 6
tags: [grown]
---
## Q
In an online judge design, why does the judge queue partition submissions by contestId rather than randomly, and how does this same tenant-isolation idea need to evolve at 10x scale (contest registrants growing from 100K to 1M, burst concurrency from ~533 to ~5,300 sandboxes)?

## A
Partitioning by contestId concentrates one contest's submissions on a small number of partitions, so the judge workers consuming those partitions get a higher local cache hit rate for that contest's test data (already pre-warmed onto their local disk) instead of spreading requests thin across every worker. At 10x scale, a single shared queue and worker pool is no longer enough — a single contest large enough to saturate it would delay judging for every other concurrent contest or practice submission — so the design needs physically separate queues and worker pools per tenant class (e.g. paid timing-sensitive contests vs. free practice), not just soft priority fields on a shared queue.

## Q zh
在一个在线判题系统设计中，为什么判题队列按 contestId 而不是随机分区？在 10 倍规模演进下（竞赛报名人数从 10 万到 100 万，爆发期并发沙箱需求从约 533 涨到约 5,300），这个租户隔离的思路要怎么进一步演进？

## A zh
按 contestId 分区能让同一场竞赛的提交集中落在少数几个分区上，消费这些分区的判题工作节点对该场竞赛的测试数据（已经预热在本地磁盘上）有更高的缓存命中率，而不是把请求稀释到所有工作节点上。到了 10 倍规模，单一共享队列和工作节点池不再够用——一场足够大的竞赛就能把它占满，拖慢其他并发竞赛或练习提交的判题——因此需要按租户类型（比如对计时敏感的付费竞赛 vs. 免费练习）做物理隔离的独立队列和工作节点池，而不只是在共享队列上加一个软优先级字段。
