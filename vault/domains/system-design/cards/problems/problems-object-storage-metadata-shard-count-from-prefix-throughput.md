---
id: problems-object-storage-metadata-shard-count-from-prefix-throughput
node: problems.foundations.object-storage
type: qa
step: 1
tags: [grown]
---
## Q
An object storage design stores 1 exabyte of logical data at an average object size of 256KB (about 3.8 trillion objects) and must sustain a peak of 2,314,815 GET requests/second. Given a real, documented per-key-prefix throughput ceiling of 5,500 GET/HEAD requests/second, why does this alone prove the metadata service cannot be a single database, and what minimum shard count does it imply?

## A
Dividing the peak GET rate by the per-prefix ceiling gives 2,314,815 / 5,500 ≈ 421 - meaning even a metadata layer that could sustain the documented per-prefix throughput on every one of its partitions would still need at least about 421 independent partitions just to survive peak read traffic, before even accounting for the roughly 763TB the metadata itself occupies (3.8 trillion objects x ~200 bytes each) which no single-machine database can hold. This makes the metadata service a distributed, sharded system by necessity, not a design preference; a design would round up to a power of two like 512 shards for simpler hash-based routing.

## Q zh
一个对象存储设计存储 1 EB 逻辑数据，平均对象大小 256KB（约 3.8 万亿个对象），需要支撑峰值 2,314,815 GET 请求/秒。已知一个真实、有文档记载的单 key 前缀吞吐上限是 5,500 GET/HEAD 请求/秒，为什么光凭这一点就能证明元数据服务不可能是单一数据库，它暗示的最小分片数是多少？

## A zh
用峰值 GET 速率除以单前缀上限：2,314,815 / 5,500 ≈ 421——意味着即使每个分区都能跑到文档给出的单前缀上限，也至少需要约 421 个独立分区才能扣住峰值读流量，还没算元数据本身约 763TB（3.8 万亿个对象 × 约 200 字节）——这个体量没有任何单机数据库能装下。这使得元数据服务必然是一个分布式分片系统，而不是设计偏好；实际设计会向上取整到 2 的幂（如 512 个分片）以简化基于哈希的路由。
