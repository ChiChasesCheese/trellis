# q08 · Store Closing-Time Penalty — Y/N hourly log, best closing hour, BEGIN/END aggregate logs

**Type:** bespoke OA / phone screen (LC 2483 "Minimum Penalty for a Shop", Stripe tag) · **Stage:** HackerRank OA (3 parts) and phone screen (parts 1a/1b/2a) · **Last asked:** 2026-07 (InterviewDB "Closing Time — Phone"), 2025-12 (Hazeera65 / TWINSRIRAM repos), 2026-02 (extrabrain)
**Frequency:** 9 independent sources (femisowems repo w/ verbatim I/O, yingw787 pytest vectors, pkafel gist, Hazeera65, TWINSRIRAM, LC 2585038 phone screen, LC 3950781 Dublin variant, Blind bj5ehdwf, extrabrain/linkjob, 1point3acres 844359) · **Confidence:** high

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

## Edge cases hidden tests are known to target
- closing_time 0 and n (both ends), log of length 1 (`Y` → 1, `N` → 0)
- all `N` → 0; all `Y` → n; ties resolved to the smallest time: `Y N` has penalties 1,0,1 → 1;
  `N Y` has penalties 1,2,1 → 0 (t=0 and t=2 tie, the smaller wins); `Y N Y N` → 1
- O(n) for 10^6 hours (the phone-screen follow-up explicitly asks for prefix sums)
- Part 3: logs spanning lines, several per line, `BEGIN` restart, `END` without `BEGIN`, unfinished
  trailing `BEGIN`, garbage tokens outside and inside (inside → invalid), empty `BEGIN END` → 0,
  lowercase `y`/`n` or `begin` are not recognised (invalid inside, garbage outside)

## Variants seen in the wild
- **Stack / nested interpretation** (Hazeera65 phone-screen notes): `BEGIN … BEGIN … END … END`
  handled with a stack, inner block reported first and the outer block includes the inner tokens.
  Conflicts with "cannot be nested" (femisowems) and the restart vector (yingw787); not implemented.
- **Dublin L2 variant** (LC 3950781): days instead of hours, index-based loss, then "very random"
  logs with `L`/`R` tokens to extract — same tokenizer with a different alphabet.
- Prose in femisowems Problem4.md claims `4` / `7` for the sample; its own expected_output.txt says
  `2` / `8` — the harness wins.
- LeetCode 2483 uses a plain string `"YYNY"` with no spaces (accepted here).

## What this tests
skills: S02 tokenizing noisy text · S05 off-by-one discipline on `t ∈ [0, n]` · S08 smallest-on-tie
· S10 state machine over a token stream (BEGIN/END) · S18 invalid / unfinished input handling ·
S19 incremental design (Part 3 reuses Part 2)

## Sources
- https://github.com/femisowems/stripe-interview-questions/tree/main/question4 (verbatim statement + sample_input/expected_output)
- https://github.com/yingw787/stripe-interview (2024-04-04, pytest vectors incl. the BEGIN-restart case)
- https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1 (2023-10-15, Kotlin parts 1–3)
- https://github.com/Hazeera65/stripe-interview/tree/main/round1/PhoneScreen (parts 1/2/3, stack variant)
- https://github.com/TWINSRIRAM/Stripe_OA_Prep/tree/main/part1-3
- https://leetcode.com/discuss/interview-question/2585038/ ("Stripe | Phone Screen | Senior SE | Reject", 2022-09-16)
- https://leetcode.com/discuss/post/3950781/ (Dublin L2 variant)
- extrabrain.app 2026-02-10 / linkjob.ai 2025-09-16 (OA 3-part listing); 1point3acres thread-844359; jointaro "Minimum Penalty for a Shop"
