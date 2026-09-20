---
id: problems-ad-click-aggregation-dual-partition-key
node: problems.search.ad-click-aggregation
type: qa
step: 3
tags: [grown]
---
## Q
In an ad click aggregation pipeline, why can't a single Kafka partitioning scheme serve both the deduplication stage and the aggregation stage, and what does the design do about it?

## A
Deduplication needs every repeated delivery of the *same click* to land on the same shard, so it must partition by the click's own identity (e.g. `insertion_id`). Aggregation needs every click for the *same ad* to land on the same shard so per-ad counts can be summed locally, so it must partition by `ad_id`. A single stream cannot be partitioned by two unrelated keys at once, so the design consumes the deduplication-stage topic (partitioned by `insertion_id`), deduplicates, and then explicitly repartitions (shuffles) the deduplicated events into a second topic keyed by `ad_id` before aggregating — the same co-partitioning requirement that stream-stream and stream-table joins have.

## Q zh
在一个广告点击聚合流水线中，为什么去重阶段和聚合阶段不能共用同一套 Kafka 分区方案？设计上是怎么处理的？

## A zh
去重要求同一次点击的所有重复投递都落在同一个分片上，所以必须按点击自身的身份（比如 `insertion_id`）分区。聚合要求同一个广告的所有点击都落在同一个分片上才能就地求和，所以必须按 `ad_id` 分区。同一份流不可能同时按两个不相关的 key 天然分区，所以设计上先消费按 `insertion_id` 分区的去重阶段 topic，去重之后再显式地重新分区（shuffle）成按 `ad_id` 分区的第二个 topic，然后才做聚合——这和 stream-stream / stream-table join 所要求的 co-partitioning 是同一个道理。
