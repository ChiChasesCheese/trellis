%% trellis:begin %%
# The Log & Kafka
*Async & Streaming*

The append-only log as system of record; partitions, consumer groups, offsets, retention.

**Requires:** [[storage.internals|Storage Engine Internals]]

**Unlocks:** [[analytics.derived|Derived Data & Materialized Views]]

## Readings
- [[kafka-docs|Apache Kafka Documentation (Design section)]]
- [[the-log-jay-kreps|The Log: What every software engineer should know (Jay Kreps)]]
- [[turning-the-database-inside-out|Turning the Database Inside-Out (Kleppmann)]]

## Cases
- [[qs-write-model-is-a-log-read-model-is-a-projection|Write model as immutable log, read model as projection]] — `quant-stroller`

## Drills
- [[design-payment-ledger|Drill: Design a payment ledger service]]

## Cards (8)
- [[async-consumer-groups-offsets]]
- [[async-consumer-lag-monitoring]]
- [[async-log-backfill-reprocessing]]
- [[async-log-compaction]]
- [[async-log-ordering-partitions]]
- [[async-log-throughput-design]]
- [[async-log-vs-queue]]
- [[async-rebalancing-protocols]]
%% trellis:end %%

## Notes
