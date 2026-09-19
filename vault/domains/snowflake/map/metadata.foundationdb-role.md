%% trellis:begin %%
# FoundationDB 作为元数据存储
*元数据与云服务*

为何所有表/模式（schema）/事务元数据都存放在一个强一致的分布式键值（KV）存储中，而不是一个定制的目录服务（catalog service）。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/architecture.cloud-services-layer|云服务（Cloud Services，GS）层]]

**Unlocks:** [[domains/snowflake/map/metadata.execution-anchor|执行锚点（Execution Anchor）]], [[domains/snowflake/map/metadata.ddl-metadata-versioning|DDL 即元数据版本化]], [[domains/snowflake/map/metadata.metadata-scaling-consistency|元数据层的伸缩与一致性]], [[domains/snowflake/map/cache.result-cache|持久化结果缓存]], [[domains/snowflake/map/continuity.replication-and-failover|数据库复制与故障切换]], [[domains/snowflake/map/security.rbac-role-hierarchy|RBAC 角色层级]], [[domains/snowflake/map/sharing.secure-data-sharing-mechanics|安全数据共享（Secure Data Sharing）机制]], [[domains/snowflake/map/openplatform.hybrid-tables-oltp|混合表（Hybrid Table，Unistore）]], [[domains/snowflake/map/cost.query-history-and-account-usage|QUERY_HISTORY 与 ACCOUNT_USAGE]]

## Cards (5)
1. [[fdb-commit-point]]
2. [[fdb-enables-stateless-services]]
3. [[fdb-transaction-limits]]
4. [[fdb-what-is-stored]]
5. [[fdb-why-kv-not-custom-catalog]]
%% trellis:end %%

## Notes
