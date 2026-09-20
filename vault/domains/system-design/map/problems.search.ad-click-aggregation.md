%% trellis:begin %%
# Ad Click Aggregation
*Design Problems / Search, Crawling & Data Pipelines*

Counting billions of clicks exactly enough to bill on: streaming aggregation, late data, reconciliation.

**Requires:** [[domains/system-design/map/async.streaming.processing|Stream Processing]], [[domains/system-design/map/async.delivery.exactly-once|Effectively Exactly-Once]]

## Readings
- [[solution-ad-click-aggregation|设计题解：广告点击聚合（Ad Click Aggregation）]]
- [[src-akidau-dataflow-model-ad-click-aggregation|The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing]]
- [[src-confluent-delivery-semantics-ad-click-aggregation|Message Delivery Guarantees for Apache Kafka — Confluent Documentation]]
- [[src-flink-watermarks-ad-click-aggregation|Generating Watermarks — Apache Flink Documentation]]
- [[src-hellointerview-ad-click-aggregation|Ad Click Aggregator Problem Breakdown]]
- [[src-pinterest-ad-click-aggregation|Building a real-time user action counting system for ads]]

## Drills
- [[design-ad-click-aggregation|Drill: Design a billing-grade ad click aggregation pipeline]]

## Cards (8)
1. [[problems-ad-click-aggregation-dollar-error-budget]]
2. [[problems-ad-click-aggregation-exact-dedup-vs-sketch]]
3. [[problems-ad-click-aggregation-dual-partition-key]]
4. [[problems-ad-click-aggregation-watermark-heuristic-retraction]]
5. [[problems-ad-click-aggregation-late-data-three-tiers]]
6. [[problems-ad-click-aggregation-deterministic-upsert-key]]
7. [[problems-ad-click-aggregation-hot-ad-id-salting]]
8. [[problems-ad-click-aggregation-reconciliation-source-of-truth]]
%% trellis:end %%

## Notes
