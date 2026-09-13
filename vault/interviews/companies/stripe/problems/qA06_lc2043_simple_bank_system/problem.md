# qA06 · LC 2043 Simple Bank System — validated transfer/deposit/withdraw, transaction log + reversal, platform lending

**Type:** LeetCode "Stripe" tag (design / simulation) · **Stage:** phone screen / onsite coding · **Last asked:** tag snapshot 2026-07-12 (>6-month bucket)
**Frequency:** tag freq 61.2 (liquidslr All), 67.1 (liquidslr >6mo), 62.5 / 62.5 (snehasishroy 2026-07) · 3 tag mirrors · **Confidence:** high (tag); the reversal / lending follow-ups mirror q13 and q27 (PaymentLedger, programhelp VO ×4)

LC 2043 · *Simple Bank System* · Medium · https://leetcode.com/problems/simple-bank-system

## The problem (restated)
Build a class `Bank` initialised with `balance`, a list where `balance[i]` is the money in account
`i+1` (accounts are **1-indexed**). Three operations, each returning whether it was **valid** and
applying its effect only when valid:
* `transfer(a, b, money)` — valid iff both accounts exist and account `a` holds at least `money`;
  moves `money` from `a` to `b`.
* `deposit(a, money)` — valid iff the account exists; adds `money`.
* `withdraw(a, money)` — valid iff the account exists and holds at least `money`; subtracts it.
An invalid operation changes nothing. LC limits: `n ≤ 10^5` accounts, balances and amounts up to
`10^12`, up to `10^4` calls.

## Context
This is the skeleton of every Stripe ledger problem: q13's account balance ledger (reject overdrafts,
platform lends the shortfall), q27's PaymentLedger (programhelp VO ×4: idempotent add / refund), q32's
money transfers. The interviewer wants validation before mutation, no partial effects on failure, and
then pushes into "undo a transaction" (refunds / reversals) and "who covers a shortfall" (platform
lending, exactly q13 Part 3).

## Input (stdin)
```
PART n                        # 1..3
b1 b2 ... bn                  # initial balances (account i has balance b_i)
RESERVE r                     # Part 3 only: platform lending reserve
deposit a money               # commands, one per line
withdraw a money
transfer a b money
reverse txn_id                # Part 2+
```

## Output
One line per command: `true` or `false`. Then `balances b1 b2 ... bn`. Part 3 adds
`reserve r`, `debts d1 d2 ... dn` and `max_outstanding m`.

## Rules
### Part 1 — LC signature  `Bank(balance)`, `.transfer/.deposit/.withdraw -> bool`, `.balances() -> list[int]`
As restated above. Validate both accounts of a transfer **before** touching either; `a == b` transfers
are valid when funded (net zero). Amounts are non-negative integers (money in minor units).

### Part 2 — transaction log and reversal  `.log: list[TxnRecord]`, `.reverse(txn_id) -> bool`
Every call (valid or not, including `reverse` itself) appends `TxnRecord(id, kind, src, dst, amount,
ok, ref)` with ids `1, 2, 3, …` in call order; `kind ∈ {deposit, withdraw, transfer, reverse}`; `ref` is
the reversed id for `reverse` records, else `None`. `reverse(txn_id)` succeeds iff the record exists,
was `ok`, is not itself a `reverse`, and has not been reversed yet — **and** the undo is fundable: a
deposit reversal debits the account (needs the funds); a withdraw reversal credits it; a transfer
reversal moves the money back (`dst` needs the funds). Reversals never borrow (Part 3). A successful
reversal marks the original as reversed (`.reversed_ids`), so a second reversal returns `false`.

### Part 3 — overdraft with platform lending (q13 link)  `Bank(balance, reserve=0)`
When `withdraw`/`transfer` would overdraw account `a` by `shortfall = money − balance[a] > 0`, the
platform **lends exactly `shortfall`** if `reserve ≥ shortfall`: `reserve −= shortfall`,
`debt[a] += shortfall`, the operation proceeds and `a` ends at `0`. If the reserve cannot cover it,
the operation is rejected (nothing changes). **Automatic repayment:** whenever an account with debt
receives money (deposit or the receiving side of a transfer / reversal), `repay = min(debt, incoming)`
goes back to the reserve first and only `incoming − repay` lands in the balance.
`.max_outstanding` = the peak of `sum(debt)` observed after any step. With `reserve=0` Part 3 is
exactly Part 1.

## Worked examples
```
LC ex   Bank([10, 100, 20, 50, 30])
        withdraw(3, 10) -> true   (acct 3: 20 -> 10)
        transfer(5, 1, 20) -> true (5: 30 -> 10 ; 1: 10 -> 30)
        deposit(5, 20) -> true    (5: 30)
        transfer(3, 4, 15) -> false (acct 3 has 10)
        withdraw(10, 50) -> false  (no account 10)
        balances -> [30, 100, 10, 50, 30]
Part 2  after the LC sequence: log ids 1..5 with ok = [T, T, T, F, F]
        reverse(2) -> true  (1: 30 -> 10 ; 5: 30 -> 50) ; reverse(2) -> false (already reversed)
        reverse(4) -> false (was not ok) ; reverse(6) -> false (id 6 is the reverse record itself)
        reverse(1) -> true  (3: 10 -> 20) ; reverse(99) -> false
        balances -> [10, 100, 20, 50, 50] ; log has 11 records (failed reversals are logged too)
        Bank([5]); deposit(1, 5) -> true ; withdraw(1, 8) -> true (2 left) ; reverse(1) -> false (needs 5, has 2)
Part 3  Bank([10, 100], reserve=50)
        withdraw(1, 30) -> true  (shortfall 20: reserve 30, debt1 20, bal1 0)
        withdraw(1, 40) -> false (shortfall 40 > reserve 30)
        deposit(1, 25) -> true   (repay 20: reserve 50, debt1 0, bal1 5)
        transfer(1, 2, 15) -> true (shortfall 10: reserve 40, debt1 10, bal1 0, bal2 115)
        balances [0, 115] ; reserve 40 ; debts [10, 0] ; max_outstanding 20
```
stdin for the LC example:
```
PART 1
10 100 20 50 30
withdraw 3 10
transfer 5 1 20
deposit 5 20
transfer 3 4 15
withdraw 10 50
```
→ `true true true false false` (one per line) then `balances 30 100 10 50 30`.

## Edge cases hidden tests are known to target
- account 0 and account n+1 are invalid (1-indexed); negative account ids
- `withdraw` of exactly the balance is valid (== ok, one more is not); amount 0 is valid
- transfer to an invalid destination must not debit the source; `a == b` transfer
- Python ints: 10^12 balances plus 10^4 deposits of 10^12 (no overflow, no floats)
- Part 2: reversing a failed / already-reversed / reverse record; reversal that is not fundable
- Part 3: shortfall exactly equal to the reserve is allowed; repayment caps at the debt; the
  platform never lends to cover a reversal

## Variants seen in the wild
- q13 Account Balance Ledger (string commands, `platform` account as lender, MAX_RESERVE).
- q27 Payment Ledger (idempotency keys on add_payment / refund) and q10 PaymentIntent state machine.
- LC 2043 with `deposit` returning the new balance instead of a bool.

## Why Stripe asks it
Validate-then-mutate with no partial effects is the core discipline of a ledger; the follow-ups are
literally refunds and Stripe Capital-style advances.

## Stripe-flavored follow-ups
1. Transaction log + reversal (refunds) — Part 2.
2. Platform lending on overdraft with automatic repayment — Part 3 (q13).
3. Idempotency keys on every call (q27) — not implemented here.

## What this tests
skills: A08 design/simulation with validation · S03 state per account · S10 reversals · S17 ledger balances · S18 validation · S19 incremental design

## Sources
- https://leetcode.com/problems/simple-bank-system
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (61.2)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (67.1)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (62.5)
- https://programhelp.net/en/vo/stripe-vo-interview-questions-and-solutions/ (PaymentLedger family, 2026-01..04) — follow-up framing
- catalog/raw/github_repos.md §30
