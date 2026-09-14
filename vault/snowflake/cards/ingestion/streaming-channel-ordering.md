---
id: streaming-channel-ordering
node: ingestion.snowpipe-streaming-offset-tokens
type: qa
source: snowflake-docs
---
## Q
Snowpipe Streaming 中的通道（channel）是什么？为什么通常让一个通道对应一个 Kafka 分区？

## A
通道是向表写入行的一条有序逻辑流：同一通道内的行按顺序摄取，而且每个通道单独跟踪自己的偏移量令牌（offset token）。Kafka 分区内部本身是有序的，一个分区对应一个通道，就能保持分区内顺序，并且每个分区可以独立地确定性重放、零丢失恢复。相比之下，基于文件的 Snowpipe 不保证加载顺序。
