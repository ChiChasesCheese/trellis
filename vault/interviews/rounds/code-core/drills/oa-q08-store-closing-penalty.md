---
nodes: [algorithms.prefix, model.state-machine, transfer.stripe-oa]
tags: [stripe-oa, q08]
---
# Drill: find the best closing hour, then recover logs from noisy text

Sixty minutes, stdin to stdout, no libraries beyond the standard one. A
store's hourly log is a string of `Y` (customers present) / `N` (empty)
tokens. A closing time `t` in `[0, n]` means open for hours `1..t` and closed
for `t+1..n`; the penalty is the number of `N` hours while open plus the
number of `Y` hours while closed. Build up to recovering many such logs
buried in a noisy text dump.

- Part 1: given a log and a closing time, compute the penalty.
- Part 2: given a log, find the closing time with the minimum penalty in
  O(n) — not by trying every `t` and recomputing from scratch — breaking
  ties toward the smallest `t`.
- Part 3: given one long aggregate text blob (tokens may span lines), extract
  every well-formed `BEGIN ... END` log, discard anything malformed or
  outside a block, and report the best closing time for each valid log found,
  in order of appearance.

**Constraints to state and honor**
- The answer space for closing time is `[0, n]` — n+1 candidates, one more
  than the number of hours.
- Part 2 must scale to ~10^6 hours in one pass, using a running total that
  updates by +1/-1 as the candidate closing time slides, not by recomputing
  the sum from scratch each time.
- Part 3: a second `BEGIN` before a matching `END` discards everything
  collected so far and restarts (blocks do not nest); an `END` with no open
  `BEGIN` is ignored; an unfinished trailing `BEGIN` at end of input is
  ignored; any non-`Y`/`N` token inside an open block invalidates that whole
  log (discarded at its `END`), while tokens outside any block are just
  ignored garbage.
- `BEGIN END` (an empty log) is valid and its best closing time is 0.

**Grading points**
- Part 2's tie-break correctness rests entirely on using a strict `<` (not
  `<=`) when updating the running best, so the first time the minimum penalty
  is reached — the smallest `t` — is the one kept.
- The running-total update direction is stated explicitly: moving the
  candidate closing time one hour later turns that hour from closed to open,
  so an `N` there now counts against penalty (+1) and a `Y` no longer does
  (-1).
- Off-by-one discipline on the `t ∈ [0, n]` boundary is exercised at both
  ends (`t=0` = never open, `t=n` = open all day) and on short logs (`N Y`
  has penalties 1,2,1 so the tie between `t=0` and `t=2` resolves to `t=0`).
- Part 3 is a small explicit state machine (open/valid flags) reused with
  Part 2's logic unchanged for each recovered log — not a rewritten
  closing-time computation.
- Case sensitivity is exact: lowercase `y`/`n`/`begin` are never recognized —
  inside a block they invalidate it, outside a block they're ignored garbage.
- A candidate should be able to name the six malformed-input categories Part
  3 must handle: restart-on-BEGIN, orphan END, unfinished trailing BEGIN,
  garbage inside a block, garbage outside a block, and the empty-log case.

**Source**
- `vault/stripe/q08_store_closing_penalty/question.md`
- `vault/stripe/q08_store_closing_penalty/solution.md`
- `vault/Quick_Check/problems/q08_store_closing_penalty/problem.md`
- `vault/Quick_Check/problems/q08_store_closing_penalty/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
