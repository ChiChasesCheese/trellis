---
id: hi-pt-metrics-monitoring-alerts-5-tsdb-choice
node: qb.sd.metrics-monitoring-alerts.points
type: qa
step: 5
---
## Q
**指标监控与告警平台 · 存储选型**｜出自：指标监控与告警平台 › 深入 2

指标监控每秒百万点追加写且数据无限增长，存储为什么选专用时序库，而不是关系库或通用宽表库？

## A
**反面。** 关系库每点一行，索引膨胀、写放大严重；通用宽表库（如 Cassandra）写扩展好，但缺少时序压缩和聚合。
**专用时序库。** 数据只追加且基本按时间有序，适合 LSM 式顺序写；同序列相邻点差异小，delta-of-delta 加 XOR 压到约 1.4 字节/点。
**分片。** 按序列哈希，同序列落一处；标签到序列 ID 的倒排索引要分片并放内存。
