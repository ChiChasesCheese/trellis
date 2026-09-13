# q17 Datacenter Request Router — report

## Summary
A small stateful command processor: register regions with coordinates and capacity, flip
health, compute Haversine distances, and route each request to the nearest healthy region that
still has capacity (consuming one unit). It is Stripe's "proximity-aware request routing" OA
(Aug 2026, SSE3/L3). Difficulty is in validation discipline (invalid commands must not mutate),
the exact ROUTE output line (chosen + rounded distance + ranked candidates), and tie-breaks.

## Sources & confidence
high — LeetCode 8470971 (verbatim commands + samples, 2026-08-19), PracHub full spec
(JSON variant, R = 6371, `floor(d+0.5)`), 1point3acres 题库 (last asked 2026-08-11), InterviewDB.
Conflicts resolved: (1) tie at equal distance — prose in two sources says alphabetical, the
LeetCode sample shows registration order → primary `tie="name"`, variant `tie="registration"`
tested; (2) the post's `DISTANCE 0 0 100 100 → 10200` does not match the standard formula
(9815; 10200 = value for lat 80) → treated as a transcription slip, PracHub's `4000` sample
matches to the metre and is used instead.

## Approach by part
1. `Router.regions[name] = {lat, lon, cap, healthy, load, idx}`; `REGISTER` checks arity, integer
   types, inclusive bounds ±90/±180, `cap > 0`, uniqueness. `SET_HEALTHZ` accepts `true/false`
   case-insensitively.
2. `haversine_km` with R = 6371; printing uses `floor(d + 0.5)` (half-up, not banker's).
3. `ROUTE`: candidates = healthy regions ranked by `(unrounded distance, name)`; chosen = first
   with `load < cap`; `load += 1`; `NONE 0 <candidates>` when none. Region radians/cos are
   pre-computed at registration so ROUTE is one sin/asin per region.
4. (reconstructed) `RELEASE region`: `load -= 1` if `load > 0`, else `ERROR`.

## Pitfalls hidden tests target
- `ERROR` commands must leave state untouched (duplicate REGISTER keeps original coordinates)
- `NONE 0` still lists healthy-but-full regions as candidates; unhealthy regions vanish entirely
- capacity boundary: the `cap`-th ROUTE succeeds, the next is `NONE`; load survives health flips
- ranking by unrounded distance, output rounded; `x.5` rounds up
- arity/type errors: `ROUTE 1`, `REGISTER a 1.5 2 3`, unknown command

## Complexity & measured cost
O(C · R log R) for C ROUTEs over R healthy regions (R is small in practice).
Measured: 1.28s, 65 MB (100k commands, 50 regions; budget 2 s / 256 MB).

## Test inventory
24 tests — part1: 5 · part2: 4 · part3: 12 (incl. 2 io, 1 perf, 2 variant flags) · part4: 3; edge 12 · fmt 1.

## Skills exercised
S01 whole-spec design · S02 typed parsing · S03 state per region · S08 tie-breaks · S09 exact output · S18 validation/error paths · S19 incremental · S21 stdlib math
