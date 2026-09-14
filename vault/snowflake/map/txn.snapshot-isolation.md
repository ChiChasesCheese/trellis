%% trellis:begin %%
# Snapshot Isolation
*Transactions & Concurrency Control*

Every statement or transaction sees a consistent point-in-time view of the table without blocking readers or writers.

**Requires:** [[txn.acid-guarantees|ACID Guarantees]]

**Unlocks:** [[txn.mvcc-immutable-partitions|MVCC via Immutable Micro-partitions]], [[txn.multi-statement-transactions|Multi-statement Transactions]], [[openplatform.external-engine-commit-protocol|External Engine Writes & Commit Protocol]]
%% trellis:end %%

## Notes
