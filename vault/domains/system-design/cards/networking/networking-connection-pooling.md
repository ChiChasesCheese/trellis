---
id: networking-connection-pooling
node: networking.protocols
type: qa
---
## Q
A service calls a downstream over HTTP/1.1 through a 50-connection pool. Load rises; downstream "latency" explodes while both ends sit at low CPU. Mechanism — and what changes under HTTP/2?

## A
**Pool exhaustion.** HTTP/1.1 allows one in-flight request per connection, so the 51st concurrent request queues waiting for a free connection — that queue wait is invisibly folded into measured downstream latency while both services idle. Required pool size ≈ concurrency = QPS × response time ([[foundations-littles-law]]), so a downstream slowdown alone can exhaust the pool.

HTTP/2 multiplexes ~100 streams per connection, so a couple of connections replace the pool — but limits move to stream caps, and one connection's packet loss now stalls all its streams.

## Q zh
一个服务通过 HTTP/1.1 在一个 50 连接池上调用下游服务。负载上升；下游"延迟"爆炸增长，但两端都处于低 CPU。机制是什么 — HTTP/2 下会发生什么变化？

## A zh
**连接池耗尽。** HTTP/1.1 每个连接只允许一个在途请求，所以第 51 个并发请求等待空闲连接 — 这个队列等待被隐形地折叠到测量的下游延迟中，而两个服务都处于空闲。所需连接池大小 ≈ 并发度 = QPS × 响应时间（[[foundations-littles-law]]），所以下游减速单独就能耗尽连接池。

HTTP/2 每个连接多路复用约 100 个流，所以几个连接就能替代连接池 — 但限制转移到流上限，现在一个连接的丢包会停滞其所有流。
