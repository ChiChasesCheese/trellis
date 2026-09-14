---
nodes: [storage.internals, storage.encoding, distributed.replication, distributed.transactions, analytics.olap, analytics.batch, async.streaming]
url: https://dataintensive.net/
tags: [book, canonical]
---
# Designing Data-Intensive Applications, 2nd ed. (Kleppmann & Riccomini, 2026)

The systematic backbone for the Storage / Distributed Data / Async / Analytics
region of this map — the cards are recall hooks for what these chapters explain
properly. The 2nd edition adds cloud-native architecture, CRDTs/local-first,
and AI-era data systems.

**Chapter map against this skeleton:**

| DDIA 2e | Node |
|---|---|
| Ch 1–2 Trade-offs, Nonfunctional Requirements | `foundations.tradeoffs`, `foundations.method` |
| Ch 3 Data Models & Query Languages | `storage.nosql`, `storage.relational` |
| Ch 4 Storage & Retrieval | `storage.internals`, `analytics.olap` |
| Ch 5 Encoding & Evolution | `storage.encoding`, `architecture.discovery` |
| Ch 6 Replication (incl. CRDTs/local-first) | `distributed.replication`, `distributed.crdt` |
| Ch 7 Sharding | `distributed.partitioning` |
| Ch 8 Transactions | `distributed.transactions` |
| Ch 9–10 Failures, Consistency & Consensus | `distributed.time`, `distributed.consistency`, `distributed.consensus` |
| Ch 11 Batch Processing | `analytics.batch` |
| Ch 12 Stream Processing | `async.streaming`, `async.log` |
| Ch 13–14 Derived State | `analytics.derived`, `analytics.warehouse` |

%% trellis:begin %%
## Source
[Open the original ↗](https://dataintensive.net/)

## Archived copy
![[ddia-2e-clip]]
%% trellis:end %%
