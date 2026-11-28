---
id: hi-c-sd-dynamodb-n17-streams
node: sd.deep-dives.dynamodb.notes
type: qa
step: 13
---
## Q
**DynamoDB · Streams：变更数据捕获**｜摘要 · 必会

DynamoDB 怎么把表的变化推给下游？常见用途有哪些？

## A
- **机制：** DynamoDB Streams 记录表中每次插入、更新、删除，成为流记录，供下游实时消费，是内置的变更数据捕获（CDC）。
- **触发函数：** 变更触发 Lambda，用于通知、更新缓存等动作。
- **同步搜索索引：** 把变更同步到 Elasticsearch，补上 DynamoDB 不擅长的搜索。
- **实时分析：** 开启 Kinesis Data Streams，再经 Firehose 写入 S3、Redshift 或 OpenSearch；Firehose 不能直接读 DynamoDB Streams，要靠 Kinesis Data Streams 或 Lambda 中转。
- **保持一致：** 它是异步的，下游总是比表稍晚，设计上要接受这个延迟。
