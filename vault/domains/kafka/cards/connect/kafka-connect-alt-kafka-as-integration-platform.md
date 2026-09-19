---
id: kafka-connect-alt-kafka-as-integration-platform
node: connect.alternatives
type: cloze
step: 1
source: kafka-2e
---
可以把 Kafka 定位成一个同时覆盖三类集成需求的平台：{{c1::数据集成——通过 Connect 在 Kafka 与外部数据存储系统之间搬运数据}}、{{c2::应用集成——通过生产者/消费者客户端让自研应用直接读写 Kafka}}、{{c3::流式处理——对流经 Kafka 的数据做实时计算}}。在这个定位下，Kafka 本身可以被当作传统图形化 ETL 工具的一种可行替代方案，而不只是众多数据源之一。
