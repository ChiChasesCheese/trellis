%% trellis:begin %%
# Brief

**Open with** [[distributed.consistency|Consistency Models]] — holding 28%, and 4 topics stand on it.
→ read [[dynamo-paper|Dynamo: Amazon's Highly Available Key-value Store (2007)]]

## Slipping

| | topic | hold | bears |
|---|---|---|---|
| System Design | [[distributed.consistency|Consistency Models]] | `███░░░░░░░` 28% | 4 |
| System Design | [[correctness.idempotency|Idempotency]] | `███░░░░░░░` 28% | 1 |
| System Design | [[async.log|The Log & Kafka]] | `███░░░░░░░` 28% | 1 |
| Low-Level Design | [[concurrency.primitives|Synchronization Primitives]] | `███░░░░░░░` 30% | 1 |
| Low-Level Design | [[concurrency.patterns|Concurrency Patterns]] | `███░░░░░░░` 27% | 0 |
| Low-Level Design | [[concurrency.model|Threads & Memory Model]] | `███░░░░░░░` 31% | 0 |

## Worth writing

- [[story.star-and-its-limits|STAR and Where It Fails]] — 10 topics stand on it, no cards yet · `trellis --domain narrative scaffold story.star-and-its-limits`
- [[story.decision-spine|The Decision Spine]] — 9 topics stand on it, no cards yet · `trellis --domain narrative scaffold story.decision-spine`
- [[round.what-is-scored|The Signals Behind the Questions]] — 6 topics stand on it, no cards yet · `trellis --domain narrative scaffold round.what-is-scored`
- [[options.pricing|Pricing Models]] — 4 topics stand on it, no cards yet · `trellis --domain markets scaffold options.pricing`
- [[execution.microstructure.book|Limit Order Book & Priority]] — 4 topics stand on it, no cards yet · `trellis --domain quant-infra scaffold execution.microstructure.book`
- [[futures.term-structure|Basis, Carry & Roll]] — 3 topics stand on it, no cards yet · `trellis --domain markets scaffold futures.term-structure`
- [[options.greeks|The Greeks & Hedging]] — 3 topics stand on it, no cards yet · `trellis --domain markets scaffold options.greeks`
- [[data.security-master|Security Master & Corporate Actions]] — 3 topics stand on it, no cards yet · `trellis --domain quant-infra scaffold data.security-master`

## Sealed

*Cards exist but are held back until the ground under them takes.*

- [[concurrency.patterns|Concurrency Patterns]] — waiting on [[concurrency.primitives|Synchronization Primitives]]
- [[distributed.consensus|Consensus]] — waiting on [[distributed.replication|Replication]]
- [[distributed.crdt|CRDTs & Local-First]] — waiting on [[distributed.replication|Replication]]
- [[analytics.derived|Derived Data & Materialized Views]] — waiting on [[async.log|The Log & Kafka]]
- [[correctness.idempotency|Idempotency]] — waiting on [[async.delivery|Delivery Semantics]]
- [[correctness.outbox|Dual Writes & Outbox]] — waiting on [[distributed.transactions|Transactions]], [[async.queues|Message Queues]]
- [[correctness.saga|Sagas]] — waiting on [[distributed.transactions|Transactions]]
- [[correctness.ledger|Ledgers & Reconciliation]] — waiting on [[correctness.idempotency|Idempotency]]

---

- **Basketball** — 97/161 cards seen, hold 90% · pulled today
- **Code Core** — 253/379 cards seen, hold 90% · pulled today
- **Low-Level Design** — 81/125 cards seen, hold 79% · pulled today
- **Markets & Factors** — 0/0 cards seen, hold — · never pulled
- **Narrative Round** — 0/0 cards seen, hold — · never pulled
- **Quant Infrastructure** — 0/0 cards seen, hold — · never pulled
- **System Design** — 307/465 cards seen, hold 69% · pulled today
%% trellis:end %%

## Notes
