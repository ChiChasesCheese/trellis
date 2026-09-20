---
id: kafka-producer-idempotence-sequence-number-mechanism
node: producer.idempotence-ordering
type: qa
step: 2
source: kafka-2e
---
## Q
开启 `enable.idempotence`（幂等生产者）之后，Kafka 靠什么机制识别并丢弃因重试产生的重复消息？生产者会不会因此报错？

## A
幂等生产者会给发送的每一条消息都打上一个序列号。broker 如果收到了序列号与之前已经成功写入的消息相同的消息，就会判定这是一次重试导致的重复，直接拒绝写入第二份。生产者这边会收到一个 DuplicateSequenceException，但这个异常对生产者来说是无害的——它只是说明这条消息其实已经写入成功过了，不需要额外处理。
