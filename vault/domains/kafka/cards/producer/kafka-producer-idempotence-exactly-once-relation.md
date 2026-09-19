---
id: kafka-producer-idempotence-exactly-once-relation
node: producer.idempotence-ordering
type: qa
step: 5
source: kafka-2e
---
## Q
「幂等生产者」（idempotent producer）和 Kafka 的「精确一次性」（exactly-once semantics，每条消息只被处理一次的语义）是什么关系？

## A
从 0.11 版本开始，Kafka 支持精确一次性语义，这是一个更大的话题，涉及生产、消费和跨系统处理等更广泛的保证。幂等生产者只是精确一次性语义里一个简单但重要的组成部分：它专门解决「生产者重试导致同一条消息被写入多次」这一类重复问题，但它本身并不等同于完整的精确一次性语义。
