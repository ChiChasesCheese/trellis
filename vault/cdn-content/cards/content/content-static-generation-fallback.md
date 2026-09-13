---
id: content-static-generation-fallback
node: content.static-generation
type: qa
---
## Q
A catalog has ten million routes, so prebuilding every page makes deploys take hours. What hybrid generation strategy preserves CDN performance?

## A
Prebuild the predictable hot set and route manifest; generate long-tail pages on first request or asynchronously, with request collapsing so one fill runs per key. Serve a bounded fallback or 404 policy while generation proceeds, persist the result in durable shared storage, and cap generation concurrency. Measure cold-generation latency and failure rate separately from cache-hit latency.

## Q zh
catalog 有一千万条 route，预构建全部页面让 deploy 耗时数小时。什么 hybrid generation strategy 能保留 CDN 性能？

## A zh
预构建可预测的 hot set 和 route manifest；long-tail page 在首次请求时或异步生成，并用 request collapsing 保证每个 key 只运行一次 fill。生成期间提供有界 fallback 或 404 policy，把结果持久化到 durable shared storage，并限制 generation concurrency。cold-generation latency / failure rate 必须与 cache-hit latency 分开测量。
