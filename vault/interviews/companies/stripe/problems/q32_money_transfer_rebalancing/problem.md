# q32 · Money Transfer — bank-account rebalancing (every account ≥ minimum)

**Type:** phone screen + virtual onsite coding (2021–2026) · **Stage:** phone ("Optimizing Money Transfer",
1point3acres phone list) and VO coding (joeytor README; programhelp VO 2025-08, 2026-02) · **Last asked:**
2026-04 (programhelp VO: LC 465 follow-up) · **Frequency:** 8 independent sources (joeytor Java header,
sahaia1 Python, LeetCode 5647506, LeetCode 7521596, 1point3acres thread-1029620, programhelp ×2,
Hazeera65 LC465 folder) · **Confidence:** high (P1 verbatim; P2 follow-up confirmed; P3 follow-up
described; P4 reconstructed)

## Context
"At Stripe we keep track of where the money is and move money between bank accounts to make sure
their balances are not below some threshold. This is for operational and regulatory reasons, e.g. we
should have enough funds to pay out to our users, and we are legally required to separate our users'
funds from our own." There are at most 500 bank accounts, some above the minimum (100) and some
below. Move money between them so that they all have at least the minimum — "we are not looking for
the optimal solution, but a working one" — then, as follow-ups, minimise the number of transfers,
audit a given list of transfers, and account for transfer fees.

## Input (stdin)
First line `PART n`. Then, in any order (blank lines ignored, a leading `- ` bullet tolerated):
- `MIN m` — the minimum balance (default 100); `FEE f` — flat fee per transfer (Part 4, default 0)
- account lines `NAME: balance` (integer units, may be negative; names unique, case-sensitive)
- transfer lines `from: A, to: B, amount: N` (Part 3 only), applied in input order

## Output
Transfer lines exactly as `from: A, to: B, amount: N` (Parts 1, 2, 4), one per line, in the order
they are made; **no output at all when no transfer is needed**; the single line `IMPOSSIBLE` when
the accounts cannot all reach the minimum. Part 3 prints balances then a verdict (below).

## Rules
### Part 1 — any working solution (verbatim task)
Feasible iff `sum(balances) ≥ minimum × number_of_accounts`; otherwise print `IMPOSSIBLE`.
Deterministic greedy **in input order**: walk sources (balance > min) and sinks (balance < min) each
in input order; transfer `amount = min(source − min, min − sink)`; advance the source when it reaches
the minimum, the sink when it is satisfied. This reproduces the source's expected output exactly.

### Part 2 — fewest transfers (interviewer's definition of "optimal", = LC 465 flavour)
Print a transfer list of **minimum length**. Let `net = balance − min`; only accounts with `net < 0`
(deficits) must be fixed, accounts with `net > 0` are sources and need not be drained. Exact answer
by DFS with branch-and-bound over deficits sorted by (deficit desc, name) and sources sorted by
(surplus desc, name): each transfer moves `min(source_remaining, deficit_remaining)` (an optimal
solution always exists in which every transfer settles the sink or drains the source); sources for
one deficit are taken in increasing index order; the first list found with the smallest count is
printed. Use the exact search when the number of non-zero-net accounts is ≤ 12
(`min_transfers_exact`), otherwise fall back to the sorted two-pointer greedy (largest surplus →
largest deficit), which is a **heuristic** (it returns 3 transfers on the verbatim example where 2
suffice). `IMPOSSIBLE` as in Part 1.

### Part 3 — audit a given list of transfers (follow-up 1, verbatim: "反过来问")
Apply the transfer lines in order (`from` loses `amount`, `to` gains it; overdraft allowed). Then
print every account as `NAME: balance` in input order, followed by one verdict line:
- `OK` — every account ≥ min;
- `INCOMPLETE` — some account < min although `sum ≥ min × n` (a full solution existed);
- `BEST_EFFORT` — `sum < min × n` (impossible) and **no account is above the minimum while another
  is below it** (all movable money was moved);
- `NOT_BEST_EFFORT` — impossible and some account still holds more than the minimum while another
  is short;
- `INVALID` — a transfer names an unknown account, has `amount ≤ 0`, or `from == to`; transfers up
  to (not including) the invalid one are applied, the rest are skipped.

### Part 4 — transfer fees (reconstructed)
`FEE f`: every transfer additionally deducts `f` from the **sender** (the receiver gets `amount`).
Greedy as in Part 2's fallback (largest surplus → largest deficit), where a source can send at most
`surplus − f` per transfer and is skipped once `surplus ≤ f`. Print the transfers, then a final line
`FEES: total`. If the greedy leaves a deficit uncovered print `IMPOSSIBLE` (exact when `f = 0`; a
heuristic verdict for `f > 0`, stated as such).

## Worked examples
```
PART 1                      Output (verbatim from the source)
AU: 80                      from: US, to: AU, amount: 20
US: 140                     from: US, to: FR, amount: 20
MX: 110                     from: MX, to: FR, amount: 10
SG: 120
FR: 70

PART 2  (same accounts)     Output (2 transfers; greedy would need 3)
                            from: US, to: FR, amount: 30
                            from: SG, to: AU, amount: 20

PART 3                      Output
AU: 80                      AU: 100
US: 140                     US: 100
MX: 110                     MX: 100
SG: 120                     SG: 120
FR: 70                      FR: 100
from: US, to: AU, amount: 20        OK
from: US, to: FR, amount: 20
from: MX, to: FR, amount: 10

PART 3                      Output
AU: 50                      AU: 70
US: 120                     US: 100
from: US, to: AU, amount: 20        BEST_EFFORT     (sum 170 < 200; nobody is above 100)
  (with amount: 10 instead)  AU: 60 / US: 110 / NOT_BEST_EFFORT

PART 4                      Output
FEE 5                       from: A, to: B, amount: 20      (A: 140 → 115)
A: 140                      from: A, to: C, amount: 5       (A: 115 → 105)
B: 80                       FEES: 10
C: 95
  (with A: 130)             IMPOSSIBLE   (A→B 20 leaves A at 105: 5 surplus = the fee, nothing sendable)
```

## Edge cases hidden tests are known to target
- feasibility is `sum ≥ min × n` — `==` is feasible (everyone ends exactly at min), one unit less is `IMPOSSIBLE`
- all accounts already ≥ min → no output (not `IMPOSSIBLE`, not an empty transfer line)
- negative balances; a single account; two accounts; deficits covered by several sources
- transfer amounts must never leave a source below the minimum (Parts 1/2/4) and must be > 0
- Part 2 count must be minimal: example needs 2 while the sorted greedy makes 3; equal surplus/deficit pairs
- Part 3 verdict boundaries: exactly at min is `OK`; `BEST_EFFORT` requires no account > min
- `MIN` other than 100; `- ` bullets and spaces around `:`/`,` in input
- 500 accounts (Part 1/2 fallback) must be fast; the exact search is only used for ≤ 12 non-zero accounts

## Variants seen in the wild
- LeetCode 7521596 (2026-01 VO): "Minimum Transactions for Multi-Party Debt Settlement" — nets sum
  to zero (pure LC 465); `min_transfers_exact` handles it (no surplus left over).
- programhelp 2026-02 VO: "current → target balances" (a per-account target instead of one minimum)
  — pass per-account minimums by giving `net` directly; audit ("dry run then compare with DB") = Part 3.
- joeytor/sahaia1 sort by balance and two-pointer richest → poorest (a different valid Part 1 order).
- Java version prints `amount: 20.0` (doubles); we use integer units.

## What this tests
skills: S02 parsing · S03 records keyed by id · S05 threshold semantics (≥ min, feasibility ==) · S08
deterministic ordering · S09 exact formatting · S17 ledger-style balances · S18 validation (audit) ·
S19 incremental design · A10 LC 465 DFS with pruning

## Sources
- https://github.com/joeytor/StripeInterview (`src/main/java/MoneyTransfer.java`, README → Virtual Onsite / Coding; verbatim statement, example, follow-ups 1–2)
- https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/money_transfer.py (Python port with the same header)
- https://leetcode.com/discuss/post/5647506/ (2024-08-16 phone screen; verbatim base problem)
- https://leetcode.com/discuss/post/7521596/ (2026-01-24 VO: minimum transactions for multi-party debt settlement)
- https://www.1point3acres.com/bbs/thread-1029620-1-1.html (Phone + Onsite: "Money Transfer" with optimization follow-ups)
- https://programhelp.net/en/vo/stripe-sde-interview-vo-5-round-interview-experience/ (2026-02-27 VO: settlement, min transactions DFS, audit)
- https://github.com/Hazeera65/stripe-interview (`round1/465optimalaccountBalancing/`)
