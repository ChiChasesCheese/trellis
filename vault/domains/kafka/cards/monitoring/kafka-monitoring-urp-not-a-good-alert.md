---
id: kafka-monitoring-urp-not-a-good-alert
node: monitoring.broker-metrics
type: qa
step: 1
source: kafka-2e
---
## Q
非同步分区（under-replicated partitions，URP，指首领 broker 上有多少分区的部分副本没有跟上首领进度）数量是 Kafka 最常被提及的监控指标，但现在不再建议把它直接用作主要的告警指标，为什么？应该用什么替代？

## A
URP 能反映从 broker 崩溃到资源过度消耗等各种各样的问题，但也正因为原因太多，在很多完全良性的操作场景下（比如正常的集群维护、部署、分区重分配）它也会短暂变成非零值。如果直接拿 URP 非零就告警，会频繁产生误报，久而久之运维人员会开始忽略这类告警，真正严重的问题反而被掩盖；而且要正确解读 URP 具体代表什么问题，还需要相当多的背景知识。因此更好的做法是使用基于 SLO（服务级别目标）的告警去捕捉客户能感知到的问题，而不是直接监控 URP 这种内部实现细节指标。
