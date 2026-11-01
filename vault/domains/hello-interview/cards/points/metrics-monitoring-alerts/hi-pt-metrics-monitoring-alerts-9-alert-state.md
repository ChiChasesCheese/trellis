---
id: hi-pt-metrics-monitoring-alerts-9-alert-state
node: qb.sd.metrics-monitoring-alerts.points
type: qa
step: 9
---
## Q
**指标监控与告警平台 · 告警状态机与去重**｜出自：指标监控与告警平台 › 深入 3

指标监控的告警如何避免抖动和告警风暴？

## A
**状态机。** inactive → pending → firing → resolved；条件持续满足 for 时长（如 5 分钟）才触发；可设迟滞（触发线与恢复线不同）。
**告警管理器。** 按标签去重，按服务或集群分组，故障波及上千台主机只发一条聚合通知；支持静默、抑制与值班升级；通知至少一次送达。
**缺失。** 没有数据（absent）要与值正常区分，规则里显式写缺失行为。
