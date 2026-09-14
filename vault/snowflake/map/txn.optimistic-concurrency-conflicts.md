%% trellis:begin %%
# Optimistic Concurrency & Write Conflicts
*Transactions & Concurrency Control*

Two concurrent writers to overlapping data detect conflict at commit time rather than locking rows up front.

**Requires:** [[txn.mvcc-immutable-partitions|MVCC via Immutable Micro-partitions]]
%% trellis:end %%

## Notes
