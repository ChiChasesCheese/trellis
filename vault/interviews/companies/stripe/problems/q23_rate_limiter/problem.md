# q23 · Rate Limiter — sliding window (global → per client → weighted) and token bucket with idle cleanup

**Type:** bespoke (design-flavoured coding) · **Stage:** phone screen / virtual onsite coding · **Last asked:** 2025-12-06 (1point3acres 题库 rate-limiter, onsite); interviewing.io & Reddit Hack2Hire 2025; techprep 2025
**Frequency:** 8 independent mentions (1point3acres 817977 「Stripe NG现场表演」, 1point3acres 1081681, 1point3acres 题库 rate-limiter, interviewing.io "Design a rate limiter in any programming language", Reddit/Hack2Hire rolling window, techprep sliding window / token bucket, darkinterview "Rate Limiter", dev.to programhelp "3 requests per 10 seconds", joeytor/StripeInterview README onsite list) · **Confidence:** medium (rules consistent across sources; exact numbers vary — the 1point3acres "5 requests per 2 seconds per user" version is primary)

## Context
Every Stripe API key is rate limited (the public docs quote 100 req/s live, 25 req/s sandbox,
and `429 rate_limit` errors); Stripe's own engineering blog describes four limiters (request
rate = token bucket, concurrent requests, fleet load shedder, worker utilisation). The interview
version: implement the in-memory core. Requests arrive as `(timestamp_ms, client_id)` in time
order; decide `ALLOW` or `DENY` for each. Part 1 is a single global window, Part 2 keys the
window by client, Part 3 lets requests carry a weight (cost), Part 4 swaps the algorithm for a
token bucket with lazy refill and a memory-cleanup follow-up ("what about clients that go idle
forever?" — the recurring follow-up in the 1point3acres reports).

## Input (stdin)
```
PART n
LIMIT <limit> <window_ms>        (Parts 1–3; default "LIMIT 5 2000" when absent)
BUCKET <capacity> <refill_per_sec> (Part 4; default "BUCKET 5 2")
<ts_ms> [<client>] [<weight>]    one request per line
CLEANUP <now_ms> <idle_ms>       (Part 4 only) evict idle clients
```
* `ts_ms` is a non-negative integer, **non-decreasing per client** (see the out-of-order rule).
* `client` is a token without spaces; Part 1 ignores it (a missing client is `-`).
* `weight` (Part 3+) is a positive integer, default 1. Up to 10^6 request lines.

## Output
One line per request line, in order: `ALLOW` or `DENY`; an out-of-order request prints `ERROR`.
`CLEANUP` prints `EVICTED <n>`.

## Rules
### Part 1 — global sliding window  `SlidingWindow(limit, window_ms).allow(ts_ms, weight=1) -> bool`
A request at time `t` is allowed iff the number of **previously allowed** requests with timestamps
in **`(t − window_ms, t]`** (left-open, right-closed) is `< limit` — i.e. `count + 1 ≤ limit`.
Denied requests are **not** recorded and never consume capacity. `5 per 2000 ms`: requests at
0,1,2,3,4 → all `ALLOW`; at 5 → `DENY`; at 1999 → `DENY` (0 is still inside `(−1, 1999]`);
at 2000 → `ALLOW` (0 has left the window: `(0, 2000]`). Requests with equal timestamps are
processed in input order.

### Part 2 — per client  `RateLimiter(limit, window_ms).allow(client, ts_ms, weight=1) -> bool`
One independent window per `client` key (a `deque` per client, created on first sight). Clients
never affect each other.

### Part 3 — weighted requests
Each request carries a `weight` (cost). Allow iff `sum(weights in window) + weight ≤ limit`.
`weight > limit` is always denied (and still not recorded); `weight ≤ 0` → `ValueError`.
Parts 1–2 are the special case `weight = 1`.

### Out-of-order timestamps (all parts)
Timestamps must be non-decreasing **per client**. A request whose `ts` is smaller than that
client's last **seen** timestamp (allowed or denied) raises `ValueError("out-of-order timestamp")`;
`main()` prints `ERROR` for that line and continues. (Reconstructed — sources only say "assume
requests arrive in order".)

### Part 4 — token bucket + cleanup  `TokenBucket(capacity, refill_per_sec).allow(client, ts_ms, cost=1) -> bool`
Each client owns a bucket that **starts full** (`capacity` tokens) at its first request.
Lazy refill: on every request add `(ts − last_ts) × refill_per_sec / 1000` tokens (exact
integer arithmetic in milli-tokens — no floats), capped at `capacity`; then allow iff
`tokens ≥ cost`, and subtract `cost`. Denied requests leave the bucket unchanged (the refill is
kept). `capacity 5, refill 2/s`: 5 requests at t=0 → `ALLOW`×5; t=0 again → `DENY`;
t=500 → `ALLOW` (1 token refilled); t=600 → `DENY` (0.2 tokens); t=5000 → `ALLOW`.
`cleanup(now_ms, idle_ms) -> int` removes every client whose last seen request is at or
before `now_ms − idle_ms` (idle **for at least** `idle_ms`) and returns how many were removed. An
evicted client that comes back starts with a full bucket — which is exactly what it would have
had anyway once `idle_ms ≥ capacity / refill_per_sec × 1000`. `RateLimiter.cleanup` has the
same signature and evicts clients whose window `(now − window_ms, now]` is empty and whose last
seen request is ≥ `idle_ms` old.

## Worked examples
```
PART 1 / LIMIT 5 2000 : ts 0,1,2,3,4,5,1999,2000,2001,2002
  -> ALLOW ALLOW ALLOW ALLOW ALLOW DENY DENY ALLOW ALLOW ALLOW
     (at 2001 the window (1, 2001] holds 2,3,4,2000 = 4 -> ALLOW; at 2002 holds 3,4,2000,2001 -> ALLOW)
PART 2 / LIMIT 2 1000 : 0 a / 0 b / 1 a / 2 a / 2 b / 1000 a / 1001 a
  -> ALLOW ALLOW ALLOW DENY ALLOW ALLOW ALLOW
     (a: 0,1 allowed; 2 denied (window {0,1}); 1000 -> (0,1000] = {1} -> ALLOW;
      1001 -> (1,1001] = {1000} -> ALLOW.  b: 0 and 2 allowed — clients are independent)
```
PART 3 / LIMIT 5 2000 : 0 a 3 / 1 a 2 / 2 a 1 / 3 a 6 / 2000 a 3 / 2001 a 3
  -> ALLOW (3) ALLOW (5) DENY (6>5) DENY (6>5 always) ALLOW ((0,2000] has 2 -> 5) DENY ((1,2001] has 2+3=5, +3 = 8)
PART 4 / BUCKET 5 2 : 0 a ×6 / 500 a / 600 a / 5000 a / CLEANUP 20000 10000 / 20000 a
  -> ALLOW ALLOW ALLOW ALLOW ALLOW DENY ALLOW DENY ALLOW EVICTED 1 ALLOW
```

## Edge cases hidden tests are known to target
- window boundary: `t − window` is **excluded**, `t` included (2000 allowed, 1999 denied)
- denied requests must not be recorded (a burst of denials must not extend the lockout)
- many requests at the same timestamp (all inside the window)
- a single client hammering vs. many clients each under the limit (fairness follow-up)
- weight exactly filling the window (`sum + w == limit` → ALLOW), one above → DENY
- token bucket: fractional refill (`600 ms × 2/s = 1.2 tokens`) must not be rounded away —
  1.2 tokens accumulate; but 0.2 tokens is not enough for a request
- token bucket cap: a client idle for a day does not accumulate more than `capacity`
- cleanup evicts exactly the clients idle ≥ `idle_ms` (boundary `==` evicts) and returns the count
- 10^6 requests must run in < 2 s — O(1) amortised per request (deque pops), no per-request scans

## Variants seen in the wild
- "3 requests per 10 seconds" (dev.to programhelp) and "100 requests per 15 minutes per user"
  (mock interview) — only the constructor numbers change.
- Fixed-window counter (`(user, window_start) → count`) instead of sliding — accepted as a
  simpler Part 1 by some interviewers; the sliding version is what the 1point3acres reports describe.
- Stripe blog's other limiters (concurrent-requests limiter with sorted set, load shedders) come
  up as discussion, not code.
- Follow-ups reported: fairness between large and small merchants (weighted / per-client limits),
  memory cleanup of idle keys (Part 4 `cleanup`), distributed version with Redis + Lua (discussion).

## What this tests
S03 modelling (state per client) · S05 strict vs non-strict boundaries · S12 time windows · S16 sliding-window / token bucket · S18 validation · S19 incremental design · S21 stdlib fluency (`collections.deque`) · A07 sliding window over sorted timestamps per key

## Sources
- 1point3acres 817977 「Stripe NG现场表演」 (5 requests per 2 s per user, sliding window; follow-ups fairness + memory cleanup); 1point3acres 1081681; 1point3acres 题库 rate-limiter (onsite, last asked 2025-12-06)
- interviewing.io "Design a rate limiter in any programming language"
- Reddit / Hack2Hire (rolling-window rate limiter); techprep (sliding window, token bucket)
- darkinterview "Rate Limiter" ("tracks API access patterns and enforces request limits; multiple clients identified by keys")
- dev.to programhelp ("3 requests per 10 seconds sliding window")
- https://gist.github.com/ptarjan/e38f45f2dfe601419ca3af937fff574d (Stripe engineering: the four rate limiters, token bucket reference)
- joeytor/StripeInterview README (Virtual Onsite / Coding → Rate Limiter)
