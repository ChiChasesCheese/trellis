---
id: problems-distributed-cache-cold-start-peer-warm
node: problems.foundations.distributed-cache
type: qa
step: 6
tags: [grown]
---
## Q
In a distributed cache design, why is warming a newly-added node or a freshly-built cluster purely from the backing database dangerous, and what alternative do Facebook's regional pools and Netflix's EVCache use instead?

## A
A node or cluster starting at a 0% hit rate turns every request it serves into a database query until it naturally warms up — potentially for minutes to hours — pushing database load toward the level it would see with no cache at all, which is especially dangerous if the cold start is happening during an incident recovery. Instead of warming purely from the database, both Facebook's regional cache pools and Netflix's EVCache warm a cold node or region from an already-warm peer node or peer region first: a miss checks the peer's cache before falling through to the database, so only a true miss on both sides reaches the database.

## Q zh
在分布式缓存设计中，为什么让新加入的节点或全新集群完全靠回源数据库来预热是危险的？Facebook 的区域缓存池和 Netflix 的 EVCache 各自用什么替代方案？

## A zh
一个从 0% 命中率开始的节点或集群，在自然预热完成之前（可能长达几十分钟到几小时）会把它服务的每一个请求都变成一次数据库查询，把数据库负载推向接近完全没有缓存保护时的水平——如果冷启动恰好发生在故障恢复期间，这尤其危险。Facebook 的区域缓存池和 Netflix 的 EVCache 都不是纯粹从数据库预热，而是先让冷节点或冷区域向一个已经暖机的对等节点或对等区域查询：未命中时先查对等方的缓存，只有双方都未命中才真正落到数据库。
