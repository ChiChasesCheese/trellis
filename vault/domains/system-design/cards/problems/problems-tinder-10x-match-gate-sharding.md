---
id: problems-tinder-10x-match-gate-sharding
node: problems.social.tinder
type: qa
step: 8
tags: [grown]
---
## Q
In a dating app's match-detection design, daily active users grow 10x (from 10 million to 100 million) with the same behavior mix. Right-swipe peak QPS grows proportionally from about 10,417 to about 104,167. Given a single Redis instance's official benchmark of about 180,180 unpipelined SET requests/sec, what happens to the safety margin, and what design change does this force?

## A
The safety margin narrows from about 17.3x (180,180 / 10,417) down to about 1.73x (180,180 / 104,167) — a margin thin enough to be in the same danger zone as a flash sale's roughly 1.8x margin on its single hot inventory key, where any jitter, GC pause, or slow neighboring command could exhaust it. This forces the match gate to move from a single Redis instance to a Redis cluster sharded by a hash of the canonical pair key, spreading the check-and-set load across multiple shards the same way a flash-sale platform spreads different SKUs' independent inventory counters across shards at its own 100x scale.

## Q zh
在约会应用的匹配判定设计里，日活用户增长 10 倍（从 1000 万到 1 亿），行为比例不变。右滑峰值 QPS 相应从约 10,417 增长到约 104,167。已知单个 Redis 实例的官方基准约为 180,180 次无 pipelining SET 请求/秒，安全边际会怎样变化？这会迫使设计做出什么改变？

## A zh
安全边际从约 17.3 倍（180,180 / 10,417）收窄到约 1.73 倍（180,180 / 104,167）——这个边际薄到已经进入和秒杀设计里单一库存热 key 约 1.8 倍边际同样的危险区间，任何抖动、GC 暂停或慢命令都可能耗尽它。这迫使匹配网关从单个 Redis 实例升级为按 canonical pair key 的哈希分片的 Redis 集群，把 check-and-set 负载分摊到多个分片上，就像秒杀平台在自己的 100 倍规模上把不同 SKU 各自独立的库存计数器分散到不同分片一样。
