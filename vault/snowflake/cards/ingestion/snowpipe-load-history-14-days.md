---
id: snowpipe-load-history-14-days
node: ingestion.snowpipe-auto-ingest
type: qa
source: snowflake-docs
---
## Q
Snowpipe 的加载历史保存在哪里、保存多久、怎么查看？这与批量 COPY 相比有何不同？

## A
Snowpipe 的加载历史存在管道（pipe）的元数据中，保存 14 天，需要通过 REST 端点、SQL 表函数或 ACCOUNT_USAGE 视图主动查询。批量 COPY 的加载历史存在目标表的元数据中，保存 64 天，并在 COPY 语句完成时直接作为语句输出返回。
