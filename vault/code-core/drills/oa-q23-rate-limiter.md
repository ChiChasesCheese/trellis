---
nodes: [chrono.windows, toolbox.deque, transfer.stripe-oa]
tags: [stripe-oa, q23]
---
# Drill: rate-limit a request stream, then swap the algorithm for a token bucket

Sixty minutes, four parts, stdin to stdout. Requests arrive as `(timestamp_ms, client_id,
weight)` in time order; decide `ALLOW` or `DENY` for each. Part 1 is a single global
sliding window. Part 2 gives every client its own independent window. Part 3 lets a request
carry a weight (cost) instead of always costing 1. Part 4 replaces the whole algorithm with
a token bucket that refills lazily over time and adds a cleanup command for clients that
have gone idle.

**Constraints to state and honor**
- The window is left-open, right-closed: `(t - window_ms, t]`; a request at exactly the
  window's far edge is allowed, one millisecond earlier is not.
- A denied request is never recorded and never consumes capacity — otherwise a run of
  denials would extend its own lockout indefinitely.
- Timestamps must be non-decreasing per client; an out-of-order one prints `ERROR` and the
  stream continues.
- Up to 10^6 request lines; every operation must be O(1) amortized, not a per-request scan.

**Grading points**
- A deque of `(timestamp, weight)` per client, popped from the left whenever an entry falls
  out of the window — every entry is pushed once and popped once across the whole run, which
  is the amortized argument, not an incidental optimization.
- The boundary check is non-strict at the sum (`current + weight <= limit` allows, one more
  denies) and a request whose own weight exceeds the limit is always denied, never
  partially admitted.
- Token bucket refill computed in integer milli-tokens from elapsed time times the refill
  rate, not floating-point tokens — a naive float or integer-truncated refill silently loses
  fractional tokens across many small gaps.
- A bucket starts full on a client's first request and is capped at capacity on refill, so
  a client idle for a long time doesn't accumulate unbounded credit.
- `cleanup(now, idle_ms)` evicts a client whose last request is at or before `now - idle_ms`
  and returns the count evicted — the boundary is inclusive, and a returning client after
  eviction starts fresh (equivalent to a full bucket once idle time exceeds the refill time).
- Global vs per-client state is the same window logic parameterized by a key, not two
  different implementations.

**Source**
- The full statement, solution notes and report: `vault/stripe/q23_rate_limiter/question.md`,
  `vault/stripe/q23_rate_limiter/solution.md`,
  `vault/Quick_Check/problems/q23_rate_limiter/problem.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
