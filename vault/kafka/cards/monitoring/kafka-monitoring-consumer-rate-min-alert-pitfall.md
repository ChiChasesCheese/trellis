---
id: kafka-monitoring-consumer-rate-min-alert-pitfall
node: monitoring.client-metrics
type: qa
source: kafka-2e
---
## Q
有人给消费者的 bytes-consumed-rate 或 records-consumed-rate 设置了「低于某个最小值就告警」的规则，想以此检测消费者工作负载不足的问题，为什么这样做容易产生误报？

## A
消费者读取消息的速率在很大程度上取决于生产者当前有没有在正常写入数据——如果某段时间恰好生产者流量低甚至没有新消息可读，消费者的消费速率自然也会跟着降低到接近零，这并不代表消费者本身出了问题。给消费速率设置最小值告警，实际上隐含了「生产者流量应该一直保持在某个水平」这个假设，一旦这个假设不成立（比如业务本身就有低峰期），这类告警就会频繁误报，让人难以区分究竟是消费者故障还是单纯没有数据可消费。
