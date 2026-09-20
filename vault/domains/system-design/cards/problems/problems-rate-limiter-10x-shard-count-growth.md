---
id: problems-rate-limiter-10x-shard-count-growth
node: problems.foundations.rate-limiter
type: qa
step: 8
tags: [grown]
---
## Q
In a rate limiter scaling from 100,000 to 1,000,000 average req/s (a 10x jump, same 3x peak factor and 3 checks per request), how many Redis shards (with 1.5x headroom, ~100,000 ops/shard/second) does exact central-store enforcement need at each scale, and what problem does this shard count growth create beyond raw compute capacity?

## A
At 100,000 avg req/s: peak checks/s = 100,000*3*3 = 900,000, needing ceil(900,000/100,000*1.5)=14 shards. At 1,000,000 avg req/s (10x): peak checks/s = 1,000,000*3*3 = 9,000,000, needing ceil(9,000,000/100,000*1.5)=135 shards. Beyond the raw operation throughput, 135 independent shards each become their own failure domain requiring monitoring, rebalancing, and capacity planning — at this point the operational complexity of managing a large, flat, hash-sharded cluster becomes a bigger problem than the compute itself, pushing toward automated shard-topology management rather than a manually maintained hash table.

## Q zh
在一个从均值 100,000 req/s 增长到 1,000,000 req/s（10 倍，峰值系数和每请求检查次数都不变）的速率限制器里，精确的中心存储执行方案在两个规模下各需要多少 Redis 分片（1.5 倍冗余，每分片约 100,000 次操作/秒）？这个分片数量的增长除了纯算力之外还带来了什么问题？

## A zh
均值 100,000 req/s 时：峰值检查量 = 100,000×3×3 = 900,000 次/s，需要 ceil(900,000/100,000×1.5)=14 个分片。均值 1,000,000 req/s（10 倍）时：峰值检查量 = 1,000,000×3×3 = 9,000,000 次/s，需要 ceil(9,000,000/100,000×1.5)=135 个分片。除了纯算力需求，135 个独立分片各自都是一个需要监控、再平衡和容量规划的独立故障域——这个规模下，管理一个庞大扁平的哈希分片集群本身的运维复杂度，已经超过了算力本身带来的问题，逼出自动化分片拓扑管理，而不是手工维护一张哈希表。
