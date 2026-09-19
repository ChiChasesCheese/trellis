---
id: kafka-consumer-fetch-max-bytes-vs-partition-fetch-bytes
node: consumer.poll-config
type: qa
step: 3
source: kafka-2e
---
## Q
要限制消费者一次 `poll()` 拉取数据占用的内存，为什么建议优先用 `fetch.max.bytes`（限制单次响应的总字节数）而不是 `max.partition.fetch.bytes`（限制每个分区返回的字节数）？

## A
用 `max.partition.fetch.bytes` 控制内存会很麻烦，因为消费者没法预知 broker 这次响应里会包含多少个分区的数据——分区数一多，即使每个分区都不超限，总数据量依然可能很大，内存占用变得不可控。而 `fetch.max.bytes` 直接限制整个响应的总字节数，能更直接地限制消费者用于缓存数据的内存上限，只有在需要保证「从每个分区读到差不多数据量」这种特殊需求时，才值得专门用 `max.partition.fetch.bytes`。
