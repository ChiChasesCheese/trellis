---
id: kafka-core-batch-latency-throughput-tradeoff
node: core.topics-partitions
type: qa
source: kafka-2e
---
## Q
Kafka 把同一主题、同一分区的多条消息打包成一个批次（batch）再发送，而不是逐条发送。这样做要在什么和什么之间做权衡？

## A
要在延迟和吞吐量之间权衡：批次越大，单位时间内能处理的消息数量（吞吐量）越高，因为减少了每条消息单独走一次网络的开销；但单条消息要等凑够一批才被发出，导致这条消息自身的传输延迟变长。此外批次通常会被压缩以提升传输和存储效率，但压缩本身又需要额外的计算开销。
