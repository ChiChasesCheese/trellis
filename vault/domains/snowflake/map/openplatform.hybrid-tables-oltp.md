%% trellis:begin %%
# 混合表（Hybrid Table，Unistore）
*开放格式与工作负载扩展*

一种行存储表类型，具有强制主键与行锁，支持毫秒级点查，并异步镜像到列式存储中以支持分析查询。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]], [[domains/snowflake/map/storage.table-types|表类型]]

**Unlocks:** [[domains/snowflake/map/openplatform.snowflake-postgres|Snowflake Postgres]]

## Readings
- [[snowflak-hybrid-tables|混合表(Hybrid Table):行存与点查/高并发写]]

## Cards (5)
1. [[hybrid-constraints-enforced]]
2. [[hybrid-row-store-async-copy]]
3. [[hybrid-same-engine-atomic-txn]]
4. [[hybrid-storage-and-index-cost]]
5. [[hybrid-vs-standard-table-choice]]
%% trellis:end %%

## Notes
