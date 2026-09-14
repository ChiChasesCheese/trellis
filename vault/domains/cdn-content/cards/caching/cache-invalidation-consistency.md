---
id: cache-invalidation-consistency
node: caching.invalidation
type: qa
---
## Q
What consistency promise should a global CDN make for purge instead of saying "instant invalidation"?

## A
Define a measurable bound and failure behavior: e.g., 99.9% of POPs stop serving the old version within 5 seconds, all acknowledged targets within 60 seconds, with status/retry for stragglers. State whether in-flight responses and disconnected POPs are included. Clients needing read-your-write may use versioned URLs or bypass until the purge watermark is observed.

## Q zh
global CDN 对 purge 应给出什么 consistency promise，而不是笼统说“instant invalidation”？

## A zh
定义可测的 bound 与 failure behavior：例如 99.9% POP 在 5 秒内停止返回旧 version，所有已确认 target 在 60 秒内完成，并对 straggler 提供 status/retry。还要说明是否包含 in-flight response 与 disconnected POP。需要 read-your-write 的 client 可使用 versioned URL，或在观察到 purge watermark 前 bypass。
