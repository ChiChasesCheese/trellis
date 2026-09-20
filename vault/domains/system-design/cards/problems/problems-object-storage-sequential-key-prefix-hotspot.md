---
id: problems-object-storage-sequential-key-prefix-hotspot
node: problems.foundations.object-storage
type: qa
step: 7
tags: [grown]
---
## Q
A customer of an object storage service writes keys with a strictly increasing timestamp prefix, like `2026-09-20/log-000001`, `2026-09-20/log-000002`, and so on. Even though the metadata service has 512 hash-based shards, why does this key pattern still overload a small number of shards instead of spreading load evenly, and what's the fix?

## A
Sequential, monotonically increasing prefixes mean that at any given moment, almost all newly written keys share the same narrow, currently-active prefix range - and whatever shard(s) that narrow range hashes to (or, in a range-partitioned index used for listing, whatever shard owns that lexicographic range) absorb effectively all of the current write traffic, while the other 500+ shards sit nearly idle. Having many shards doesn't help because the problem isn't total capacity, it's that all writes are concentrated on the same few keys at any point in time. The fix is to mix a hash of the key (e.g. the first few hex digits of a hash) into the prefix itself, so consecutively-written objects land on effectively random, spread-out shards instead of a single hot one.

## Q zh
一个对象存储服务的客户用严格递增的时间戳前缀写 key，如 `2026-09-20/log-000001`、`2026-09-20/log-000002` 依次类推。即使元数据服务有 512 个基于哈希的分片，为什么这种 key 模式仍然会把负载集中到少数几个分片上，而不是均匀分散？修复方法是什么？

## A zh
递增前缀意味着在任何一个时刻，几乎所有新写入的 key 都共享同一个狭窄的、当前活跃的前缀范围——这个狭窄范围无论哈希到哪个分片（或在用于列举的范围分片索引中，无论哪个分片拥有这段字典序范围），都会吸收几乎全部当前写入流量，而其余 500 多个分片几乎空闲。分片数多不能解决这个问题，因为问题不在于总容量，而在于任何时刻的写入都集中在同几个 key 上。修复方法是把 key 的哈希值（例如哈希的前几位十六进制数字）混入前缀本身，让连续写入的对象落在实际上随机、分散的分片上，而不是集中在一个热点上。
