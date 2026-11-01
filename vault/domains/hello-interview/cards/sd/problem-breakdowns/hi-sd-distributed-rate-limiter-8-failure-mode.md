---
id: hi-sd-distributed-rate-limiter-8-failure-mode
node: sd.problem-breakdowns.distributed-rate-limiter
type: qa
step: 8
---
## Q
**高可用：失败时放行还是拒绝**｜系统设计 · 问题拆解

Redis 分片不可用时，fail-open 和 fail-closed 各是什么、各自的风险？社交平台选哪个，如何降低故障概率？

## A
**fail-closed（拒绝）。** 连不上 Redis 就返回 503 或 429，没有验证过的请求都不放。风险：等同于下线 API，后端明明健康，用户还会激进重试；适合支付、高安全场景。

**fail-open（放行）。** 当作没有限流，直接转发。风险：失去保护；若 Redis 是因高负载而挂，所有流量涌向后端，可能造成级联崩溃。

**选择。** 两个都是「好」方案，取决于需求。社交平台选 fail-closed：限流故障常与流量高峰同时发生，病毒式事件里放行会压垮数据库，短暂拒绝好过整个平台崩溃。

**预防。** 每个分片配主从复制，主挂了自动提升副本，Redis Cluster 内置故障转移；代价是成本和复制延迟。再配上监控告警：CPU、内存、网络、限流成功率、延迟，以及进入 fail-open 的告警。
