---
nodes: [toolbox.cache, chrono.intervals, transfer.stripe-oa]
tags: [stripe-oa, q26]
---
# Drill: a sandbox-account scheduler with timed locks and LRU auto-select

Sixty minutes, no `PART` header — every command lands on one accumulating
scheduler. `ADD id` registers an account (`EXISTS` if already present).
`AVAILABLE id t` and `ACQUIRE id duration t` check and take a lock covering
`[t, t+duration)` — exclusive end, so the account is available again exactly
at `t + duration`. `ACQUIRE_ANY duration t` locks and returns the
least-recently-used available account: accounts never yet acquired come
first (smallest id among them), then the smallest `last_used`, ties by id.
`RELEASE id` clears a lock immediately without disturbing `last_used`, so an
early release does not reset the account's LRU position. Malformed lines
(unknown verb, wrong arity, a non-integer where a number is expected) print
`ERROR` and change nothing.

**Constraints to state and honor**
- A lock taken at `t0` for `duration` covers the half-open interval
  `[t0, t0+duration)`; `is_available` is `true` at `t0+duration` and `false`
  at `t0+duration-1`.
- Only a successful `ACQUIRE` (direct or via `ACQUIRE_ANY`) updates
  `last_used`; failed acquires, `AVAILABLE` queries, and `RELEASE` never do.
- `acquire` requires `duration > 0`; timestamps are not guaranteed
  non-decreasing, so every query must be answered strictly from the `t` it
  carries, never from "now."
- Up to 10^5 commands over 10^4+ accounts — a linear scan per
  `ACQUIRE_ANY` is roughly 10^9 operations and must be called out as too
  slow.

**Grading points**
- Availability reduces to one comparison against a stored `locked_until`,
  not a boolean flag — say why the half-open interval makes the boundary
  arithmetic exact rather than off-by-one-prone.
- The LRU selection key is a full tuple, `(never_used, last_used, id)`,
  built once and reused for every `ACQUIRE_ANY`, not reconstructed
  ad hoc per call.
- At scale, two heaps — one of available accounts by the LRU key, one of
  locked accounts by expiry — with lazy invalidation on pop, rather than a
  full rescan each time; explain why a stale heap entry is cheaper to skip
  than to keep the heap perfectly in sync.
- `RELEASE` explicitly leaves `last_used` untouched — an early release is
  not equivalent to a fresh acquire for LRU purposes.
- Re-`ADD`ing an existing id, `RELEASE` on an unknown or already-free id, and
  `duration <= 0` are each handled as a named case, not folded silently into
  the happy path.
- String tie-break on id (`a10` before `a2`) when `last_used` ties.

**Source**
- `vault/Quick_Check/problems/q26_account_scheduler_lru/problem.md`, `vault/Quick_Check/problems/q26_account_scheduler_lru/REPORT.md`, `vault/Quick_Check/study/10-solutions/q26_account_scheduler_lru.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
