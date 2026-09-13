---
id: kafka-producer-batching-config-interaction
node: producer.batching-throughput
type: qa
source: kafka-2e
---
## Q
`batch.size`、`linger.ms`、`buffer.memory`、`compression.type` 这四个参数是如何共同影响生产者吞吐量的？

## A
`batch.size` 和 `linger.ms` 共同决定一个批次何时被发送——批次达到 `batch.size` 字节数或等待时间达到 `linger.ms`，哪个先满足就触发发送；批次越大、等待时间越长，单条消息的网络开销越低，吞吐量越高，但延迟也随之增加。`buffer.memory` 决定生产者在消息发出之前能缓存多少数据，缓冲区不足会阻塞 `send()` 甚至抛出异常。`compression.type` 则在批次发送前压缩数据，批次越大压缩效果通常越好，能进一步减少网络传输和存储开销。四者共同作用，本质都是在延迟与吞吐量/资源占用之间做权衡。
