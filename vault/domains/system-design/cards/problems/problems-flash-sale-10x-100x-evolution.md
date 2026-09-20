---
id: problems-flash-sale-10x-100x-evolution
node: problems.commerce.flash-sale
type: qa
step: 8
tags: [grown]
---
## Q
In a flash-sale design where admission control throttles purchase attempts down to a few thousand requests/sec before they reach the inventory key, what happens to the hot key's load at 10x buyer scale (1M to 10M buyers, same 1,000 units), and what actually changes at 100x scale (a platform-wide event with thousands of SKUs selling simultaneously, like Alibaba's Singles Day, which recorded a real peak of about 583,000 transactions/sec)?

## A
At 10x buyer scale, the hot key's load doesn't change at all — admission control's throttled admission rate is set by what the downstream durable store can sustain, not by how many buyers are waiting, so the growth is entirely absorbed by the stateless, horizontally-scalable admission layer. At 100x scale, the bottleneck isn't any single SKU's key getting hotter — Redis Cluster's key hashing naturally spreads thousands of different SKUs' independent counters across different shards — the bottleneck shifts to the shared front-door infrastructure (edge rate limiters, CDN capacity) that must be provisioned for the platform's aggregate traffic and must separately identify and throttle unusually hot individual SKUs so they don't crowd out others.

## Q zh
在一个准入控制已经把购买尝试削减到每秒几千次才打到库存 key 的秒杀设计里，买家规模涨到 10 倍（100 万到 1000 万，库存仍是 1,000 件）时，热 key 的负载会怎样变化？规模涨到 100 倍（平台级同时有成千上万个商品在秒杀，如阿里巴巴双十一，真实峰值曾达到约每秒 58.3 万笔交易）时，真正变化的是什么？

## A zh
10 倍买家规模下，热 key 的负载完全不变——准入控制放行的速率由下游持久化存储能承受多少决定，而不是由等待的买家有多少决定，增长完全被无状态、可水平扩展的准入层吸收。100 倍规模下，瓶颈不是某一个 SKU 的 key 变得更热——Redis 集群的 key 哈希天然会把成千上万个不同商品各自独立的计数器分散到不同分片——瓶颈转移到必须按平台整体流量规划容量、并且要单独识别和限制异常火爆商品的共享前门基础设施（边缘限流器、CDN 容量），防止个别热点商品挤占其他商品的共享资源。
