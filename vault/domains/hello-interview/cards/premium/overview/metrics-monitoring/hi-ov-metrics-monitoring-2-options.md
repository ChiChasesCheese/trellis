---
id: hi-ov-metrics-monitoring-2-options
node: sd.problem-breakdowns.metrics-monitoring
type: qa
step: 2
tags: [通览]
---
## Q
**指标监控平台 · 高层设计**｜通览

指标监控平台的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 本机采集器、摄入服务、Kafka、时序库、查询服务、告警评估服务、通知服务、Postgres。

**每条路径。**
- **摄入指标：** 采集器本地聚合、缓冲、批量发送，经摄入服务进 Kafka，再写入时序库。
- **查询看板：** 仪表盘请求到独立的查询服务，查询时序库，返回时间戳与值数组。
- **定义告警：** 规则经 `POST /alerts/rules` 存进 Postgres；评估服务定期取出，查询时序库，越线时发出告警事件。
- **发通知：** 通知服务接收告警事件，去重、分组、静默、升级，再发邮件、Slack、PagerDuty。

**存储。** 指标点进时序库（只追加、按时间分块、列式压缩）；告警规则放 Postgres，因为规则很少变。
