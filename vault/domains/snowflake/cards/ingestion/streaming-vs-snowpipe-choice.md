---
id: streaming-vs-snowpipe-choice
node: ingestion.snowpipe-streaming-offset-tokens
type: qa
source: snowflake-docs
---
## Q
一个现有管道每几分钟把数据写成文件落到 S3，另一个应用产生逐条的 IoT 事件。分别应该选 Snowpipe 还是 Snowpipe Streaming？

## A
落到 S3 的文件选 Snowpipe：它为基于文件的加载设计，数据已经是文件时再改成按行写入没有意义。逐条事件选 Snowpipe Streaming：它通过 SDK 或 REST API 直接把行写入表，不需要先生成文件、也不需要中间存储，延迟更低、通道内有序，并提供恰好一次（exactly-once）语义。两者是互补关系，Snowpipe Streaming 并不取代 Snowpipe。
