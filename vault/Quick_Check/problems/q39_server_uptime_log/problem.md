# q39 · Server Process Uptime Log — removal penalty, best removal time, aggregate logs, k removals

**Type:** phone screen (live coding, 1a/1b/2a) · **Stage:** Stripe phone interview · **Last asked:** 2022 (joeytor/StripeInterview), Glassdoor phone-screen question
**Frequency:** 3 independent sources (joeytor/StripeInterview `ServerPenalty.java` verbatim prompt; prashantrai/Algo_DS_InterviewPrep mirror `AnalyzeServerProcessUptimeLog.java`; Glassdoor QTN_4434801 `compute_penalty(server_log, remove_at)`) · **Confidence:** high

## Context
Stripe's infrastructure team keeps a simplified uptime log per server process: one digit per
hour, `1` = the process **crashed** during that hour ("down"), `0` = it did not ("up"). A server
can be **permanently removed from the network at the beginning of any hour**; it stays powered
on, just off the network. Removing too early wastes healthy hours, removing too late exposes the
network to crashes, so we define a penalty and look for the removal time that minimizes it.
This is the 0/1 twin of the store closing-time problem (q08).

## Input (stdin)
First line `PART n` (n ∈ 1..4). Blank lines ignored in Parts 1, 2, 4.
- Part 1: one query per line, `log|remove_at` — `log` is space-separated `0`/`1` tokens (an
  unspaced run `0010` is also accepted, one hour per character; an empty log is allowed: `|0`).
- Part 2: one log per line.
- Part 3: everything after the `PART 3` line is **one** aggregate log; it contains only the
  tokens `BEGIN`, `END`, `0`, `1`, spaces and newlines (a log may span lines).
- Part 4: one query per line, `log|k`.

## Output
- Part 1: the penalty per query. Part 2: the best `remove_at` per log. Part 3: one integer per
  valid log, in order of appearance (no output if none). Part 4: the minimum penalty per query.

## Rules
### Part 1 — `compute_penalty(log, remove_at) -> int`
`remove_at = x` means "removed before hour `x+1`"; it ranges from `0` (before the first hour)
to `n` (after the final hour). `penalty = (# of '1' among hours 1..remove_at) + (# of '0' among
hours remove_at+1..n)`: +1 for each DOWN hour while on the network, +1 for each UP hour after
removal.

### Part 2 — `find_best_removal_time(log) -> int`
The `remove_at` with the minimum penalty; **on a tie the smallest `remove_at`**. O(n): start
from `remove_at = 0` (penalty = number of `0`s) and slide. Empty log → 0.

### Part 3 — `get_best_removal_times(aggregate_log) -> list[int]`
Tokenize on whitespace. A valid log is `BEGIN`, zero or more `0`/`1` tokens, then `END`.
A `BEGIN` before the `END` **restarts** the log (the earlier tokens are discarded — "we'll only
consider inner BEGINs and ENDs"); an `END` without an open `BEGIN` is ignored; tokens outside a
`BEGIN…END` pair are ignored. Return the best removal time of every valid log in order.

### Part 4 — `min_penalty_k(log, k) -> int` (reconstructed)
Now a removed server may be **re-attached** at the beginning of any later hour, and removed
again, **at most `k` times** (k off-network intervals). Penalty as in Part 1: +1 per DOWN hour
on the network, +1 per UP hour off the network. `k = 0` → the server is never removed
(penalty = number of `1`s). Note `k = 1` is *not* Part 2: the single off interval may end before
the log does. Return the minimum penalty (DP over hours × removals used × on/off).

## Worked examples
Verbatim from the source:
```
PART 1
0 0 1 0|0        -> 3      (three UP hours after removal)
0 0 1 0|4        -> 1      (one DOWN hour before removal)
0 0 1 0|2        -> 1
PART 2
0 0 1 1          -> 2
0 0 1 0          -> 2      (penalties by remove_at 0..4 = 3,2,1,2,1 -> min 1 first at 2)
PART 3
BEGIN BEGIN
BEGIN 1 1 BEGIN 0 0
 END 1 1 BEGIN   -> 2      (the only valid log is "BEGIN 0 0 END")
```
(`"BEGIN BEGIN BEGIN 1 1 BEGIN 0 0 END 1 1 BEGIN"` likewise → `[2]`.)
```
PART 4
0 1 0|0          -> 1
0 1 0|1          -> 0      (off during hour 2 only)
1 0 1 0 1|1      -> 2
1 0 1 0 1|2      -> 1
1 0 1 0 1|3      -> 0
```

## Edge cases hidden tests are known to target
- `remove_at = 0` and `remove_at = n` (both ends are legal); empty log → penalty 0, best 0
- all `0` → best `n`; all `1` → best `0`; tie → smallest (`1 0` → penalties 1,2,1 → 0; `0 1 0 1` → 1)
- Part 3: nested `BEGIN` restarts; `END` without `BEGIN`; unfinished trailing `BEGIN`; logs across
  line breaks; an empty valid log `BEGIN END` → 0; several logs → several answers in order
- unspaced `0010` accepted like `0 0 1 0`
- Part 4: `k` larger than needed (never worse than fewer removals); `k = 0`

## Variants seen in the wild
- q08 store closing time (`Y`/`N`, `BEGIN`/`END`) — identical structure with letters; LC 2483.
- Named servers `name: log` one per line → the same Part 2 per line (InterviewDB "Closing Time").

## What this tests
skills: S02 parsing · S05 off-by-one / boundary discipline · S08 deterministic tie-break · S10 state machine over tokens · S18 malformed input · S19 incremental design · S20 self-testing (the prompt asks for tests)

## Sources
- https://github.com/joeytor/StripeInterview `src/main/java/ServerPenalty.java` (README → Phone Interview; verbatim prompt)
- https://github.com/prashantrai/Algo_DS_InterviewPrep `src/Stripe/AnalyzeServerProcessUptimeLog.java` (mirror)
- https://www.glassdoor.com/Interview/Write-a-function-compute-penalty-that-computes-the-total-penalty-given-a-server-log-as-a-string-AND-a-time-at-which-we-re-QTN_4434801.htm
