---
id: cache-validator-304
node: caching.validators
type: qa
---
## Q
What is the correct flow when a stale cache entry has an ETag and receives a new request?

## A
Send a conditional request with `If-None-Match`. If the selected representation is unchanged, the origin returns `304`; the cache updates relevant metadata and serves the stored body. If changed, the origin returns `200` with the new representation. Coalesce concurrent revalidations so one stale hot object does not fan out to origin.

## Q zh
stale cache entry 有 ETag，又收到新请求时，正确流程是什么？

## A zh
发送带 `If-None-Match` 的 conditional request。若选定 representation 未变化，origin 返回 `304`；cache 更新相关 metadata，并发送已存 body。若已变化，origin 返回带新 representation 的 `200`。并发 revalidation 应 request coalescing，避免一个 stale hot object fan out 到 origin。
