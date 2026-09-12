---
id: kafka-monitoring-quota-three-types
node: monitoring.client-metrics
type: cloze
source: kafka-2e
---
Kafka 的配额（quota，限制客户端能占用多少 broker 资源）机制支持三种类型：{{c1::生产配额（producer quota），限制客户端每秒能向 broker 发送多少字节}}、{{c2::消费配额（consumer quota），限制客户端每秒能从 broker 读取多少字节}}、{{c3::请求配额（request quota），限制 broker 花在处理这个客户端请求上的时间占比}}。
