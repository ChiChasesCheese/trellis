---
id: storage-scaling-ladder
node: storage.relational.operations
type: qa
---
## Q
Your single Postgres is saturating. Give the escalation ladder in order, and the signal that forces each step.

## A
1. **Tune first**: indexes, query plans, caching, connection pooling — most "DB is slow" cases end here.
2. **Bigger box**: vertical scaling is boring and works to surprisingly large sizes (hundreds of GB RAM, NVMe).
3. **Read replicas**: when read QPS dominates and some staleness is tolerable — writes still bottleneck on the primary.
4. **Federation / functional split**: separate DBs per service or domain when unrelated workloads contend.
5. **Sharding**: only when *write* volume or dataset size exceeds one primary — it costs cross-shard queries, transactions, and rebalancing forever.

Interview point: a single well-tuned Postgres is the right answer far longer than candidates assume.

## Q zh
你的单个 Postgres 饱和了。按顺序给出升级梯子，以及强制每一步的信号。

## A zh
1. **首先调整**：索引、查询计划、缓存、连接池化——大多数"DB 慢"情况在这里结束。
2. **更大的盒子**：垂直扩展是无聊的并在惊人大的大小工作（数百 GB RAM、NVMe）。
3. **读副本**：当读 QPS 占主导并某种陈旧是可容忍的——写仍在主库上受瓶颈。
4. **联邦/函数分割**：当不相关的工作负载竞争时的每服务或域的单独 DB。
5. **分片**：只有当**写**量或数据集大小超过一个主库——它花费跨分片查询、事务、永远重新平衡。

面试点：单个调整好的 Postgres 是候选人假设的更长时间的正确答案。
