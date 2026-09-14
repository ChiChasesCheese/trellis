---
id: streaming-offset-token-exactly-once
node: ingestion.snowpipe-streaming-offset-tokens
type: qa
source: snowflake-docs
---
## Q
一个把 Kafka 数据写入 Snowflake 的 Snowpipe Streaming 客户端进程崩溃重启后，如何做到既不丢数据也不重复写？

## A
依靠偏移量令牌（offset token）。客户端在写入行时附带来源位置（如 Kafka offset），Snowflake 为每个通道（channel）记录最后一次已提交的偏移量令牌。重启后，应用先查询该通道最后提交的偏移量，再从这个位置之后开始重放源数据：已提交的数据不会被再次写入，未提交的数据会被重新发送，从而实现恰好一次（exactly-once）交付。
