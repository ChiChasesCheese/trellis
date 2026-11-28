---
id: hi-c-sd-kafka-n03-messages-partitioning
node: sd.deep-dives.kafka.notes
type: qa
step: 3
---
## Q
**Kafka · 消息的结构，以及它怎么选分区**｜摘要 · 必会

一条 Kafka 消息有哪些字段？没有键时怎么分区？消息怎么找到对应的 broker？

## A
- **四个字段（都可选）：** 值（payload）、键、时间戳、头（headers，类似 HTTP 头的元数据键值对）。键用来决定去哪个分区；时间戳记录创建或写入时间，但分区内的顺序由偏移量决定，不是时间戳。
- **分区选择：** 对键做哈希分到特定分区，同键必到同一分区，保证分区级顺序。没有键时，现代客户端用"粘性"分区器：先把一批消息批量送进同一个分区以提高效率，再轮换。设计大型系统时通常要用键，让相关消息进入同一分区、按序处理。
- **找 broker：** 分区确定后，集群元数据（由 Kafka 控制器维护）说明分区在哪个 broker 上，生产者据此直接把消息发给持有该分区的 broker。
- **命令行例子：** `kafka-console-producer --topic my_topic --property parse.key=true --property key.separator=:`，输入 `key1: Hello`。
