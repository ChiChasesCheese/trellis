---
id: reliability-metrics-histogram-aggregation
node: reliability.metrics
type: qa
---
## Q
You need fleet-wide p99 origin latency across hundreds of edge instances. Should each instance export a client-side p99 summary or histogram buckets?

## A
Export histogram buckets with boundaries chosen around the SLO, then aggregate bucket counts and compute the fleet quantile. Per-instance summary quantiles generally cannot be averaged into a correct global p99. Validate bucket resolution near the objective; buckets that are too wide can make the computed p99 useless even though aggregation is mathematically valid.

## Q zh
你需要计算数百个 edge instance 的 fleet-wide p99 origin latency。每个 instance 应导出 client-side p99 summary，还是 histogram bucket？

## A zh
应导出围绕 SLO 选择边界的 histogram bucket，再聚合 bucket count 并计算 fleet quantile。per-instance summary quantile 通常不能通过平均得到正确的 global p99。还要验证 objective 附近的 bucket resolution；即使聚合数学上有效，过宽的 bucket 也会让 p99 失去决策价值。
