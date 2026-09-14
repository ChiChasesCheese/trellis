---
id: external-table-refresh-billing
node: ingestion.external-tables-over-lake
type: qa
source: snowflake-docs
---
## Q
开启外部表自动刷新后，账单里出现了 Snowpipe 费用。这是为什么？手动刷新又如何计费？

## A
自动刷新依靠 Snowpipe 处理云存储的事件通知，Snowflake 为管理这些通知收取开销费用，金额随外部表路径中新增文件的数量增长，并以 Snowpipe 费用的形式出现在账单中，可以通过 `PIPE_USAGE_HISTORY` 估算。手动执行 `ALTER EXTERNAL TABLE … REFRESH` 会产生少量维护开销，按云服务（cloud services）计费模型收取；普通外部表的手动刷新只是云服务操作，而引用 Delta Lake 的外部表的手动刷新需要使用用户的虚拟仓库。
