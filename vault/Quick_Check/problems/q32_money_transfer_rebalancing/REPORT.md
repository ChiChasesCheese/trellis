# q32 Money Transfer / Rebalancing — report

## Summary
Move money between bank accounts so every account holds at least the minimum (Stripe's real
treasury/regulatory rebalancing, simplified). Part 1 wants "a working solution, not the optimal
one"; the follow-ups asked in phone screens and VOs are: fewest transfers (LC 465 flavour), audit
a given transfer list ("is it best effort when the goal is impossible?"), and — reconstructed —
per-transfer fees.

## Sources & confidence
high — verbatim statement, example and both follow-ups in joeytor `MoneyTransfer.java` (VO coding)
and sahaia1's Python port; LeetCode 5647506 (2024 phone screen quotes the same text); LeetCode
7521596 (2026 VO min-transactions settlement); 1point3acres thread-1029620 ("Money Transfer" with
optimisation follow-ups); programhelp 2026-02 VO (settlement + DFS + audit); Hazeera65 LC 465 folder.
Conflict: joeytor/sahaia1 sort accounts by balance for Part 1; the source's expected output is
reproduced only by an **input-order** two-pointer, which is what Part 1 uses (the sorted greedy is
Part 2's fallback and Part 4's engine). The Java prints doubles (`20.0`); we use integer units.

## Approach by part
1. `feasible = sum ≥ min·n`; input-order two-pointer on sources/sinks with `amount = min(surplus, deficit)`.
2. `min_transfers_exact`: DFS over deficits (desc) choosing sources (desc) with branch-and-bound
   (`transfers so far + open deficits ≥ best` prunes), sources for one deficit in increasing index,
   equal remaining surpluses deduplicated. Only deficits must be settled (surplus may stay). Used when
   ≤ 12 non-zero accounts, else the sorted greedy heuristic (documented: 3 vs optimal 2 on the example).
3. Apply transfers; verdict `OK` / `INCOMPLETE` (feasible but short) / `BEST_EFFORT` (infeasible and
   nobody above min) / `NOT_BEST_EFFORT` / `INVALID` (unknown account, amount ≤ 0, self-transfer; stop there).
4. Greedy with `usable = surplus − fee` per transfer; prints `FEES: total`; `IMPOSSIBLE` when uncovered
   (exact only for fee = 0 — stated as heuristic).

## Pitfalls hidden tests target
- feasibility boundary `sum == min·n`; no output (not `IMPOSSIBLE`) when nothing to do
- sources must never dip below min; negative balances; a deficit covered by several sources
- Part 2 must beat the greedy on the verbatim example (2 vs 3); LC 465 samples
- audit boundaries: exactly min is `OK`; `BEST_EFFORT` needs *no* account above min; invalid transfer stops
- `- ` bullets and spaces around `:` / `,`; `MIN` override

## Complexity & measured cost
Parts 1/4 O(n log n); Part 3 O(n + t); Part 2 exact exponential in ≤ 12 accounts (≤ 1 ms on random
6×6 and on the adversarial distinct-value case). Measured: 0.17s, 55 MB (500 accounts + 100k audited transfers).

## Test inventory
19 tests — part1: 6 · part2: 5 · part3: 4 · part4: 4 (incl. 1 io, 1 perf); edge 9.

## Skills exercised
S02 parsing · S03 records keyed by id · S05 threshold/feasibility semantics · S08 deterministic
ordering · S09 exact formatting · S17 ledger balances · S18 validation (audit) · S19 incremental
design · A10 LC 465 DFS with pruning
