%% trellis:begin %%
# 隔离级别：READ COMMITTED 与一致性读
*事务与并发控制*

普通表只支持 READ COMMITTED——每条语句看到语句开始时已提交的数据；读不阻塞写，基于不可变微分区的多版本读取；Stream 在事务内提供可重复读（repeatable read）。

**Requires:** [[domains/snowflake/map/txn.acid-guarantees|ACID 保证]]

**Unlocks:** [[domains/snowflake/map/txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]], [[domains/snowflake/map/txn.multi-statement-transactions|多语句事务]], [[domains/snowflake/map/openplatform.external-engine-commit-protocol|外部引擎写入与提交协议]]

## Readings
- [[snowflak-transactions-isolation|事务、隐式提交与 READ COMMITTED 隔离级别]]

## Cards (5)
- [[isolation-read-committed-only]]
- [[isolation-read-consistency-mode-global]]
- [[isolation-readers-never-deadlock]]
- [[isolation-sees-own-uncommitted-writes]]
- [[isolation-statement-level-not-txn-level]]
%% trellis:end %%

## Notes
