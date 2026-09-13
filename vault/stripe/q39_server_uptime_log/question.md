# q39 · Server Process Uptime Log — removal penalty, best removal time, aggregate logs, k removals

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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s20-self-test-discipline|S20 自测纪律]]
