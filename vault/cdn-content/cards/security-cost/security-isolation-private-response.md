---
id: security-isolation-private-response
node: security-cost.isolation
type: qa
---
## Q
An authenticated profile response has `s-maxage=300` but no tenant-specific cache key. May a shared CDN cache it?

## A
No. Authentication does not make shared caching safe; the cache must prove every representation-varying authorization input is partitioned, or the response must be `private`/`no-store` or bypass shared cache. Prefer separating public shell from private data. Never rely on an unkeyed cookie or `Authorization` header being forwarded to origin if the cache can serve before authorization runs.

## Q zh
一个 authenticated profile response 设置了 `s-maxage=300`，但没有 tenant-specific cache key。shared CDN 可以缓存它吗？

## A zh
不可以。authentication 本身不能保证 shared caching 安全；cache 必须证明所有会改变 representation 的 authorization input 都进入 partition，否则 response 必须设为 `private`/`no-store` 或 bypass shared cache。优先拆分 public shell 与 private data。绝不能依赖 unkeyed cookie 或 `Authorization` header 被 forward 到 origin，因为 cache 可能在 authorization 执行前就返回内容。
