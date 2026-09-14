---
id: kafka-streams-exactly-once-config
node: streams.concepts
type: qa
source: kafka-2e
---
## Q
Kafka Streams 应用要开启「精确一次」处理保证（一条记录不管是否发生故障，都恰好被处理一次，不多不少），需要把 `processing.guarantee` 配置成什么值？它依赖 Kafka 的哪些底层特性来实现？`exactly_once_beta` 这个更高效的实现选项对 broker 版本有什么要求？

## A
把 `processing.guarantee` 设置为 `exactly_once` 就能启用精确一次保证；Streams 借助 Kafka 生产者原生支持的**事务**（transaction）和**幂等性**（idempotence，避免因重试导致同一条消息被重复写入）这两项特性来实现这个保证，而不是自己重新发明一套机制。从 Streams 2.6 版本开始，还提供了一种更高效的精确一次实现，通过把 `processing.guarantee` 设置为 `exactly_once_beta` 来启用，但这个更高效的版本要求集群的 broker 版本至少是 2.5 或更高，如果 broker 版本更老，就只能使用普通的 `exactly_once` 而不是 `exactly_once_beta`。
