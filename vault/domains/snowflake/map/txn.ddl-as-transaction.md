%% trellis:begin %%
# DDL 即事务
*事务与并发控制*

为何模式（schema）变更从读者的视角看是原子且瞬时的——它构建在与 DML 相同的元数据版本化机制之上。

**Requires:** [[domains/snowflake/map/metadata.ddl-metadata-versioning|DDL 即元数据版本化]]

## Readings
- [[snowflak-transactions-isolation|事务、隐式提交与 READ COMMITTED 隔离级别]]

## Cards (5)
1. [[ddl-change-tracking-brief-lock]]
2. [[ddl-concurrent-with-insert-inconsistency]]
3. [[ddl-ctas-counts-as-ddl]]
4. [[ddl-inside-nested-procedure-error]]
5. [[ddl-own-transaction-implicit-commit]]
%% trellis:end %%

## Notes
