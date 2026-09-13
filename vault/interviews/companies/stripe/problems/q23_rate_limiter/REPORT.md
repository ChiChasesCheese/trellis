# q23 Rate Limiter — report

## Summary
The in-memory core of Stripe's API rate limiting (429 `rate_limit`; the engineering-blog token
bucket). Reported as a phone-screen / onsite coding question ("5 requests per 2 seconds per
user") with two standard follow-ups: fairness between big and small merchants (per-client keys,
weighted requests) and memory cleanup for idle keys. Parts: global sliding window → per client →
weighted → token bucket with lazy refill + `cleanup`.

## Sources & confidence
medium — 1point3acres 817977 / 1081681 / 题库 rate-limiter (onsite, last asked 2025-12-06),
interviewing.io, Reddit Hack2Hire, techprep, darkinterview, dev.to programhelp, joeytor README;
the numbers (5 per 2 s) come from the 1point3acres reports, the token-bucket semantics from
Stripe's own gist (ptarjan).

## Approach by part
1. `SlidingWindow`: deque of `(ts, weight)` for *allowed* requests + running sum; on each request
   pop everything with `ts <= t − window` (window is `(t − W, t]`), allow iff `sum + w <= limit`.
   O(1) amortised — every event is appended once and popped once.
2. `RateLimiter`: `dict[client] → SlidingWindow`, created on first sight. Out-of-order
   timestamps are checked per client (`ValueError`, printed as `ERROR`).
3. Weight is just the deque payload; `weight > limit` is denied and not recorded; `weight <= 0`
   is a `ValueError`.
4. `TokenBucket`: `[milli_tokens, last_ts]` per client; refill = `elapsed_ms × refill_per_sec`
   milli-tokens (exact integers, no float drift), capped at `capacity × 1000`; new clients start
   full; denied requests keep the refill. `cleanup(now, idle)` evicts `last_ts <= now − idle`.

## Pitfalls hidden tests target
- window boundary: `t − W` excluded, `t` included (2000 allowed after 0; 1999 denied)
- recording denied requests (extends the lockout — wrong)
- `sum + weight == limit` must be allowed (non-strict)
- fractional refill lost to integer division (`600 ms × 2/s = 1.2` tokens) — milli-tokens fix it
- bucket must cap at capacity after a long idle gap
- cleanup boundary (`idle == idle_ms` evicts) and returning the count

## Reconstructed rules / conflicts
- Out-of-order handling (`ValueError` → `ERROR` line) and `cleanup` semantics for the sliding
  window (empty window *and* idle) are reconstructions — sources only mention the follow-up.
- Fixed-window counters are accepted by some interviewers; the sliding version is primary
  because the 1point3acres reports say 滑动窗口 explicitly.

## Complexity & measured cost
O(1) amortised per request, O(active clients + events in windows) memory.
Measured: 0.61 s, 139 MB for 10^6 weighted requests over 2 000 clients (budget 2 s / 256 MB;
memory is dominated by holding the 10^6 input lines and output strings).

## Test inventory
18 tests — part1: 5 · part2: 4 · part3: 4 · part4: 5; edge 12 · io 1 · perf 1.

## Skills exercised
S03 state per client · S05 boundary semantics · S12 time windows · S16 sliding window / token bucket · S18 validation · S19 incremental design · S21 `deque` · A07
