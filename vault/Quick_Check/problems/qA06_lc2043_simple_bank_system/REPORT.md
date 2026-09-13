# qA06 LC 2043 Simple Bank System — report

## Summary
Validate-then-mutate ledger class: 1-indexed accounts, `transfer / deposit / withdraw` returning
validity and applying no partial effect on failure. Tag freq 61–67 on three mirrors. It is the
skeleton of q13 (balance ledger + platform lender), q27 (PaymentLedger, programhelp VO ×4) and q32;
the follow-ups add a transaction log with reversals (refunds) and q13's platform lending.

## Sources & confidence
high (tag) — liquidslr All 61.2 / >6mo 67.1, snehasishroy 62.5, github_repos.md §30; follow-up
framing from the programhelp PaymentLedger reports. Parts 2–3 are designed, mirroring q13/q27 rules.

## Approach by part
1. Two primitives `_debit` / `_credit`; every public op validates (both accounts of a transfer
   first) and only then mutates. Withdrawing exactly the balance is valid; amount 0 is valid.
2. `TxnRecord` NamedTuple appended for every call (failed ones and `reverse` itself included), ids
   1..k. `reverse` succeeds iff the record exists, was ok, is not a reverse, not already reversed,
   and the undo is fundable (deposit undo debits, transfer undo debits `dst`); reversals never borrow.
3. `_debit` lends `shortfall` from `reserve` when `reserve >= shortfall` (account ends at 0, debt
   grows); `_credit` repays `min(debt, incoming)` first. `max_outstanding` tracked with a running
   sum, not `sum(debt)` per call. `reserve=0` degenerates to Part 1.

## Pitfalls hidden tests target
- account 0 / n+1 / negative ids; a failed transfer must not debit the source; `a == b` transfers
- `==` balance withdraw valid, one more invalid; 10^12 × 10^4 sums (Python ints, no floats)
- reversing failed / already-reversed / reverse records; unfundable reversals leave state intact
- shortfall exactly equal to the reserve; repayment capped at the debt; no loans for reversals

## Complexity & measured cost
O(1) per operation, O(n) init. Measured: 0.10s (10^4 random ops on 10^5 accounts in-process +
script run); script run at LC max ≈ 0.06 s, ~35 MB. Budget 2 s / 256 MB.

## Test inventory
16 tests — part1: 8 (incl. 1 io, 1 perf) · part2: 4 · part3: 4; edge 9 · fmt 0.

## Skills exercised
A08 design/simulation with validation · S03 state per account · S10 reversals · S17 ledger balances · S18 validation · S19 incremental design
