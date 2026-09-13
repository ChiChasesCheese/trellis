---
id: cache-hierarchy-local-remote
node: caching.hierarchy
type: qa
---
## Q
When is an in-process L1 cache valuable in front of a regional Redis-like L2, and what correctness cost does it add?

## A
L1 removes network latency and L2 load for very hot objects, and can preserve limited service during L2 trouble. But every process now owns an independently stale copy; fleet deploys cause cold starts, memory is duplicated, and invalidation fans out. Use short TTLs/versioned keys and measure L1 and L2 hit/miss separately.

## Q zh
regional Redis-like L2 前的 in-process L1 cache 什么时候有价值？它增加了什么 correctness 成本？

## A zh
L1 能为极热 object 消除 network latency 与 L2 load，并在 L2 故障时提供有限服务。但每个进程都有独立 stale copy；fleet deploy 会造成 cold start，memory 重复占用，invalidation 还要 fan out。使用短 TTL/versioned key，并分别测量 L1、L2 hit/miss。
