---
id: kafka-monitoring-record-error-vs-retry-rate
node: monitoring.client-metrics
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka 生产者提供 record-error-rate 和 record-retry-rate 两个指标，为什么前者比后者更值得设置告警？

## A
record-retry-rate 反映的是消息重试的频率——生产者配置了重试次数和退避策略，遇到可重试的错误（比如短暂的网络抖动）会自动重发，这是一种正常、预期内的行为，本身不代表出了严重问题。而 record-error-rate 表示消息在重试次数用尽后仍然发送失败、最终被生产者**丢弃**的比率，正常情况下这个值应该始终是零，一旦大于零就意味着有数据永久丢失了，是必须立刻关注和告警的信号，比单纯的重试次数增多严重得多。
