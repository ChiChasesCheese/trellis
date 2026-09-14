---
id: cache-model-origin-execution
node: caching.model
type: qa
---
## Q
When does an edge request execute the origin, even though the URL was previously cached?

## A
On a true miss, expired response that requires revalidation, explicit bypass, key/`Vary` mismatch, purge, eviction, or a request directive the cache honors. A stale response may avoid origin execution under `stale-while-revalidate` or `stale-if-error`. Therefore measure cache status by reason, not just a binary hit ratio.

## Q zh
即使 URL 以前缓存过，edge request 在什么情况下仍会执行 origin？

## A zh
true miss、过期且必须 revalidate、显式 bypass、cache key/`Vary` 不匹配、purge、eviction，或 cache 遵循了 request directive 时都会执行 origin。若使用 `stale-while-revalidate` 或 `stale-if-error`，stale response 可能避免同步回源。因此要按原因统计 cache status，而不只是二元 hit ratio。
