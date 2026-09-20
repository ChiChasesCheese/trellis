---
id: problems-object-storage-10x-metadata-shards-4096
node: problems.foundations.object-storage
type: qa
step: 8
tags: [grown]
---
## Q
An object storage design planned for 512 metadata shards (sized for 421 shards' worth of peak GET traffic at 1x scale) grows 10x in traffic to a peak of 23,148,148 GET requests/second. Why isn't simply keeping the same 512 shards and giving each one more hardware a viable fix, and what shard count does the same per-shard throughput ceiling imply instead?

## A
The 5,500 GET/HEAD-per-second ceiling used to size shards is a ceiling for a single partitioned key range/prefix, not a number that scales by adding hardware behind an existing shard - it reflects how the request rate can be sustained for one logical partition of the keyspace, so the only way to sustain 10x the request rate is to have roughly 10x as many independent partitions. Dividing the new peak by the same per-shard ceiling gives 23,148,148 / 5,500 ≈ 4,209, so the design needs to grow to about 4,096 shards (the next convenient power of two) - and because the shard count itself is 8x larger, the routing layer that maps a key to its shard (previously trivial at 512 shards) also needs to change, typically by adding a level of indirection rather than a single flat hash table.

## Q zh
一个元数据服务按 512 个分片规划（1 倍规模下峰值 GET 流量需要 421 个分片的容量），流量增长 10 倍到峰值 23,148,148 GET 请求/秒。为什么单纯给现有 512 个分片堆硬件不是可行的修复方案，同样的单分片吞吐上限暗示的分片数应该是多少？

## A zh
用来确定分片大小的 5,500 GET/HEAD 每秒上限是单一分区好的 key 范围/前缀的上限，而不是一个可以通过给现有分片背后加硬件来提升的数字——它反映的是 key 空间单一逻辑分区能扣住的请求速率，所以扣住 10 倍请求速率的唯一办法是拥有大约 10 倍多的独立分区。用新峰值除以同样的单分片上限：23,148,148 / 5,500 ≈ 4,209，所以需要增长到约 4,096 个分片（下一个方便的 2 的幂）——且因为分片数本身变大了 8 倍，把 key 映射到分片的路由层（在 512 个分片时很简单）也需要变化，通常要加一层间接寻址而不是单层平坦哈希表。
