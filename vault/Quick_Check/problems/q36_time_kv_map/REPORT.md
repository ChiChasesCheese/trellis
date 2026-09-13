# q36 Time-based KV map — report

## Summary
Versioned key-value store: every write is stamped with a time, reads are "as of t". It is the
LeetCode 981 pattern (Stripe tag) with two Stripe-flavoured extensions — version history and TTL —
plus the same repo's `first_missing_positive` warm-up as a bonus part. Tests the bisect
boundary (`<=`), overwrite-at-equal-time and exclusive expiry.

## Sources & confidence
medium-high — SogAniMic/Stripe_coding_challenge `MultiTimeMap.ipynb` (verbatim statement and
example, 2023-01), Murillo2380 `medium-stripe-timestamp-cache`, LC 981 Stripe tag.

## Approach by part
1. per key parallel sorted lists `times / values / expires`; `set` = `bisect_right` + overwrite
   if `times[i-1] == time` else `insert` (out-of-order writes allowed); `get` =
   `bisect_right(times, t) - 1`.
2. `get_all` = the prefix `times[:bisect_right(times, t)]`, filtered by liveness.
3. TTL stored as an exclusive end `time + ttl`; alive iff `t < end`; the selected (latest) version
   decides — an expired newer version returns `None`, no fallback.
4. `first_missing_positive`: set membership walk from 1 (O(n) time, O(n) space).

## Conflicts resolved
The notebook pastes Daily Coding Problem #97's three example blocks as one sequence; as a single
map the second block contradicts the first (`get(1,0)` would be 1, not null). Primary reading:
three fresh maps (= DCP #97 / LC 981); documented under Variants and tested as three blocks.

## Pitfalls hidden tests target
- `get` at exactly the write time (`<=`); before first write → `null`; equal-time overwrite
- TTL: `time+ttl-1` alive, `time+ttl` expired, `ttl=0` never readable; no fallback to older version
- `GETALL` with nothing → empty line, not `null`; Part 4 `[]` → 1, duplicates, all-negative

## Complexity & measured cost
`get` O(log n); `set` O(log n) append / O(n) middle insert. Measured: 0.15s, 54 MB
(200k mixed SET/GET over 1000 keys; budget 2 s / 256 MB).

## Test inventory
15 tests — part1: 7 (incl. 1 perf) · part2: 2 · part3: 4 (incl. 1 io) · part4: 2; edge 7 · fmt 1.

## Skills exercised
S03 domain modeling · S12 time handling · S13 inclusive/exclusive boundaries · S18 error paths · S19 incremental design
