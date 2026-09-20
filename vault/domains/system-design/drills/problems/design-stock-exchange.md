---
nodes: [problems.commerce.stock-exchange, distributed.consensus]
tags: [problem]
---
# Drill: Design a stock exchange and the retail brokerage in front of it

Design both halves of the system: the exchange itself (deterministic matching per symbol,
sequencing, replication, market-data fan-out) and a Robinhood-style retail brokerage that
routes orders to it and streams quotes to millions of clients. 8,000 listed symbols, a
300,000 orders/sec market-wide peak, 15 million brokerage daily active users.

**Constraints to state and honor**
- Matching results must be deterministic and replayable — the same input sequence must
  always produce the same trades, even after a failover.
- Per-order matching latency budget is microseconds, not milliseconds.
- The brokerage must never double-execute an order or let two concurrent orders overdraw
  an account's buying power.
- Quote delivery to clients is allowed to be eventually consistent and briefly stale;
  order execution and the ledger are not.

**Grading points**
- Computes the per-symbol order-rate skew from the market-wide peak and compares it
  against a real single-thread matching benchmark to show that compute, not concurrency,
  is not the constraint on a per-symbol engine
  ([[problems-stock-exchange-headroom-vs-lmax-benchmark]]).
- Picks a price-bucket-plus-linked-list order book over a balanced tree and explains why
  O(1) operations matter specifically at a microsecond latency budget
  ([[problems-stock-exchange-order-book-price-bucket-linked-list]]).
- Journals an input event before the matching engine processes it, and explains why that
  ordering (not the reverse) is what makes deterministic replay-based recovery possible
  ([[problems-stock-exchange-journal-before-match-replay-recovery]]).
- Rejects a multi-threaded, lock-protected matching engine even though it sounds faster,
  because it breaks deterministic replay
  ([[problems-stock-exchange-single-thread-vs-multithread-locking]]).
- Computes the naive per-subscriber quote fan-out rate for a hot symbol and designs a
  conflation layer that bounds it independent of the raw tick rate
  ([[problems-stock-exchange-market-data-conflation-375x]]).
- Reserves buying power with a single conditional update rather than a read-then-write,
  and explains exactly which race the conditional update closes
  ([[problems-stock-exchange-buying-power-conditional-update]]).
- States that the exchange must halt new orders for a symbol rather than bypass
  sequencing when the sequencer is down, prioritizing correctness over availability
  ([[problems-stock-exchange-sequencer-down-halt-not-degrade]]).
- Explains why the 10x bottleneck is symbol-to-partition placement, not raw matching
  throughput, given the headroom already established
  ([[problems-stock-exchange-10x-symbol-count-not-throughput]]).

**Solution**: [[solution-stock-exchange]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
