%% trellis:begin %%
# Snowpipe Streaming 与偏移量令牌（offset token）
*数据加载与摄取*

基于通道（channel）的行级摄取，由客户端提供偏移量令牌（offset token），在无需暂存文件的情况下提供恰好一次（exactly-once）语义。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/ingestion.snowpipe-auto-ingest|Snowpipe 自动摄取]]

**Unlocks:** [[domains/snowflake/map/ingestion.datastream-kafka-compatible|Datastream（兼容 Kafka 协议的摄取）]]

## Readings
- [[snowflak-snowpipe-streaming|Snowpipe Streaming:行级流式写入与精确一次投递]]

## Cards (5)
1. [[streaming-channel-ordering]]
2. [[streaming-offset-token-exactly-once]]
3. [[streaming-pipe-object-server-side]]
4. [[streaming-throughput-latency-numbers]]
5. [[streaming-vs-snowpipe-choice]]
%% trellis:end %%

## Notes
