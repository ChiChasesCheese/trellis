---
id: stream-retention-auto-extension-14-days
node: pipelines.stream-staleness-and-retention-extension
type: qa
source: snowflake-docs
---
## Q
一张表的保留期只有 1 天，上面的流已经 5 天没有被消费，却仍然没有陈旧。Snowflake 做了什么？这有什么代价？

## A
当表的保留期小于 14 天且流未被消费时，Snowflake 会临时把表的保留期延长到流的偏移量处，默认最多 14 天，与账户版本无关；上限由 `MAX_DATA_EXTENSION_TIME_IN_DAYS` 参数决定。流被消费后，延长的保留期恢复为表的默认值。代价是延长保留期需要额外存储，会反映在月度存储费用中。
