%% trellis:begin %%
# Streams as Offset Bookmarks
*Streams, Tasks & Dynamic Tables*

A Stream is a pointer into a table's version history, not a copy of data; querying it returns the net change since the last consumption.

**Requires:** [[txn.mvcc-immutable-partitions|MVCC via Immutable Micro-partitions]]

**Unlocks:** [[pipelines.stream-types|Stream Types (Standard / Append-only / Insert-only)]], [[pipelines.stream-consumption-and-offset-advance|Offset Advance Only Inside the Consuming DML]], [[pipelines.stream-staleness-and-retention-extension|Stream Staleness & Retention Extension]], [[pipelines.task-scheduling-cron-and-dag|Task Scheduling & DAGs]], [[pipelines.dynamictable-target-lag|Dynamic Tables & TARGET_LAG]]
%% trellis:end %%

## Notes
