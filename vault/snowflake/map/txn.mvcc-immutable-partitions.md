%% trellis:begin %%
# MVCC via Immutable Micro-partitions
*Transactions & Concurrency Control*

A write never mutates a micro-partition in place; it produces a new table version referencing new and unchanged partitions.

**Requires:** [[storage.micro-partition-format|Micro-partition Format]], [[txn.snapshot-isolation|Snapshot Isolation]]

**Unlocks:** [[txn.optimistic-concurrency-conflicts|Optimistic Concurrency & Write Conflicts]], [[continuity.retention-vs-failsafe|Time Travel vs Fail-safe]], [[pipelines.stream-offset-bookmark|Streams as Offset Bookmarks]]
%% trellis:end %%

## Notes
