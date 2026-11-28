---
id: hi-pt-metrics-aggregator-8-cardinality
node: qb.sd.metrics-aggregator.points
type: qa
step: 8
---
## Q
**指标聚合系统 · 标签基数爆炸**｜追问 · 出自：指标聚合系统 › 深入 4

有人把 `userId` 当作标签，序列数从 200 万涨到上亿。系统怎么防住？

## A
**要点。** 网关为每个指标设序列数上限（如 1 万），超出的归并到 `other` 标签并报警。

**治理。** 元数据里记录每个指标当前的序列数，作为治理依据，和业务方协商拆掉高基数标签。

**为什么。** 基数同时放大内存、存储和查询成本。
