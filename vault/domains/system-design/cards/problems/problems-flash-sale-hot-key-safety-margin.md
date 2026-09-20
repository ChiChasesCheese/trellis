---
id: problems-flash-sale-hot-key-safety-margin
node: problems.commerce.flash-sale
type: qa
step: 1
tags: [grown]
---
## Q
In a flash sale with 1,000,000 buyers and a 10-second window, all purchase attempts race for the same single inventory counter key. Using Redis's own published single-instance benchmark (about 180,180 SET requests/sec, unpipelined, on bare metal), what is the safety margin against the naive unthrottled purchase-attempt peak, and what does that number imply about admission control?

## A
The naive peak is 1,000,000 / 10 = 100,000 purchase attempts/sec; 180,180 / 100,000 ≈ 1.8x — only about an 1.8x margin over a single Redis instance's own documented throughput ceiling. That margin is far too thin to trust in production (network jitter, GC pauses, or a slow neighboring command could exhaust it), which is why admission control in front of the inventory key isn't an optional optimization here — it's what keeps the one key that can't be sharded away from ever seeing the raw peak in the first place.

## Q zh
在一场 100 万买家、10 秒窗口的秒杀里，全部购买尝试都争抢同一个库存计数器 key。用 Redis 官方公布的单实例基准（裸机、不开 pipelining，`SET` 约 180,180 请求/秒），相对未经任何限流的裸购买峰值，安全边际是多少？这个数字说明了什么？

## A zh
裸峰值是 1,000,000 / 10 = 100,000 次购买尝试/秒；180,180 / 100,000 ≈ 1.8 倍——单个 Redis 实例的官方吞吐上限相对裸峰值只有约 1.8 倍的余量，这个余量在生产环境里（网络抖动、GC 暂停、慢命令）远不够安全。这正是为什么库存 key 前面的准入控制不是可选的性能优化，而是让这个无法被分片稀释的唯一热 key 永远见不到裸露峰值的必要手段。
