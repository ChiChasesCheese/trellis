%% trellis:begin %%
# Snowpipe Streaming 与偏移量令牌（offset token）
*数据加载与摄取*

基于通道（channel）的行级摄取，由客户端提供偏移量令牌（offset token），在无需暂存文件的情况下提供恰好一次（exactly-once）语义。

**Requires:** [[ingestion.snowpipe-auto-ingest|Snowpipe 自动摄取]]

**Unlocks:** [[ingestion.datastream-kafka-compatible|Datastream（兼容 Kafka 协议的摄取）]]

## Readings
- [[snowflak-snowpipe-streaming|Snowpipe Streaming:行级流式写入与精确一次投递]]

## Cards (5)
- [[streaming-channel-ordering]]
- [[streaming-offset-token-exactly-once]]
- [[streaming-pipe-object-server-side]]
- [[streaming-throughput-latency-numbers]]
- [[streaming-vs-snowpipe-choice]]
%% trellis:end %%

## Notes
