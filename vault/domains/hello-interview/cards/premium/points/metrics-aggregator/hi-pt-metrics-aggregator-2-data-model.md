---
id: hi-pt-metrics-aggregator-2-data-model
node: qb.sd.metrics-aggregator.points
type: qa
step: 2
---
## Q
**指标聚合系统 · 数据模型与接口**｜必会 · 出自：指标聚合系统 › 核心实体与接口

只支持计数的指标系统，序列、数据点、上报批次、查询分别怎么定义？

## A
**序列。** `(指标名, 标签集合)` 的哈希，是时序数据的键。
**数据点。** `(seriesId, 时间桶起点, 计数)`。
**批次。** `{instanceId, batchSeq, points}`，`(instanceId, batchSeq)` 用于去重。
**查询。** `GET /query?metric=&tags=&from=&to=&step=&groupBy=`，返回每个分组的 `[{ts, value}]`。
