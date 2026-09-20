%% trellis:begin %%
# Distributed Message Queue
*Design Problems / Building Blocks & Warm-ups*

A Kafka-class log: partitions, replication, consumer groups, retention and delivery semantics.

**Requires:** [[domains/system-design/map/async.log|The Log & Kafka]], [[domains/system-design/map/async.delivery.guarantees|Delivery Guarantees]]

## Readings
- [[solution-message-queue|设计题解：分布式消息队列（Distributed Message Queue，Kafka 一类）]]
- [[src-confluent-rebalancing-message-queue|Incremental Cooperative Rebalancing in Apache Kafka: Why Stop the World When You Can Change It?]]
- [[src-kafka-docs-message-queue|Design | Apache Kafka]]
- [[src-linkedin-message-queue|Reflecting on One Year (and 1 Trillion Messages) with Kafka at LinkedIn]]

## Drills
- [[design-message-queue|Drill: Design a distributed message queue like Apache Kafka]]

## Cards (8)
1. [[problems-message-queue-partition-count-two-lower-bounds]]
2. [[problems-message-queue-pull-based-consumer-model]]
3. [[problems-message-queue-isr-quorum-f-plus-1-tradeoff]]
4. [[problems-message-queue-page-cache-consumer-lag-cliff]]
5. [[problems-message-queue-cooperative-rebalancing-stabilization]]
6. [[problems-message-queue-log-compaction-vs-time-retention]]
7. [[problems-message-queue-hot-partition-key-skew]]
8. [[problems-message-queue-tiered-storage-10x-evolution]]
%% trellis:end %%

## Notes
