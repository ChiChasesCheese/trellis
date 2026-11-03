---
id: hi-pt-distributed-rate-limiter-6-fail-open-closed
node: qb.sd.distributed-rate-limiter.points
type: qa
step: 6
---
## Q
**分布式限流器 · 限流器挂了怎么办**｜必会 · 出自：分布式限流器 › 深入 3

分布式限流器依赖的 Redis 不可用时，请求该放行还是拒绝？各自的风险是什么，实际怎么折中？

## A
**拒绝（fail-closed）。** 保护后端，但等于关掉整个 API，还引发客户端重试风暴；适合支付等场景。
**放行（fail-open）。** API 可用，但丢失保护，故障常与高峰同时发生，可能引发级联故障。
**折中。** 放行但退化为每网关本地的粗粒度限流（限额按网关数均分），并告警。关键是明确说出选择和理由。
