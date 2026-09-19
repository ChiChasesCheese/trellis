---
id: kafka-monitoring-health-check-stale-metrics-tradeoff
node: monitoring.metrics-and-slo
type: qa
step: 3
source: kafka-2e
---
## Q
检测 Kafka broker 是否健康有两种常见方式：一种是用外部进程主动探测 broker（比如尝试连接它对外的端口看是否有响应），另一种是「broker 一段时间没有上报任何指标就告警」（也叫过时指标检测）。为什么说第二种方式虽然可行，但存在一个明显的局限？

## A
「过时指标」检测依赖监控系统本身持续、正常地收到 broker 上报的数据，一旦发现指标停止更新就报警；但这时候很难分清究竟是 broker 本身出了故障，还是采集或传输指标的监控链路（比如采集代理、网络、监控系统本身）出了问题——两种原因看起来是一样的现象。相比之下，直接用外部进程连接 broker 对客户端开放的那个端口、看是否能建立连接和收到响应，是一种更直接、更不依赖监控系统自身可用性的健康检测方式。
