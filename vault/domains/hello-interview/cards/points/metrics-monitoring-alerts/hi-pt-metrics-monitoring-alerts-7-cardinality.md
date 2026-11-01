---
id: hi-pt-metrics-monitoring-alerts-7-cardinality
node: qb.sd.metrics-monitoring-alerts.points
type: qa
step: 7
---
## Q
**指标监控与告警平台 · 基数爆炸**｜出自：指标监控与告警平台 › 深入 2

有人把 user_id 或 request_id 当指标标签，会发生什么？平台如何防护？

## A
**后果。** 序列数爆炸，压垮索引和内存，是监控系统最常见的事故源。
**防护。** 接入时对每个指标、每个租户限制序列数上限，超限拒绝并告警。
**设计关联。** 序列是名称加标签集合的唯一组合，标签选择直接决定规模。
