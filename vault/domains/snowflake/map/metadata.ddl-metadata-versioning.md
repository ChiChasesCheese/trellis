%% trellis:begin %%
# DDL 即元数据版本化
*元数据与云服务*

为何 ALTER/CREATE/DROP 都是仅涉及元数据的操作，它们创建一个新的表版本，而不是就地修改数据。

**Requires:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]]

**Unlocks:** [[domains/snowflake/map/txn.ddl-as-transaction|DDL 即事务]]

## Cards (5)
- [[ddl-add-column-instant]]
- [[ddl-drop-column-new-version]]
- [[ddl-running-query-keeps-its-version]]
- [[ddl-swap-with-atomic-cutover]]
- [[ddl-type-widening-vs-rebuild]]
%% trellis:end %%

## Notes
