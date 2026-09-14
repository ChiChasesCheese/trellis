---
id: kafka-monitoring-burrow-vs-xinfra-scope
node: monitoring.lag-e2e
type: qa
source: kafka-2e
---
## Q
同样是 LinkedIn 开源的外部监控工具，Burrow 和 Xinfra Monitor（原 Kafka Monitor）各自负责回答什么不同的问题？

## A
Burrow 关注的是「消费端」问题：它对比 broker 上分区的最新偏移量和各个消费者群组已提交的偏移量，判断某个消费者群组是不是正常、是不是滞后或已经停止工作，回答的是「这个消费者群组是不是把消息消费到位了」。Xinfra Monitor 关注的是「集群本身能不能正常读写」这个更基础的问题：它主动向一个跨越所有 broker 的专用主题持续写入并读取合成消息，衡量每个 broker 生产/读取请求的可用性和读写延迟，回答的是「现在还能不能正常往 Kafka 写数据、从 Kafka 读数据」，这个问题不依赖任何具体的消费者群组是否存在。
