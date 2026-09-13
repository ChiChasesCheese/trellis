# q08 · Store Closing-Time Penalty — Y/N hourly log, best closing hour, BEGIN/END aggregate logs

## Context
A merchant on Stripe Terminal keeps an hourly log of whether customers were in the store:
`Y` = customers present that hour, `N` = empty. Head office wants to know when the store should
have closed. Closing time `t ∈ [0, n]` means the store is open for hours `1..t` and closed for
`t+1..n` (`0` = never opened, `n` = open all day). Every open hour without customers wastes
staff; every closed hour with customers loses sales. Part 3 is the ops-data reality: many days'
logs are dumped into one noisy text file delimited by `BEGIN` / `END` tokens and must be recovered.

## Input (stdin)
First line `PART n` (n ∈ 1..3). Blank lines are ignored in Parts 1–2.
- Part 1: one query per line, `log|closing_time` (log = `Y`/`N` tokens separated by spaces; an
  empty log is allowed: `|0`).
- Part 2: one log per line.
- Part 3: everything after the `PART 3` line is **one** aggregate log (whitespace-separated
  tokens, may span lines; line breaks are just whitespace).
Logs are whitespace-separated single letters; a run without spaces (`YYNY`) is also accepted
(each character is one hour).

## Output
- Part 1: the penalty, one integer per query line.
- Part 2: the best closing time, one integer per log.
- Part 3: one integer per **valid** log found, in order of appearance (no output if none).

## Rules
### Part 1 — `compute_penalty(log, closing_time) -> int`
`penalty = (# of 'N' among hours 1..closing_time) + (# of 'Y' among hours closing_time+1..n)`.
`closing_time` is guaranteed in `[0, n]`.

### Part 2 — `find_best_closing_time(log) -> int`
The closing time with the minimum penalty; **on a tie, the smallest closing time**. Must be O(n)
(prefix sums or a single running pass), not O(n²). Empty log → 0.

### Part 3 — `get_best_closing_times(aggregate_log) -> list[int]`
Tokenize on whitespace. A valid log is `BEGIN`, then zero or more `Y`/`N` tokens, then `END`.
- `BEGIN` starts a log. A **second `BEGIN` before `END` discards the earlier tokens and restarts**
  (logs cannot be nested — the inner `BEGIN` is the one that counts).
- `END` without an open `BEGIN` is ignored; an unfinished `BEGIN …` at the end of input is ignored.
- Any token other than `Y`/`N` (or a run of them) inside a log makes that log **invalid**; it
  is discarded at its `END` (the next `BEGIN` starts fresh).
- Tokens outside `BEGIN … END` (garbage) are ignored.
- `BEGIN END` (empty log) is valid and yields best time `0`.
For each valid log, in order, output `find_best_closing_time(log)`.

## Worked examples
Example 1 (Part 1):
```
PART 1
Y Y N Y|0
Y Y N Y|1
Y Y N Y|2
Y Y N Y|4
N Y N Y|2
Y Y Y N N N N|3
|0
```
→ `3`, `2`, `1`, `1`, `2`, `0`, `0`. (`Y Y N Y`, t=2: hours 1–2 open with customers → 0; hours
3–4 closed: hour 4 had customers → 1.)

Example 2 (Part 2):
```
PART 2
Y Y N Y
Y Y N N
N N N N
Y Y Y Y
N Y Y Y Y N N N Y N N Y Y N N N N Y Y N N Y N N N
Y Y N N N Y Y N Y Y N N N Y Y N N Y Y Y N Y N Y Y
```
→ `2` (penalties 3,2,1,2,1 → first minimum at 2), `2`, `0`, `4`, `5`, `25`.

Example 3 (Part 3, verbatim repo sample):
```
PART 3
BEGIN
Y Y N Y N N N Y Y N
END
GARBAGE
BEGIN
N N Y Y Y N Y Y
END
```
→ `2`, `8`.

Example 4 (Part 3, restart / stray END — yingw787 vector):
```
PART 3
BEGIN BEGIN
BEGIN N N BEGIN Y Y
 END N N END
```
→ `2` only: the fourth `BEGIN` restarts with `Y Y`; the trailing `N N END` has no open `BEGIN`.

Example 5 (Part 3, invalid and empty logs):
```
PART 3
BEGIN Y X N END BEGIN END BEGIN Y Y END BEGIN N
```
→ `0`, `2`: the first log contains `X` → invalid; `BEGIN END` → 0; `Y Y` → 2; the last is unfinished.

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
