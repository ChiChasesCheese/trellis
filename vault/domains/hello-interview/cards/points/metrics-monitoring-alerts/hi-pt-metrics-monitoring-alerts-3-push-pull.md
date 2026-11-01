---
id: hi-pt-metrics-monitoring-alerts-3-push-pull
node: qb.sd.metrics-monitoring-alerts.points
type: qa
step: 3
---
## Q
**指标监控与告警平台 · 推与拉**｜出自：指标监控与告警平台 › 深入 1

指标采集用拉模式（Prometheus 式）还是推模式（Agent 上报）？30 万台规模怎么选？

## A
**拉。** 拉不到就是挂了，天然有存活信号，采集频率由服务端控制；缺点是要做服务发现，跨网络分区和防火墙麻烦，短任务可能来不及拉。
**推。** 适合动态扩缩和短任务；缺点是没有数据有歧义，需显式心跳。
**选择。** Agent 推到区域收集器更实用（连接数可控、易批量压缩），收集器侧补存活指标。
