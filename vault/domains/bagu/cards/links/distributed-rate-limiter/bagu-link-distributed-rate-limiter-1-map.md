---
id: bagu-link-distributed-rate-limiter-1-map
node: links.distributed-rate-limiter
type: qa
step: 1
---
## Q
**分布式限流器（Rate Limiter） · 会被追问哪些八股**｜必会

设计分布式限流器（Rate Limiter）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 限流是对海量计数器做低延迟的原子读改写。基础是：令牌桶等算法、单机线程安全、Redis 加 Lua 的原子计数、主从切换丢计数可容忍、限流的位置。

**下钻路线。**
- 算法怎么选 → 大多数网关默认令牌桶，允许突发，平均速率可控，[[a.protect.rate-limit-algorithms|限流算法]]
- 单机限流器怎么写、怎么线程安全 → 引出多实例共享计数的问题，[[b.protect.limiter-handwrite|手写限流器]]
- 先查再放导致超额 → 单机内也要原子，用 CAS 或原子累加，[[a.runtime.java-chm|ConcurrentHashMap 如何线程安全]]
- 多个实例共享计数 → Redis 加 Lua 原子计数，[[b.protect.distributed-limit|分布式限流怎么实现]]
- Redis 挂了放行还是拒绝 → 普通接口 fail-open 退本地限流，资金类 fail-closed，[[b.protect.distributed-limit|分布式限流怎么实现]]
- 计数放单个 Redis，主库挂了 → 哨兵切换会丢最近一小段，限流可容忍偏松，[[b.redis.sentinel-failover|哨兵选主、故障转移与脑裂]]
- 限流放网关还是服务内 → 网关入口粗限流，服务内按下游精细限流；网关多实例要共享计数，[[b.distributed.rpc-gateway-lb|RPC、API 网关与负载均衡]]
- 单个客户端压垮一个分片 → 本地聚合配额，热点分流，[[a.cache.hot-key|热 key 的发现与处理]]

**业务场景。** 支付下单接口的限流器故障时选 fail-closed 拒绝，避免放进超量请求；浏览类接口则放行退本地限流。
**系统设计。** [[links.tt-flash-sale-ticketing|秒杀抢票（排队、限流、防超卖）]]：入口限流的阈值要与库存挂钩；[[links.url-shortener-design|短链接服务（URL Shortener / TinyURL）]]：创建接口限流同源，差别是不限库存。
