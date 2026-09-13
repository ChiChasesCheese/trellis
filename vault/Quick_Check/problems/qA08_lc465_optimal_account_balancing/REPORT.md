# qA08 LC 465 Optimal Account Balancing — report

## Summary
Fewest transfers that settle a group of IOUs: the LeetCode Hard that shows up as the *follow-up* to
Stripe's bank-rebalancing problem (q32 Part 2) and as a stand-alone "algorithm" VO round (programhelp
2026-04, LC discuss 2026-01). Net the parties, drop zeros, exact search over ≤ 12 non-zero nets with
three prunings, cross-checked by the bitmask DP `n − max #zero-sum subsets`. Follow-ups: return the
transfers (payout instructions) and write off dust balances below a fee threshold with a platform
account absorbing the residual.

## Sources & confidence
tag freq 51.5 (shreeratn 2025-05; absent from the liquidslr/snehasishroy mirrors); 3 dated candidate
reports (programhelp H1 2026-04-02, H3 2026-02-27, LeetCode 7521596 2026-01-24) + Hazeera65 repo
folder → high as a follow-up, medium as a stand-alone. Part 3 (write-off) is designed, marked so.

## Approach by part
1. `net_balances`: credit = given − received (`[a,b,x]` ⇒ b owes a), zeros dropped, ascending id.
   `_search`: DFS settling the first unsettled party against each later opposite-sign party; prunings —
   duplicate current values at a level, `break` after an exact cancel, branch-and-bound on the best
   count. `min_transfers_bitmask`: `dp[mask] = max_i dp[mask^i] + [sum(mask)==0]`, answer `n − dp[full]`.
2. `settle`: the same DFS keeps the path; the first list with the minimal count wins (strict `<`), so
   output is deterministic (ascending-id search order). Chains (over-pay then forward) are allowed.
3. `settle_with_writeoff`: parties with `0 < |net| < threshold` (strict) are dropped; if the rest do
   not sum to zero a `PLATFORM` party (id −1, sorted first) takes the residual; then Part 2's search.

## Pitfalls hidden tests target
- sign of the net: reversing it reverses every transfer (count unchanged — easy to miss)
- pass-through parties (net 0) must be dropped before the search, or the DP/DFS over-count
- `n − 1` is wrong whenever a proper zero-sum subset exists (LC ex2 → 1, two-pair case → 2)
- duplicate-value pruning must compare *current* values at that level, not original nets
- the exact-cancel `break` is only safe after trying that j (not before)
- Part 3: `|net| == threshold` is settled; written-off nets that cancel exactly → no PLATFORM party

## Complexity & measured cost
DFS: O(n · 2^n)-ish worst case in theory (n ≤ 12 non-zero nets), milliseconds with the prunings; DP:
O(2^n · n) time, O(2^n) memory. Measured: 0.17 s for the perf test (12-net worst shape + slowest-of-3000
random instance + 200 random LC-max instances through both solvers + one script run); script run on
the 12-net case 0.03 s, ~16 MB. Budget 2 s / 256 MB.

## Test inventory
16 tests — part1: 8 (incl. 1 perf) · part2: 5 (incl. 1 io) · part3: 3; edge 7 · fmt 1.

## Skills exercised
A10 min transactions to settle debts · S03 domain records · S17 ledger balances · S19 incremental design · S21 recursion + bitmask DP
