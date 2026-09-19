---
id: kafka-producer-linger-ms-latency-throughput
node: producer.batching-throughput
type: qa
step: 3
source: kafka-2e
---
## Q
默认情况下（linger.ms=0），生产者只要有可用的发送线程，即使批次里只有一条消息也会立刻发送出去。把 `linger.ms` 调大会带来什么效果？

## A
`linger.ms` 指定生产者在发送一个消息批次之前，愿意再多等待多长时间以便让更多消息加入这个批次。把它设置成大于 0 的值，会让批次里能装进更多消息，从而降低单位消息的网络和处理开销（如果启用了压缩，压缩效果也更好），显著提升吞吐量；代价是每条消息都要多等这么一段时间才被发出去，牺牲了一点延迟。
