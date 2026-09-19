---
id: kafka-monitoring-records-lag-max-not-recommended
node: monitoring.client-metrics
type: qa
step: 3
source: kafka-2e
---
## Q
消费者的获取请求管理器（fetch request manager）提供了一个 records-lag-max 指标，能直接反映消费滞后（消费者偏移量和 broker 日志结束偏移量之间的差值）。为什么不建议把它当作监控消费滞后的首选指标？

## A
这个指标有两个局限：一是它只能反映**单个分区**的最大滞后，如果消费者读取多个分区，看不到每个分区各自的滞后情况，也拿不到跨消费者群组的全局视图；二是它依赖消费者客户端自身的内部实现细节，不同客户端或版本的行为可能不一致，不够可靠和通用。因此更好的做法是使用专门的外部消费滞后监控工具，从 broker 侧独立计算每个分区、每个消费者群组的滞后情况，而不是依赖消费者客户端自己上报的这个指标；只有在没有其他选择时，才退而求其次监控它并设置告警。
