---
id: external-table-metadata-refresh-stale-results
node: ingestion.external-tables-over-lake
type: qa
source: snowflake-docs
---
## Q
新文件已经写进 S3 路径，但外部表查询结果里就是看不到，重复查询还一直返回旧结果。最可能的原因是什么？

## A
外部表只能看到已登记在其元数据中的文件。如果自动刷新被关闭（`AUTO_REFRESH = FALSE`）或事件通知配置不正确，又没有手动执行 `ALTER EXTERNAL TABLE … REFRESH`，新文件就不会被登记；此时文件集合没有变化，结果缓存也不会失效，于是持续返回过期结果。修复方法是配置好云存储的事件通知以自动刷新，或定期手动刷新；刷新会新增文件、更新变化的文件，并移除已不存在的文件。
