---
id: problems-food-delivery-hot-sku-sharded-counters
node: problems.geo.food-delivery
type: qa
step: 7
tags: [grown]
---
## Q
In a local-inventory delivery design, if a promoted item at a single micro-fulfillment center becomes a hot spot with a very high rate of concurrent checkout attempts against its inventory row, what happens even though each conditional decrement update is individually fast, and what's a standard fix?

## A
Even though each conditional-decrement update (subtract one if quantity is still above zero) completes quickly on its own, a very high rate of concurrent writes targeting the exact same row creates row-level lock contention, which becomes the bottleneck regardless of how fast any single update is. The standard fix is to shard that one inventory row into several sub-counters that can be decremented independently and concurrently, spreading the write contention across them; reading the total available quantity then requires summing across the shards, which is the trade-off this fix accepts in exchange for removing the single-row bottleneck.

## Q zh
在一个本地库存配送设计中，如果某个微仓里一件促销商品成为热点，大量并发的结账请求同时对它的库存行做扣减，即便每次条件扣减更新本身都很快，会发生什么？标准的解决办法是什么？

## A zh
即便每次条件扣减更新（数量仍大于零才扣减一件）本身完成得很快，极高速率的并发写入同时打到完全相同的一行，仍然会造成行级锁竞争，无论单次更新有多快，这都会成为瓶颈。标准的解决办法是把这一行库存拆分成多个可以独立、并发扣减的子计数器（分段库存），把写竞争分散到多个子分片上；代价是查询库存总量时需要对各个分片求和，这是为消除单行瓶颈而接受的权衡。
