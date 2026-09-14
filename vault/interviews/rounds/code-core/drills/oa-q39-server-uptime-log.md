---
nodes: [algorithms.prefix, algorithms.dp, transfer.stripe-oa]
tags: [stripe-oa, q39]
---
# Drill: the best time to remove a crashing server from the network

Sixty minutes, stdin to stdout. A server's uptime log is one `0`/`1` digit
per hour (`1` = crashed that hour); the server can be permanently removed
from the network at the start of any hour, and the penalty is one point per
crashed hour it stayed on the network plus one point per healthy hour after
it was pulled. Part 1 computes the penalty for a given removal hour. Part 2
finds the removal hour with the minimum penalty in one linear pass,
tie-breaking to the earliest hour. Part 3 recovers valid logs from a noisy
aggregate file that uses `BEGIN`/`END` markers and may contain restarts and
unmatched tokens. Part 4 generalizes to at most `k` removal-and-reattachment
intervals, solved with a small DP.

**Constraints to state and honor**
- `remove_at` ranges over `[0, n]` inclusive — removing before the first hour
  and after the last hour are both legal.
- Part 1's input allows a spaced log (`0 0 1 0`) or an unspaced run (`0010`);
  an empty log is allowed.
- Part 3's aggregate stream has only the tokens `BEGIN`, `END`, `0`, `1`; a
  `BEGIN` before a matching `END` restarts the log (discarding what came
  before), a stray `END` is ignored, and a log may span lines.
- Part 4's `k` off-network intervals may each end before the log does —
  `k = 1` is not the same question as Part 2.
- Time/memory budget: O(n) for Parts 1–3, O(n·k) for Part 4.

**Grading points**
- Part 2 as one O(n) slide from `remove_at = 0` (penalty = count of zeros),
  adjusting by ±1 per hour — not a re-scan per candidate removal time.
- Get the polarity right and say it out loud: `1` (crashed) costs while on
  the network, `0` (healthy) costs after removal — easy to invert under
  pressure, worth a hand-checked example before coding.
- Tie-breaking on the minimum penalty is strict `<`, keeping the smallest
  `remove_at` — state that explicitly rather than leaving it to whichever
  comparison happens to run first.
- Part 3 is a small token state machine, not a regex hack: nested `BEGIN`,
  an unmatched `END`, and a trailing unclosed `BEGIN` are three separate
  behaviors to test.
- Part 4's DP tracks hours × intervals-used × on/off state; `k = 0` reduces
  to "never removed", and a larger `k` than needed must never make the
  answer worse.
- The prompt itself asks for tests — write the hand-computed examples
  (`1 0`, `0 1 0 1`) into the suite rather than skipping straight to the DP.

**Source**
- `vault/interviews/companies/stripe/problems/q39_server_uptime_log/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q39_server_uptime_log.md`, `vault/interviews/companies/stripe/problems/q39_server_uptime_log/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
