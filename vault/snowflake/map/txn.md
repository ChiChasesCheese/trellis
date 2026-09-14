%% trellis:begin %%
# 事务与并发控制

平台围绕并发读写者所做出的承诺，这一切完全建立在不可变文件之上。

## Topics
- [[txn.acid-guarantees|ACID 保证]]
- [[txn.snapshot-isolation|隔离级别：READ COMMITTED 与一致性读]]
- [[txn.mvcc-immutable-partitions|基于不可变微分区的 MVCC]]
- [[txn.optimistic-concurrency-conflicts|写并发：表级锁与写冲突]]
- [[txn.ddl-as-transaction|DDL 即事务]]
- [[txn.multi-statement-transactions|多语句事务]]
%% trellis:end %%

## Notes
