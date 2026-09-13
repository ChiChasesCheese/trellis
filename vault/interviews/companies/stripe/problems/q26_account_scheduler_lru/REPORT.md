# q26 AccountScheduler — report

## Summary
Onsite "general coding" classic: a pool of sandbox accounts with timed locks, `is_available(id, t)`,
`acquire(id, duration, t)` and an `acquire_any` that hands out the least-recently-used free account.
Stripe uses it to check class design, edge-case enumeration (exclusive lock end, unknown ids,
duplicate adds, idempotent release) and whether the candidate can upgrade an O(n) scan to a heap
with lazy invalidation when asked about 10^5 operations.

## Sources & confidence
medium — 1point3acres 题库 "AccountScheduler LRU" (onsite, last asked 2026-03-27), linkjob
2025-12-07 / 2026 onsite report (`is_available → acquire(duration) → LRU auto-select`),
process_and_jd.md onsite table. Return values, `duration > 0`, `never-used first, then oldest
last_used, ties by id`, and the command stream are reconstructed (marked in problem.md).

## Approach by part
1. `Account(locked_until|None, last_used|None, ver)` in a dict; available iff `locked_until <= t`
   (exclusive end); `acquire` requires availability and `duration > 0`, sets `last_used = t`.
2. Two heaps: `free` keyed `(never_used_flag, last_used, id, ver)` and `locked` keyed
   `(locked_until, id, ver)`. `acquire_any(t)` first migrates expired locks (`locked_until <= t`)
   into `free`, then pops the LRU entry, skipping stale versions; entries that are still locked
   for this `t` (non-monotonic time) are parked back into `locked`. `locked_until` is *kept* when
   an account returns to the free heap, so an earlier-`t` query still sees the old lock.
3. `release` sets `locked_until = None`, bumps the version and re-pushes with the unchanged
   `last_used`; releasing a free or unknown account is a no-op (`OK` / `UNKNOWN`).
4. `run_commands(lines, max_part)` drives one scheduler; arity/int validation → `ERROR`;
   `part1..part4` gate the verbs so earlier-part suites reject later verbs.

## Pitfalls hidden tests target
`t0 + d` free vs `t0 + d − 1` locked; re-lock exactly at expiry; unknown ids; `ADD` twice;
never-used before used and `'a10' < 'a2'` string order; failed acquires / queries / release
must not bump `last_used`; `NONE` when all locked, then the one that expires; `duration <= 0`;
a lock taken at a later `t` still blocks an earlier `t` (bug caught by the test-suite during
development: clearing `locked_until` when migrating expired locks).

## Complexity & measured cost
`add`/`acquire`/`release` O(log n); `acquire_any` amortised O(log n) (each heap entry is popped
at most once per version). 100k commands over 20k accounts: 0.165 s, 38.6 MB.
An O(n) scan per `acquire_any` would be ~1.4·10^9 steps on this input.
Measured: 0.165s, 38.6 MB

## Test inventory
17 tests — part1: 4 · part2: 7 · part3: 3 · part4: 3; edge 9 · fmt 1 · io 1 · perf 1.
`IMPL=starter`: 17 failed / 0 passed.

## Skills exercised
S03 class + dict modeling · S05 strict/non-strict time comparison · S08 deterministic tie-breaks ·
S10 state over an event stream · S11 idempotent add/release · S18 validation/error paths ·
S19 incremental design · S20 self-testing
