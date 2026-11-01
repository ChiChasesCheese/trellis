---
id: hi-pt-metrics-monitoring-alerts-4-why-kafka
node: qb.sd.metrics-monitoring-alerts.points
type: qa
step: 4
---
## Q
**指标监控与告警平台 · 为什么中间放 Kafka**｜出自：指标监控与告警平台 › 取舍与追问

指标监控平台里收集器和时序库之间为什么放一层 Kafka？代价是什么？

## A
**好处。** 缓冲尖峰、解耦采集与存储、多消费者（存储、告警、流式降采样）、可重放（存储故障恢复后补写）。
**代价。** 多一层运维与 1 到几秒延迟。
**分区。** 收集器按 hash(序列) 写分区。
