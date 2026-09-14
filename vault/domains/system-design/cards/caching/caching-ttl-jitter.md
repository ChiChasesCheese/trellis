---
id: caching-ttl-jitter
node: caching.invalidation
type: cloze
---
When many keys are warmed at the same moment (deploy, cache flush, midnight job), identical TTLs make them all expire together and hammer the backend at once. The fix is {{c1::adding random jitter to each TTL (e.g. `ttl + rand(0, 10%·ttl)`)}} so expiries spread out; for a single hot key, use {{c2::a lock / single-flight recompute (one request rebuilds, others serve stale)}} to stop a stampede.

## zh
当许多键在同一时刻被预热时（部署、缓存刷新、午夜作业），相同的 TTL 使它们全部同时过期并一次性锤击后端。修复是 {{c1::给每个 TTL 加上随机抖动（例如 `ttl + rand(0, 10%·ttl)`）}} 所以过期传播；对于单个热键，使用 {{c2::一把锁 / single-flight 重新计算（一个请求负责重建，其他请求返回旧值）}} 来停止尖峰。
