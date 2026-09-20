---
nodes: [problems.commerce.flash-sale, traffic.rate-limiting, distributed.transactions.concurrency-control]
tags: [problem]
---
# Drill: Design a flash sale like a 10-second, 1,000-unit product drop

Design the admission and inventory paths for a flash sale: 1,000 units of one SKU,
1,000,000 buyers converging within a 10-second window, and a 6% payment failure/no-show
rate on successful reservations.

**Constraints to state and honor**
- 1,000,000 buyers, 1,000 units, 10-second window — a naive unthrottled peak of
  100,000 purchase attempts/sec against one inventory key.
- Never oversell (confirmed orders must never exceed 1,000) and never undersell (a
  legitimate buyer must not be wrongly rejected while stock remains).
- A successful reservation has a short payment window; failed or expired reservations
  must be reclaimed and re-offered without manual intervention.
- The design must identify which layer runs out of safety margin first and why, using
  a real published throughput number, not a guess.

**Grading points**
- Computes the safety margin of a single Redis instance against the naive unthrottled
  peak using a real published benchmark figure, and explains why that margin alone is
  not enough without admission control ([[problems-flash-sale-hot-key-safety-margin]]).
- Designs a layered admission-control front door (CDN/static offload, rate limiting,
  and a lottery/collection-window scheme when the supply:demand ratio is extreme) rather
  than relying on inventory-layer correctness alone to survive the peak ([[problems-flash-sale-lottery-vs-first-come-first-served]]).
- Implements the atomic decrement as a single check-and-decrement operation (e.g. a Lua
  script) rather than a bare decrement with an after-the-fact check, and can explain the
  race the naive version allows ([[problems-flash-sale-lua-atomic-check-and-decrement]]).
- Justifies the division of labor between a fast in-memory gate and a durable relational
  record, rather than putting the atomic decrement directly on the database ([[problems-flash-sale-redis-vs-db-division-of-labor]]).
- Sets a reservation TTL and expiry-sweep frequency that reclaims failed holds quickly
  enough to avoid undersell, and can justify why it differs from a longer seat-hold TTL
  ([[problems-flash-sale-reservation-ttl-vs-ticket-booking]]).
- States, in order, which component runs out of safety margin first under the computed
  peak load, and why the hot key itself is not the first thing to fail if admission
  control works ([[problems-flash-sale-bottleneck-order]]).
- Names at least one concrete oversell-causing mistake and one concrete undersell-causing
  mistake, and explains why they have different root causes ([[problems-flash-sale-undersell-vs-oversell]]).
- Explains what changes and what stays the same at 10x buyer scale and at 100x scale
  (many SKUs selling simultaneously) ([[problems-flash-sale-10x-100x-evolution]]).

**Solution**: [[solution-flash-sale]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
