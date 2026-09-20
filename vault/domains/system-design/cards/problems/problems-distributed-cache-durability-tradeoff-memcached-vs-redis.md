---
id: problems-distributed-cache-durability-tradeoff-memcached-vs-redis
node: problems.foundations.distributed-cache
type: qa
step: 7
tags: [grown]
---
## Q
In a distributed cache, classic Memcached deployments replicate nothing across nodes while Redis Cluster deployments typically pair each shard with an async replica. What does each choice trade off, and why doesn't the 'better' choice generalize?

## A
Unreplicated Memcached loses a node's entire cached content on failure — that key range's hit rate drops to zero until it re-warms — but avoids doubling memory usage. Redis Cluster's replica-per-shard setup keeps hit rate nearly unaffected by a single node failure (the replica is promoted automatically), but costs double the memory for the same working set. Neither is universally better: since caching accepts data loss by design, the question is whether the spare memory capacity is worth spending on replicas versus more working-set headroom — and that answer depends on whether the deployment is already throughput-bound (where memory is comparatively cheap to spend) or already memory-bound (where doubling it is expensive).

## Q zh
在分布式缓存中，经典 Memcached 部署不在节点间做任何复制，而 Redis Cluster 部署通常给每个分片配一个异步复制的从节点。这两种选择各自的代价是什么？为什么「更好」的那个选择不能一概而论？

## A zh
不做复制的 Memcached 在节点故障时会丢失该节点的全部缓存内容——对应 key 范围的命中率归零直到重新预热——但避免了双倍内存开销。Redis Cluster 的每分片配从节点方案让命中率在单节点故障时几乎不受影响（从节点自动被提升接管），但要为同样的工作集付出双倍内存成本。两者没有绝对的优劣：既然缓存在设计上就接受数据丢失，真正的问题是这部分富余内存该花在副本上还是花在更大的工作集空间上——答案取决于这套部署本身已经是吞吐瓶颈（内存相对富余）还是已经是内存瓶颈（双倍内存代价高昂）。
