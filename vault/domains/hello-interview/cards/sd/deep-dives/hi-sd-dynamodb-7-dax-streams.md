---
id: hi-sd-dynamodb-7-dax-streams
node: sd.deep-dives.dynamodb
type: qa
step: 7
---
## Q
**DynamoDB：DAX 与 Streams**｜系统设计 · 深入技术

DynamoDB 自带的缓存 DAX 和变更流 Streams 分别解决什么问题？有哪些注意事项？

## A
**DAX（DynamoDB Accelerator）。** 专为 DynamoDB 做的内存缓存，读多的负载可达微秒级，因此未必要额外引入 Redis 或 Memcached。使用时要把客户端换成 DAX 客户端 SDK，API 兼容但不是完全透明。它既是读穿（read-through）又是写穿（write-through）缓存，有条目缓存和查询缓存两个缓存，始终开启。

**DAX 的坑。**
- 只对经过 DAX 的写自动失效；绕过 DAX 直接写 DynamoDB，缓存会一直过期到 TTL 或被淘汰
- 强一致读不缓存，直接透传给 DynamoDB

**Streams（DynamoDB Streams）。** 内置的变更数据捕获（CDC）：条目的插入、更新、删除都以流记录形式出现，供下游处理。

**用途。**
- 触发 Lambda，发通知或更新缓存
- 保持 Elasticsearch 索引与表同步，实现搜索
- 实时分析：启用 Kinesis Data Streams，再接 Firehose 写入 S3 / Redshift / OpenSearch；Firehose 不能直接读 DynamoDB Streams，需要 Kinesis 或 Lambda 做中介
