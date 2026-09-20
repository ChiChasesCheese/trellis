---
id: problems-tinder-match-gate-safety-margin
node: problems.social.tinder
type: qa
step: 2
tags: [grown]
---
## Q
In a dating app's match-detection path, the atomic check-and-set that tests whether the other user has already right-swiped runs on every right swipe, not just on confirmed matches. If right swipes are 20% of a 52,083 peak-QPS swipe stream, and a single Redis instance's official unpipelined benchmark is about 180,180 SET requests/sec, what is the safety margin, and how does it compare to a flash-sale's single hot inventory key at only about 1.8x margin?

## A
Right-swipe peak QPS ≈ 52,083 × 0.20 ≈ 10,417; 180,180 / 10,417 ≈ 17.3x margin — an order of magnitude healthier than the flash sale's roughly 1.8x margin on its single inventory key. The lesson is that not every 'atomic operation on one key' scenario needs special hot-key handling like replication or sharding: the match-detection load here (thousands to ~10K QPS) is one to two orders of magnitude below a flash sale's everyone-races-one-key spike, so a single Redis instance running the canonical-pair-key check-and-set is sufficient at this scale without extra complexity.

## Q zh
在约会应用的匹配判定路径里，检查对方是否已经右滑过自己的原子 check-and-set 发生在**每一次**右滑上，而不只是发生在确认的匹配上。如果右滑占 52,083 峰值滑动 QPS 的 20%，而单个 Redis 实例的官方无 pipelining 基准约为 180,180 次 SET 请求/秒，安全边际是多少？这和秒杀设计里单一库存热 key 只有约 1.8 倍的边际相比说明了什么？

## A zh
右滑峰值 QPS ≈ 52,083 × 0.20 ≈ 10,417；180,180 / 10,417 ≈ 17.3 倍安全边际——比秒杀设计里库存热 key 约 1.8 倍的边际健康一个数量级。这说明的道理是：不是所有「对同一个 key 做原子操作」的场景都需要靠冗余复制或分片这类热 key 特殊处理——这里匹配判定的负载（几千到约一万 QPS）比秒杀那种「全网同时抢一个 key」的峰值低一到两个数量级，在这个规模下单个 Redis 实例跑 canonical pair key 的 check-and-set 就足够，不需要额外复杂度。
