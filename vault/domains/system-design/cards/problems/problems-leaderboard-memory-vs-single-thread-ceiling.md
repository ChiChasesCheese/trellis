---
id: problems-leaderboard-memory-vs-single-thread-ceiling
node: problems.realtime.leaderboard
type: qa
step: 1
tags: [grown]
---
## Q
In a leaderboard design serving 150 million total accounts where a Redis sorted set costs roughly 112 bytes per member (skip-list-and-hash-table overhead plus the member id and score), the whole leaderboard fits in about 17GB of memory on a single node — comfortably within one primary's RAM. At a peak of roughly 41,700 combined reads and writes per second, is memory or throughput the constraint that actually matters here, and does either one force sharding at this scale?

## A
Memory and throughput are separate constraints, and throughput is the one that matters for this workload, not memory — 17GB is trivial for a single node to hold. But throughput doesn't force sharding at this particular scale either: because Redis executes commands on a single thread, one primary has a hard ceiling on sustained operations per second — conservatively, on the order of 50,000 op/s once you derate a simple-command benchmark baseline for sorted sets' O(log N) cost plus replication and persistence overhead — and a peak of ~41,700 combined ops/sec still fits under that ceiling with some headroom, especially once writes (the only traffic that must land on one primary) are separated from reads (which read replicas can absorb). Sharding only earns its keep once write throughput itself grows enough to exceed a single primary's ceiling; it's a request-rate problem, not a data-size problem, and shouldn't be assumed just because the player count sounds large.

## Q zh
在一个服务 1.5 亿总账号的排行榜设计中，Redis 有序集合每条记录大约 112 字节开销（跳表+哈希表开销加上成员 id 和分数），整个排行榜在单节点上只占约 17GB 内存——一个主节点的内存轻松装得下。在峰值读写合计约每秒 41,700 次的情况下，真正卡脖子的是内存还是吞吐？这两者中有没有哪一个在这个规模下就已经逼出分片？

## A zh
内存和吞吐是两个独立的约束，对这个工作负载来说真正卡脖子的是吞吐，不是内存——17GB 对单节点来说微不足道。但即便是吞吐，在这个具体规模下也还没有逼出分片：因为 Redis 对命令执行是单线程的，一个主节点在每秒可持续处理的操作数上有一个硬上限——保守估计约为 50,000 次/秒（把简单命令的基准吞吐打折，为有序集合 O(log N) 的开销以及复制、持久化的生产成本留出余量）——而约每秒 41,700 次的峰值合计吞吐仍然在这个上限之内、留有余量，尤其是在把写入（唯一必须落到一个主节点上的流量）和读取（可以由只读副本承担）分开之后。只有当写入吞吐本身增长到超过单个主节点的上限时，分片才真正值回成本；这是一个请求速率问题，不是数据规模问题，不应该仅仅因为玩家数量听起来很大就默认需要分片。
