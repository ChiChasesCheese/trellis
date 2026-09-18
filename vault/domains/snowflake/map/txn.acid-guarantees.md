%% trellis:begin %%
# ACID 保证
*事务与并发控制*

在一个不可变、带版本的存储层上，原子性、一致性、隔离性与持久性具体意味着什么。

**Requires:** [[domains/snowflake/map/architecture.three-layer-model|三层架构]]

**Unlocks:** [[domains/snowflake/map/txn.snapshot-isolation|隔离级别：READ COMMITTED 与一致性读]]

## Readings
- [[snowflak-transactions-isolation|事务、隐式提交与 READ COMMITTED 隔离级别]]

## Cards (5)
- [[txn-detached-transaction-auto-abort]]
- [[txn-failed-statement-does-not-abort-txn]]
- [[txn-granularity-tradeoff]]
- [[txn-never-nested]]
- [[txn-shared-connection-threads-share-txn]]
%% trellis:end %%

## Notes
