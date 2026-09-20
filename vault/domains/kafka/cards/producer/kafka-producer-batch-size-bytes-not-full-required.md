---
id: kafka-producer-batch-size-bytes-not-full-required
node: producer.batching-throughput
type: qa
step: 2
source: kafka-2e
---
## Q
`batch.size` 参数是按消息条数计算的吗？把它设置得很大，是不是意味着生产者会等到批次被填满才发送，从而增加延迟？

## A
不是。`batch.size` 是按字节数（而不是消息条数）限制一个批次能使用的内存大小。批次填满时会被整体发送，但生产者并不要求批次必须填满才发送——未填满、甚至只有一条消息的批次也可能被发出去。因此把 `batch.size` 设置得很大本身不会增加延迟，只是会多占用一些内存；但如果设置得太小，生产者需要更频繁地发送小批次，反而增加额外开销。
