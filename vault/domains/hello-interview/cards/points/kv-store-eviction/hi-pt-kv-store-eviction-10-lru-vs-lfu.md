---
id: hi-pt-kv-store-eviction-10-lru-vs-lfu
node: qb.lld.kv-store-eviction.points
type: qa
step: 10
---
## Q
**可配置淘汰策略的内存键值存储 · LRU 与 LFU 的取舍**｜出自：可配置淘汰策略的内存键值存储 › 取舍与追问

追问：LRU 和 LFU 怎么选？精确 LRU 在高并发下有什么问题？

## A
**LRU。** 对最近热友好、实现简单，但会被一次性大扫描冲掉热数据。
**LFU。** 对长期热友好、抗扫描，但新数据频次低容易被立刻淘汰，旧高频数据不衰减；实用版加频次衰减或 TinyLFU 准入过滤。
**近似。** 精确 LRU 的链表是热点；Redis 随机抽样 N 个键淘汰其中最久未用的。
