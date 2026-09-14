---
id: cache-failure-negative
node: caching.failure
type: qa
---
## Q
Why cache a `404` for a missing object, and why should its TTL usually differ from a successful response?

## A
Negative caching prevents repeated misses—whether legitimate, buggy, or abusive—from hammering origin/storage. But absence may be repaired or content may appear soon, so use a shorter bounded TTL and distinguish stable `404` from transient `5xx`/timeout. Never cache an authorization-dependent denial under a shared key that omits identity.

## Q zh
为什么要缓存 missing object 的 `404`？它的 TTL 为什么通常应不同于成功响应？

## A zh
negative caching 防止合法、buggy 或 abusive 的重复 miss 持续轰击 origin/storage。但缺失可能被修复，新内容也可能很快出现，因此应使用更短的 bounded TTL，并区分稳定 `404` 与 transient `5xx`/timeout。绝不能把 authorization-dependent denial 缓存在遗漏 identity 的 shared key 下。
