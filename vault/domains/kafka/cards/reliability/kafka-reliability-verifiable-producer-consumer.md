---
id: kafka-reliability-verifiable-producer-consumer
node: reliability.validation
type: qa
source: kafka-2e
---
## Q
Kafka 自带的 `VerifiableProducer` 和 `VerifiableConsumer` 这两个命令行工具是用来做什么的？为什么要用它们而不是直接上线跑真实的业务生产者/消费者来验证可靠性配置？

## A
`VerifiableProducer` 会按你配置的 `acks`、`retries`、`delivery.timeout.ms` 等参数，持续发送一串编号从 1 到指定数字的消息，并把每条消息成功/失败的结果打印出来；`VerifiableConsumer` 负责读取这些消息，按读取顺序打印出来，同时打印偏移量和再均衡相关的信息。用它们而不是真实业务代码的好处是，可以在完全不涉及业务处理逻辑的情况下，单独验证「这套 broker + 客户端配置，在首领选举、控制器选举、滚动重启、不彻底首领选举等场景下到底会表现出什么行为」——比如停掉正在写入的分区首领后，只需核对 `VerifiableProducer` 发出的消息条数和 `VerifiableConsumer` 收到的消息条数是否一致，就能验证「短暂停顿后恢复、不丢消息」这个预期是否成立。
