# q39 Server Uptime Log — report

## Summary
The 0/1 twin of q08: a per-hour crash log (`1` = crashed, `0` = up), a penalty for removing the
server at a given hour, the best removal hour, and recovery of valid logs from a noisy
`BEGIN`/`END` aggregate file. Part 4 (reconstructed) generalizes to at most `k` off-network
intervals with a small DP. The prompt explicitly asks the candidate to write tests.

## Sources & confidence
high — joeytor/StripeInterview `ServerPenalty.java` (verbatim prompt, README → Phone Interview),
prashantrai mirror, Glassdoor QTN_4434801 (`compute_penalty(server_log, remove_at)`).

## Approach by part
1. `hours[:remove_at].count('1') + hours[remove_at:].count('0')`; `remove_at ∈ [0, n]`.
2. one O(n) slide from `remove_at = 0` (penalty = #`0`): `+1` for a `1`, `-1` for a `0`; strict
   `<` keeps the smallest hour on a tie (the source's Java does the same).
3. token state machine: `BEGIN` (re)starts, `END` closes if a log is open, everything else outside
   is ignored; tokens other than `0`/`1` inside a log are ignored (the spec guarantees none).
4. DP over hours with `on[j]` / `off[j]` (j = off-intervals used); removal costs one interval,
   re-attach is free; answer `min(on + off)`. O(n·k).

## Conflicts resolved
The task sketch said "`1` = process running"; the source says `1` = crashed/down, `0` = up, and
its examples (`compute_penalty("0 0 1 0", 0) = 3`) only work that way — the source wins. The
sketch's "multiple servers separated by `;`/named lines" is listed as a variant; the source's
Part 2a (BEGIN/END aggregate) is Part 3.

## Pitfalls hidden tests target
- `remove_at = 0` and `= n`; empty log; tie → smallest hour (`1 0` → 0, `0 1 0 1` → 1)
- nested `BEGIN` restarts, `END` without `BEGIN`, trailing unfinished `BEGIN`, `BEGIN END` → 0,
  logs spanning lines; unspaced `0010`
- Part 4: `k = 0` = number of `1`s; `k = 1` can beat Part 2 (off interval may end early)

## Complexity & measured cost
Parts 1–3 O(n); Part 4 O(n·k). Measured: 0.08s, 36 MB (10^6-hour log, Part 2; the perf test
also runs 5000 aggregate logs; budget 2 s / 256 MB).

## Test inventory
14 tests — part1: 3 · part2: 4 (incl. 1 perf) · part3: 4 (incl. 1 io) · part4: 3; edge 5 (+ 2 brute-force cross-checks).

## Skills exercised
S02 parsing · S05 boundary discipline · S08 deterministic tie-break · S10 token state machine · S18 malformed input · S19 incremental design · S20 self-testing
