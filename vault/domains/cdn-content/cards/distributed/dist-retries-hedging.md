---
id: dist-retries-hedging
node: distributed.retries
type: qa
---
## Q
When is request hedging safer than immediately retrying a slow object read?

## A
For idempotent reads with independent replicas, send a duplicate only after a latency threshold such as p95, take the first success, and cancel the loser. This targets tail outliers while duplicating only a small fraction of traffic. Bound hedges globally, never hedge a hedge, and disable them under overload or correlated dependency failure. Without cancellation and capacity guardrails, hedging is simply an early retry storm.

## Q zh
什么情况下 request hedging 比立即 retry slow object read 更安全？

## A zh
对有独立 replica 的 idempotent read，仅在超过 p95 等 latency threshold 后发送 duplicate，取第一个成功结果并 cancel loser。这样针对 tail outlier，同时只复制少量流量。全局限制 hedge、绝不 hedge 一个 hedge，并在 overload 或 correlated dependency failure 时禁用。没有 cancellation 和 capacity guardrail，hedging 只是更早的 retry storm。
