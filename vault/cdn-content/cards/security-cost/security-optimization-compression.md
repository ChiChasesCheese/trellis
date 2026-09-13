---
id: security-optimization-compression
node: security-cost.optimization
type: qa
---
## Q
Brotli reduces JavaScript bytes by 8% but triples on-demand CPU. When is it still a good CDN optimization?

## A
When compression can be done once at build time or on first request, cached under a representation-safe `Accept-Encoding` key, and reused enough that transfer savings exceed compute and storage cost. Measure end-to-end latency and unit cost by object class. For dynamic low-reuse content, a cheaper encoding level may deliver better total performance and capacity.

## Q zh
Brotli 让 JavaScript byte 减少 8%，但 on-demand CPU 增加三倍。什么时候它仍是好的 CDN optimization？

## A zh
当 compression 可以在 build time 或 first request 只做一次，并用 representation-safe `Accept-Encoding` key 缓存，且 reuse 足够高，使 transfer saving 超过 compute 和 storage cost 时，它是好选择。按 object class 测量 end-to-end latency 与 unit cost。对于 dynamic low-reuse content，更便宜的 encoding level 可能带来更好的整体 performance 和 capacity。
