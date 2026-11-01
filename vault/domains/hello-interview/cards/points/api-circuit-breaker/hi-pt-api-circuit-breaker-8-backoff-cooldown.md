---
id: hi-pt-api-circuit-breaker-8-backoff-cooldown
node: qb.lld.api-circuit-breaker.points
type: qa
step: 8
---
## Q
**熔断器 · 半开策略与指数退避**｜出自：熔断器 › 深入 3

半开期有两个参数：`half_open_max_calls` 和 `success_threshold`，另外冷却时间可以固定也可以退避。它们各自控制什么？下游长时间故障时冷却时间怎么调？

## A
**参数。** `half_open_max_calls` 控制同时探测数；`success_threshold` 控制连续成功几次才信任下游。
**冷却时间。** 固定值最简单；可用指数退避——每次半开探测失败后把冷却时间翻倍（设上限），下游长时间故障时减少无谓的探测。
