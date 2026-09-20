---
id: problems-rate-limiter-single-key-shard-hotspot
node: problems.foundations.rate-limiter
type: qa
step: 7
tags: [grown]
---
## Q
In a rate limiter that shards its Redis counter store by hash(API key), why does adding more Redis shards fail to fix the case where one abnormally active API key (e.g. a client stuck in a retry storm) overloads a single shard, and what does the design do instead?

## A
Hashing by API key routes every request for that one key to exactly one shard no matter how many total shards exist, so a single hot key's operations always land on the same shard while every other shard stays idle relative to it — this is identical in shape to a hot-key problem on a content cache, not something more shards resolves. The fix is not more shards but a local static hard cap for that specific key enforced independently at the gateway, so an abnormal key gets throttled without depending on the real-time responsiveness of the one shard it happens to hash to.

## Q zh
在一个按 hash(API key) 分片 Redis 计数器存储的速率限制器里，为什么增加 Redis 分片数量解决不了'某个异常活跃的 API key（例如客户端卡在重试风暴里）压垮单个分片'这个问题？这个设计用什么代替加分片？

## A zh
按 API key 哈希分片时，无论总共有多少分片，这一个 key 的所有操作永远会被路由到同一个分片，这个热 key 所在的那个分片始终承压，其它分片相对闲置——这和内容缓存上的热 key 问题形状完全一样，不是增加分片数量能解决的。解决办法不是加分片，而是在网关侧对这个特定 key 独立执行一个本地静态硬上限，让异常 key 被限流，且不依赖它恰好哈希到的那一个分片能否实时响应。
