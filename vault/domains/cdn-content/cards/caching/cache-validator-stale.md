---
id: cache-validator-stale
node: caching.validators
type: qa
---
## Q
How do `stale-while-revalidate` and `stale-if-error` make different availability/freshness trade-offs?

## A
`stale-while-revalidate=N` permits serving stale for N seconds while refreshing asynchronously, reducing user latency and stampedes during normal expiry. `stale-if-error=N` permits stale reuse when validation/origin fails, trading freshness for availability during failure. Both require a bounded stale window, clear telemetry, and data whose risk tolerates staleness.

## Q zh
`stale-while-revalidate` 与 `stale-if-error` 分别做了什么 availability/freshness 权衡？

## A zh
`stale-while-revalidate=N` 允许在 N 秒内先返回 stale、异步 refresh，降低正常 expiry 时的用户 latency 与 stampede。`stale-if-error=N` 在 validation/origin failure 时允许复用 stale，用 freshness 换 availability。两者都需要 bounded stale window、清晰 telemetry，并且数据风险必须能容忍 staleness。
