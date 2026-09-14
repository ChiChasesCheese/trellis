---
nodes: [algorithms.settlement, algorithms.backtracking, transfer.stripe-oa]
tags: [stripe-oa, q32]
---
# Drill: rebalance bank accounts to a minimum, then minimize transfers

Sixty minutes, stdin to stdout. A set of bank accounts, some above a minimum balance and some
below, must be rebalanced by transfers between them — "a working solution, not necessarily the
optimal one," as the interviewer puts it. Part 1 asks for feasibility (is the total enough to
bring everyone to the minimum?) and a deterministic transfer list built by walking sources and
sinks in input order. Part 2 asks for the fewest possible transfers — only accounts below the
minimum must be topped up, accounts above it need not be drained, and this is the LC 465 "optimal
account balancing" problem in disguise. Part 3 reverses the question: given a list of transfers
already made, replay them and classify the result as fully settled, incomplete, best-effort, not
best-effort, or invalid partway through. Part 4 adds a flat fee deducted from the sender on every
transfer.

**Constraints to state and honor**
- Feasibility is `sum(balances) >= minimum * n`; equality is feasible (everyone lands exactly at
  the minimum), one unit short is `IMPOSSIBLE`.
- No transfer may ever leave its source below the minimum, and a transfer amount must be
  positive; accounts already all at or above the minimum produce no output at all — not
  `IMPOSSIBLE`, not an empty line.
- Part 2's exact search only needs to consider the accounts with a nonzero net against the
  minimum; an exact search is tractable up to roughly a dozen such accounts, and a sorted greedy
  fallback is required beyond that, at the cost of being a heuristic (not guaranteed minimal).
- Part 3's verdicts hinge on two conditions: whether a full solution existed (`sum >= min * n`)
  and whether any account still sits above the minimum while another is short — both must be
  computed after applying the given transfers, not before.
- An invalid transfer in Part 3's list (unknown account, non-positive amount, or a self-transfer)
  stops replay at that point — everything before it applies, everything after it is skipped.

**Grading points**
- Feasibility and the transfer-building step kept as separate concerns: check feasibility once,
  then run whichever of the four transfer strategies the part calls for.
- Part 2's DFS with branch-and-bound over deficits sorted by (size desc, name) and sources sorted
  by (surplus desc, name), pruning when transfers-so-far plus remaining open deficits can't beat
  the best count found — and a clear, spoken threshold for when to fall back to the greedy
  heuristic instead of pretending the greedy is exact.
- The Part 3 verdict table implemented as one small function, not scattered conditionals: `OK` /
  `INCOMPLETE` / `BEST_EFFORT` / `NOT_BEST_EFFORT` / `INVALID`, each with its own precise boundary.
- Fee accounting in Part 4 as one extra deduction on the sender's side per transfer
  (`usable = surplus - fee`, skip a source once its surplus can't cover even the fee), plus a
  running total printed at the end.
- Negative balances, a single account, and a deficit that needs several sources to fill, all
  exercised as distinct cases rather than assumed to fall out of the general logic.
- 500 accounts must run fast in the greedy paths; the exact search is deliberately bounded so it
  never runs on the full-size input.

**Source**
- `vault/interviews/companies/stripe/problems/q32_money_transfer_rebalancing/problem.md`, `vault/interviews/companies/stripe/problems/q32_money_transfer_rebalancing/REPORT.md`, `vault/interviews/companies/stripe/problems/q32_money_transfer_rebalancing/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q32_money_transfer_rebalancing.md`, `vault/interviews/companies/stripe/study/10-solutions/q32_money_transfer_rebalancing.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
