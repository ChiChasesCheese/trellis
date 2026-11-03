---
id: hi-sd-key-technologies-8-cache-cdn
node: sd.in-a-hurry.key-technologies.exam
type: qa
step: 8
---
## Q
**分布式缓存与 CDN**｜系统设计 · 速览

面试里缓存和 CDN 各用在什么地方？缓存要说清哪几件事，CDN 只能缓存静态资源吗？

## A
**缓存的用途。** 存放计算或读取代价高的数据：预先聚合好的指标（异步后台任务算好）、用户会话以减少数据库查询、昂贵查询的结果（如关注者的帖子列表，直接在 Postgres 上联表可能极慢）。

**必须说清的四件事。**
- 淘汰策略：LRU（最近最少使用）、FIFO、LFU（最不常用）
- 失效策略：数据库更新后让缓存失效，如活动场地变了
- 写策略：write-through（同时写缓存和库，一致但写慢）、write-around（直接写库，避免污染缓存）、write-back（先写缓存再异步落库，快但缓存挂了会丢数据）
- 存什么、用什么数据结构：别只说「存缓存」，例如热门活动列表可用 Redis 有序集合（sorted set）

**选型。** Redis（多种数据结构）或 Memcached（只支持简单键值）。

**CDN。** 靠近用户的分布式缓存：命中就直接返回，未命中回源取并缓存。不只用于图片、视频、JS，也可缓存变化不频繁的动态内容，甚至 API 响应；同样有 TTL 和失效机制。常见的有 Cloudflare、Akamai、CloudFront。
