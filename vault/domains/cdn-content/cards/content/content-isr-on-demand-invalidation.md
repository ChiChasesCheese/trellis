---
id: content-isr-on-demand-invalidation
node: content.isr
type: qa
---
## Q
A CMS webhook invalidates a product tag, but one region serves old ISR output for ten minutes. What distributed invariant was missing?

## A
Invalidation must have a durable global sequence/version, not a best-effort local delete. Each region records the newest tag generation and refuses artifacts built against an older generation, while asynchronous purge removes old copies. Make webhook delivery idempotent and replayable, and expose propagation lag. Define the staleness SLO explicitly; “on demand” does not mean instant without a consistency contract.

## Q zh
CMS webhook invalidates product tag，但某 region 仍服务十分钟前的 ISR output。缺少什么 distributed invariant？

## A zh
invalidation 必须有 durable global sequence/version，而不是 best-effort local delete。每个 region 记录最新 tag generation，拒绝使用更旧 generation 构建的 artifact，同时异步 purge 旧副本。webhook delivery 要 idempotent、可 replay，并暴露 propagation lag。必须显式定义 staleness SLO；没有 consistency contract，“on demand” 不等于瞬时生效。
