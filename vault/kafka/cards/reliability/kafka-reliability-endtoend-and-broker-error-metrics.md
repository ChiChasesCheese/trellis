---
id: kafka-reliability-endtoend-and-broker-error-metrics
node: reliability.validation
type: qa
source: kafka-2e
---
## Q
除了单独看生产者和消费者各自的指标，还需要监控什么，才能确认「数据从生成到被消费，整个链路是端到端可靠、及时的」？broker 侧又提供了哪两个可以用来发现异常的指标？

## A
需要监控**端到端的数据流**：让生产者记录自己每秒生成的消息数量，消费者记录自己每秒读取的消息数量以及「消息生成时间戳（Kafka 从 0.10.0 起会给每条消息打时间戳）与被读取时间」之间的差值，再用一个系统把两边的数据汇总比对，确认没有消息在中途丢失、且生产到消费的时间差落在业务可接受的范围内——这类端到端监控系统实现起来颇具难度，目前没有现成的开源实现，只有 Confluent Control Center 提供了商业化方案。broker 侧则建议采集 `kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec` 和 `...,name=FailedFetchRequestsPerSec` 这两个指标——它们统计 broker 返回给客户端的失败响应速率；偶尔出现（比如首领切换时的 `NOT_LEADER_FOR_PARTITION`）属正常现象，但如果失败请求数量激增，就需要进一步诊断根因。
