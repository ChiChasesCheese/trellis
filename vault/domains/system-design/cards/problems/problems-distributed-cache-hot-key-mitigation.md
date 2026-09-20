---
id: problems-distributed-cache-hot-key-mitigation
node: problems.foundations.distributed-cache
type: qa
step: 5
tags: [grown]
---
## Q
In a distributed cache, why does adding more shards not help when a single key becomes disproportionately hot, and what mitigation does?

## A
Sharding only guarantees that different keys land on different nodes — it guarantees nothing about how much traffic any one key's own single node absorbs. No matter how many shards exist, one hot key still lands on exactly one node, so adding shards dilutes nothing for that key. The mitigation is detecting the hot key by sampling per-key request rates, then replicating its value under several suffixed copies (`key#1`...`key#R`) stored on different nodes; readers pick a suffix at random, spreading the hot key's read load across R nodes at the cost of R-way invalidation fan-out and brief cross-copy inconsistency.

## Q zh
在分布式缓存中，当单个 key 的流量异常集中时，为什么增加分片数没有帮助？什么方法有用？

## A zh
分片只保证不同的 key 落在不同节点上——对某一个 key 自己所在的那个节点要承受多少流量毫无保证。不管分片数多少，这个热 key 依然只落在恰好一个节点上，增加分片对这个 key 而言没有任何稀释作用。缓解办法是通过采样每个 key 的请求频率来探测热 key，然后把它的值复制成若干个带后缀的副本（`key#1`...`key#R`）分别存到不同节点，读请求随机选一个后缀读取，把这个热 key 的读流量摊到 R 个节点上，代价是失效时要向全部 R 个副本广播，且短时间内各副本之间可能不完全一致。
