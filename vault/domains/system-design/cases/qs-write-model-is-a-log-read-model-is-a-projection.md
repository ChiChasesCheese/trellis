---
nodes:
- async.log
- analytics.derived
title: Write model as immutable log, read model as projection
codebase: quant-stroller
ref: 4dae805d2955
artefact: decisions:0004-experiment-ledger-event-log-not-rdbms
---

# Write model as immutable log, read model as projection

Ask of every dataset: is this the source of truth, or a projection of it?

A source of truth is well served by an append-only log where each event is one immutable file published by atomic rename. That shape buys concurrency for free — many workers, several machines, no locks, and no half-written file ever visible to a reader — and it makes merging across machines a copy rather than a transaction. Everything else (rankings, running totals, dashboards) is recomputed from the log, so it may be deleted and rebuilt without touching the record.

The standing pressure is to "put it in a database", trading that lock-free write path for one mutable store and its write contention. That is the right trade when queries are the bottleneck. It is the wrong one when a full scan of a few hundred small files is microseconds and no ticket asks for speed.

Note what an engine migration would not fix. The pain usually blamed on file storage is semantic: two aliases for one entity inflating counts, dangling references between stores, older rows missing columns. Those are validation, a canonical registry, and a write-time schema contract — no database merges two names for you.

When reads do get heavy, materialize a projection beside the log, and never let the write path change to serve it.
