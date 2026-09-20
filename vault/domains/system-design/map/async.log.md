%% trellis:begin %%
# The Log & Kafka
*Async & Streaming*

The append-only log as system of record; partitions, consumer groups, offsets, retention.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/storage.internals|Storage Engine Internals]]

**Unlocks:** [[domains/system-design/map/analytics.derived|Derived Data & Materialized Views]], [[domains/system-design/map/problems.foundations.message-queue|Distributed Message Queue]]

## Readings
- [[kafka-docs|Apache Kafka Documentation (Design section)]]
- [[the-log-jay-kreps|The Log: What every software engineer should know (Jay Kreps)]]
- [[turning-the-database-inside-out|Turning the Database Inside-Out (Kleppmann)]]

## Cases
- [[qs-write-model-is-a-log-read-model-is-a-projection|Write model as immutable log, read model as projection]] — `quant-stroller`

## Drills
- [[design-payment-ledger|Drill: Design a payment ledger service]]
- [[design-message-queue|Drill: Design a distributed message queue like Apache Kafka]]

## Cards (8)
1. [[async-log-vs-queue]]
2. [[async-log-throughput-design]]
3. [[async-log-ordering-partitions]]
4. [[async-consumer-groups-offsets]]
5. [[async-consumer-lag-monitoring]]
6. [[async-rebalancing-protocols]]
7. [[async-log-compaction]]
8. [[async-log-backfill-reprocessing]]
%% trellis:end %%

## Notes
