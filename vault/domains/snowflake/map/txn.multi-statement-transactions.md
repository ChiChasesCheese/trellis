%% trellis:begin %%
# 多语句事务
*事务与并发控制*

用显式的 BEGIN/COMMIT 将多条语句纳入同一事务范围、默认的自动提交（autocommit）行为，以及隐式事务容易带来麻烦的地方。

**Requires:** [[domains/snowflake/map/txn.snapshot-isolation|隔离级别：READ COMMITTED 与一致性读]]

## Readings
- [[snowflak-transactions-isolation|事务、隐式提交与 READ COMMITTED 隔离级别]]

## Cards (5)
- [[multistmt-autocommit-default-behavior]]
- [[multistmt-autocommit-false-implicit-boundaries]]
- [[multistmt-best-practice-explicit-with-autocommit]]
- [[multistmt-scoped-txn-logging-pattern]]
- [[multistmt-txn-cannot-span-procedure-boundary]]
%% trellis:end %%

## Notes
