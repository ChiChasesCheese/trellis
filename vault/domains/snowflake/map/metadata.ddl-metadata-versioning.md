%% trellis:begin %%
# DDL 即元数据版本化
*元数据与云服务*

为何 ALTER/CREATE/DROP 都是仅涉及元数据的操作，它们创建一个新的表版本，而不是就地修改数据。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]]

**Unlocks:** [[domains/snowflake/map/txn.ddl-as-transaction|DDL 即事务]]

## Cards (5)
1. [[ddl-add-column-instant]]
2. [[ddl-drop-column-new-version]]
3. [[ddl-running-query-keeps-its-version]]
4. [[ddl-swap-with-atomic-cutover]]
5. [[ddl-type-widening-vs-rebuild]]
%% trellis:end %%

## Notes
