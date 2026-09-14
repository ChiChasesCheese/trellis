---
id: commit-snowflake-refresh-external
node: openplatform.external-engine-commit-protocol
type: qa
source: snowflake-docs
---
## Q
一张使用外部 catalog 的 Iceberg 表，由外部引擎持续写入。Snowflake 为什么可能看不到最新提交？需要注意哪些同步和数据质量问题？

## A
对外部管理的表，Snowflake 需要刷新（refresh）元数据才能获知 catalog 中新的元数据指针；可开启自动刷新（automated refresh）按 `REFRESH_INTERVAL_SECONDS` 轮询，但频繁更新的表用过短的轮询间隔会降低性能；自动刷新随 DML 同步模式变更，仅由 DDL 造成的模式变更需要手动刷新。Time Travel 到建表后的快照要求在快照过期前定期刷新。外部引擎写入时还要保证元数据统计（如 `RowCount`、`NullCount`）与实际数据一致，且同一快照的清单中不能有重复文件，否则 Snowflake 会报错或读到不一致的元数据。
