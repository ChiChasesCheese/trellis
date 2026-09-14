---
id: reliability-testing-cache-state-matrix
node: reliability.testing
type: qa
---
## Q
What integration-test matrix is the minimum for a stale-while-revalidate cache, beyond one HIT and one MISS test?

## A
Cover absent, fresh, stale-within-window, and too-stale entries against origin success, `304`, timeout, and error. Assert response body, status, `Age`/cache headers, whether the caller blocks, origin call count under concurrency, and the stored value after background work. Include cancellation and failed regeneration so a partial response never replaces the last good object.

## Q zh
对于 stale-while-revalidate cache，除了一个 HIT 和一个 MISS test，最小 integration-test matrix 还应包括什么？

## A zh
用 origin success、`304`、timeout 和 error 分别覆盖 absent、fresh、stale-within-window 与 too-stale entry。断言 response body、status、`Age`/cache header、caller 是否 block、并发下的 origin call count，以及 background work 后保存的 value。还要覆盖 cancellation 和 failed regeneration，确保 partial response 永远不会替换 last good object。
