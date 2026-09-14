---
id: datastream-maturity-status
node: ingestion.datastream-kafka-compatible
type: qa
tags: [grown]
---
## Q
在 2026 年规划生产级实时入仓方案时，应该把 Datastream 当作默认选择，还是 Snowpipe Streaming？为什么？

## A
应以 Snowpipe Streaming（按行写表、偏移量令牌保证恰好一次）或 Kafka Connector 为默认方案。Datastream 于 Snowflake Summit 2026 发布，当时处于即将进入私有预览（private preview）的阶段，功能范围、限制和定价都可能变化，适合评估和试点，不宜作为关键生产链路的唯一依赖。
