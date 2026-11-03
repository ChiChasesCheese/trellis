---
id: hi-pt-tt-cache-consistency-hot-keys-3-layered-design
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 3
---
## Q
**缓存一致性与热点 Key · 两级缓存与写路径兜底**｜必会 · 出自：缓存一致性与热点 Key › 整体设计

缓存层的读写路径怎么设计？写完数据库后缓存怎么失效？有哪几层兜底？

## A
**读。** 先本地缓存 L1（容量小、TTL 很短），再 Redis L2，都未命中才回源并回填；回源做并发合并。
**写。** 只更新数据库并立刻删除对应 Redis key。
**兜底。** 订阅 binlog（Canal、Debezium）解析被改主键，发消息给失效消费者，删 Redis 并通知各实例清本地缓存，覆盖所有写入路径及删除失败；所有条目带 TTL 加随机抖动，最坏错误持续一个 TTL。
