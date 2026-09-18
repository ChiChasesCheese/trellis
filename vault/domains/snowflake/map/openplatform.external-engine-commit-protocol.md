%% trellis:begin %%
# 外部引擎写入与提交协议
*开放格式与工作负载扩展*

先写入数据、再原子更新目录指针、最后提交治理元数据的顺序，使非 Snowflake 引擎也能安全地写入一张 Iceberg 表。

**Requires:** [[domains/snowflake/map/openplatform.polaris-catalog|Polaris（开放目录）]], [[domains/snowflake/map/txn.snapshot-isolation|隔离级别：READ COMMITTED 与一致性读]]

## Readings
- [[snowflak-iceberg-tables|Apache Iceberg 表:开放格式与目录(Catalog)选型]]

## Cards (5)
- [[commit-crash-before-swap]]
- [[commit-optimistic-concurrency]]
- [[commit-readers-snapshot-isolation]]
- [[commit-snowflake-refresh-external]]
- [[commit-write-then-swap-order]]
%% trellis:end %%

## Notes
