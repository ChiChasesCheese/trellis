---
id: cache-failure-bypass
node: caching.failure
type: qa
---
## Q
The external cache fleet is down. Why can "bypass cache and send everything to origin" turn a partial failure into a total outage?

## A
The origin was sized for misses, not total traffic; automatic fail-open can multiply its load and cause cascading failure. Bound bypass QPS/concurrency, retain a small local/stale fallback, shed low-priority work, and recover gradually to avoid a refill storm. Test the cache-disabled mode under production-shaped load before calling it a fallback.

## Q zh
external cache fleet 宕机。为什么“绕过 cache，把所有请求发给 origin”会把 partial failure 变成 total outage？

## A zh
origin 通常按 miss 流量而不是总流量扩容；自动 fail-open 会成倍放大 origin load，引发 cascading failure。应限制 bypass QPS/concurrency，保留小型 local/stale fallback，shed 低优先级工作，并逐步恢复以避免 refill storm。必须先用 production-shaped load 测试 cache-disabled mode，才能称它为 fallback。
