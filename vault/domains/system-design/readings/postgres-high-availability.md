---
nodes: [storage.relational.operations]
url: https://www.postgresql.org/docs/current/high-availability.html
tags: [reference]
---
# High Availability, Load Balancing, and Replication (PostgreSQL docs)

The authoritative source for what running the default system of record at
scale actually involves — streaming replication, sync vs async trade-offs,
failover — straight from the database most designs should start with.

**Extract on read:**
- Read replicas via streaming WAL replication; replication lag as the price of async.
- Synchronous replication: durability bought with commit latency, per-transaction tunable.
- What the docs assume around them: connection pooling (PgBouncer) because Postgres connections are processes, and VACUUM as mandatory MVCC maintenance.

%% trellis:begin %%
## Source
[Open the original ↗](https://www.postgresql.org/docs/current/high-availability.html)

## Archived copy
![[postgres-high-availability-clip]]
%% trellis:end %%
