---
id: hi-pt-metrics-monitoring-alerts-10-monitor-monitor
node: qb.sd.metrics-monitoring-alerts.points
type: qa
step: 11
---
## Q
**指标监控与告警平台 · 监控的监控**｜加分 · 出自：指标监控与告警平台 › 深入 6

指标监控平台自己的告警链路坏了怎么发现？

## A
**独立。** 告警链路不能依赖被监控的同一套存储；评估器区域内自治，依赖组件独立部署。
**死人开关。** dead man's switch：持续发一个永远为真的告警，下游一旦收不到，就说明整条告警链路坏了。
**多区域。** 各区域自带收集器、存储与评估，全局视图用联邦查询。
