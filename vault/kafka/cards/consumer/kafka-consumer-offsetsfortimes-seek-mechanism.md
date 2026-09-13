---
id: kafka-consumer-offsetsfortimes-seek-mechanism
node: consumer.seek-and-replay
type: qa
source: kafka-2e
---
## Q
如果想让消费者从「一小时前」这个时间点开始重新读取消息，而不是跳到某个具体的偏移量数字，应该怎么做？

## A
先用 `consumer.offsetsForTimes(...)` 方法，给它一个「分区 → 目标时间戳」的映射（比如把每个已分配给该消费者的分区都映射到一小时前的时间戳），这个调用会向 broker 发请求，换回每个分区里对应这个时间点附近的偏移量（`OffsetAndTimestamp`）；然后对每个分区调用 `consumer.seek(partition, offset)`，把消费者的读取位置设置成刚查到的偏移量，这样下一次 `poll()` 就会从这个时间点附近继续读取。
