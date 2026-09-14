---
id: dist-routing-affinity-tradeoff
node: distributed.routing
type: qa
---
## Q
Cache affinity improves hit ratio, but one shard is overloaded. When should routing violate affinity?

## A
Affinity is an optimization, not an availability invariant. Prefer the owner while it is healthy and below a capacity threshold; overflow to a bounded alternate set when queue, latency, or utilization crosses guardrails. The alternate may miss and increase origin load, so collapse fills and enforce a global origin budget. Record affinity breaks so chronic skew triggers rebalancing rather than permanent random spillover.

## Q zh
cache affinity 改善 hit ratio，但一个 shard 已 overload。routing 什么时候应违反 affinity？

## A zh
affinity 是优化，不是 availability invariant。owner 健康且低于 capacity threshold 时优先使用；queue、latency 或 utilization 超过 guardrail 时，overflow 到有界 alternate set。alternate 可能 miss 并增加 origin load，因此要 collapse fill 并执行 global origin budget。记录 affinity break，使 chronic skew 触发 rebalancing，而不是永久 random spillover。
