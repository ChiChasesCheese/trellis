---
nodes: [problems.commerce.auction, distributed.transactions.concurrency-control]
tags: [problem]
---
# Drill: Design an online auction platform (eBay-style)

Design the bidding core of an eBay-style auction platform: concurrent bids on the same
item must resolve to exactly one strict winner, watchers need near-real-time price
updates, proxy (automatic) bidding must be supported, and sniping at the close must be
handled. Assume 5 million simultaneously active auctions, with the hottest 0.1% (5,000
auctions) drawing disproportionate bid and watcher traffic near their close.

**Constraints to state and honor**
- The current highest bid must be strongly consistent — no two clients may ever observe
  two different "current highest bids" for the same auction at the same time.
- Bid confirmation latency target is P99 < 500ms.
- Watcher price updates may be eventually consistent, target P99 < 2s.
- An auction's close (declaring a winner) must happen exactly once, even with multiple
  scheduler instances running for availability.

**Grading points**
- Computes the expected rate of write collisions on a hot auction's last-second highest-
  bid row and uses that number to justify a per-auction serialized writer over plain
  optimistic retries ([[problems-auction-collision-rate-drives-serialized-actor]]).
- Explains why an auction's contention (many bidders on one row) is structurally
  different from a ticket-booking system's contention (many buyers on many independent
  rows), and why that changes the concurrency-control choice
  ([[problems-auction-contention-differs-from-ticket-booking]]).
- Resolves a concrete proxy-bidding example using a real bid-increment table, showing the
  new leader pays only one increment over the previous leader rather than their own
  ceiling ([[problems-auction-proxy-bid-increment-table-worked-example]]).
- Computes the expected total extension time under a soft-close rule and identifies that
  it needs a hard cap because it is otherwise unbounded
  ([[problems-auction-soft-close-expected-extension-needs-cap]]).
- Decouples watcher fan-out from the bid-write path and justifies it by which path needs
  strong consistency and which needs only eventual consistency
  ([[problems-auction-watcher-fanout-decoupled-eventual-consistency]]).
- Guarantees an auction's close happens exactly once across multiple racing scheduler
  instances using an idempotent conditional write through a single serialized entry
  point ([[problems-auction-close-exactly-once-idempotent-token]]).
- States what changes at 10x scale: fan-out sharding granularity, not per-auction actor
  throughput ([[problems-auction-10x-fanout-sharding-not-actor-throughput]]).
- Recovers a crashed per-auction actor's state from a single row read in the store rather
  than a journal replay, and explains why that's sufficient here
  ([[problems-auction-actor-crash-rebuild-from-store-not-replay]]).

**Solution**: [[solution-auction]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
