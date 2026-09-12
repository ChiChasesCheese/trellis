---
id: kafka-producer-key-null-sticky-partitioning
node: producer.extensibility
type: qa
source: kafka-2e
---
## Q
如果 ProducerRecord 没有指定键（key 为 null），Kafka 默认分区器会怎么选择分区？Kafka 2.4 之后这个策略有什么改进？

## A
键为 null 时，默认分区器采用轮询调度（round-robin）算法把消息尽量均衡地分布到各个分区。从 Kafka 2.4 开始，这个轮询变成了「粘性」的（sticky）：在切换到下一个分区之前，会把同一个批次里的消息都写入当前分区，而不是每条消息都轮换一次分区。这样可以用更少的请求发送相同数量的消息，既降低延迟，又减少 broker 处理请求的 CPU 开销。
