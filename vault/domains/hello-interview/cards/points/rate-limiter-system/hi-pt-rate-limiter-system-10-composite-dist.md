---
id: hi-pt-rate-limiter-system-10-composite-dist
node: qb.lld.rate-limiter-system.points
type: qa
step: 10
---
## Q
**限流器（单机类设计） · 多规则组合与分布式扩展**｜追问 · 出自：限流器（单机类设计） › 取舍与追问

追问：每秒 10 次且每分钟 100 次怎么实现？要扩展到多实例呢？

## A
**组合。** `CompositeLimiter` 持有多个 Limiter，全部通过才放行；其中一个拒绝时，之前已通过的不应被扣减（先检查后统一扣，或提供回滚）。
**分布式。** 状态放共享存储（Redis 加 Lua 保证原子），`Limiter` 接口基本不变，只换成远端实现。
**权重。** `try_acquire(now, cost=1)`，令牌桶直接扣 `cost`。
