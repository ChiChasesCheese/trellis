---
id: dist-skew-detect-hot-key
node: distributed.skew
type: qa
---
## Q
Fleet average CPU is 35%, but one cache shard is saturated. Which measurements reveal whether a hot key or large object is responsible?

## A
Inspect per-shard QPS, bytes, queueing, evictions, and top-key sketches; compare request count with byte and compute cost per key. A key can be hot by frequency, object size, miss cost, or synchronized expiry. Fleet averages hide skew. Use bounded-cardinality heavy-hitter telemetry or sampled logs—never attach raw cache keys as metric labels.

## Q zh
fleet 平均 CPU 只有 35%，但一个 cache shard 已饱和。哪些 measurement 能判断是 hot key 还是 large object？

## A zh
检查 per-shard QPS、bytes、queueing、eviction 和 top-key sketch；比较每个 key 的 request count、byte cost 与 compute cost。key 可因 frequency、object size、miss cost 或 synchronized expiry 而变 hot。fleet average 会隐藏 skew。使用 bounded-cardinality heavy-hitter telemetry 或 sampled log；绝不能把 raw cache key 当 metric label。
