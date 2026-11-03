---
id: hi-pt-api-circuit-breaker-4-half-open-thundering
node: qb.lld.api-circuit-breaker.points
type: qa
step: 4
---
## Q
**熔断器 · 半开期惊群**｜必会 · 出自：熔断器 › 深入 1

冷却时间一结束，大量等待的线程同时冲向刚恢复的下游，会把它再次打垮。熔断器应该如何避免这种惊群？

## A
**要点。** 半开状态只放行 `half_open_max_calls` 个探测请求（通常 1 个），其余请求继续被拒绝或走降级；探测通过后才全量放行。
**实现。** 取许可时在锁内检查在途探测数，已达上限就拒绝，否则占一个名额。
**取舍。** 名额取 1 最保守，但恢复慢；取多个恢复快，但风险更大。
