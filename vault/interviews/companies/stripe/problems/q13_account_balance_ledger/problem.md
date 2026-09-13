# q13 · Account Balance Ledger — balances, rejected debits, platform loans and MAX_RESERVE

**Type:** bespoke OA (Easy) · **Stage:** HackerRank OA (60 min, 3 parts); the same statement is recycled as an intern VO · **Last asked:** 2026-05-12 (1point3acres 题库 `account-balance-manager`)
**Frequency:** 6 independent sources (1point3acres 题库; linkjob 2025-12-07 "Transaction Balance Problem" intern VO; prachub "Build an Account Transfer Ledger" onsite May 2026; dev.to/programhelp `user event amount` logs; GitHub Shivam5022 OA "simulate transactions between users' bank accounts"; Glassdoor "parse the input API and get account balance information for a user") · **Confidence:** medium (rules consistent across sources; exact I/O shapes reconstructed)

## Context
Every money movement at Stripe is a balance transaction on a ledger: credits and debits per account,
processed strictly in order. A platform (Stripe Connect) may cover a connected account's shortfall out
of its own funds and recover it from the account's next incoming credits — the amount the platform has
lent out at any moment is the *reserve* it must hold. Parts: plain ledger → insufficient-funds
rejection → platform lending with peak-reserve reporting.

## Input (stdin)
First line `PART n`. Then one transaction per line, processed in input order. Blank lines and spaces
around commas are ignored. Amounts are decimal strings with up to two decimals (`12.34`, `7`, `0.5`),
non-negative; parse them to **integer cents** (never float). Up to 2·10^5 lines.
```
txn_id,user_id,credit,amount            add amount to user_id
txn_id,user_id,debit,amount             subtract amount from user_id
txn_id,from_user,transfer,to_user,amount   (Part 3) debit from_user, credit to_user
```
`txn_id` is an opaque unique string; `user_id` is a case-sensitive string. In Part 3 the account
`platform` is special (see rules). (The transfer line shape is reconstructed: sources only say
"transfers between accounts"; it mirrors the credit/debit line and keeps the id for the rejected list.)

## Output
1. one line per user whose **final balance is non-zero**: `user_id balance`, balance as `x.xx`
   (two decimals, `-` prefix when negative, e.g. `bob -3.50`), **sorted by user_id (plain string order)**;
2. Part 2–3: then `REJECTED: id1,id2,…` (rejected txn ids in input order, comma-separated, no spaces) or
   `REJECTED: NONE`;
3. Part 3: then `MAX_RESERVE: x.xx`.

## Rules
### Part 1 — final balances
Apply every line. Balances **may go negative** (a debit is never refused here). Print non-zero
balances sorted by user. An account that ends at exactly `0.00` is not printed (even if it had activity).

### Part 2 — reject overdrafts
A `debit` whose result would be `< 0` (i.e. `balance − amount < 0`, strict) is **rejected**: balance
unchanged, id appended to the rejected list. A debit that lands exactly on `0.00` is accepted. Credits are
never rejected. A debit on a never-seen user is rejected (balance 0). Balances are therefore never
negative in Part 2.

### Part 3 — transfers and the `platform` lender
- `transfer` = debit `from_user` then credit `to_user` (a rejected transfer changes nothing).
- The account named `platform` is the lender. When a **non-platform** account's debit/transfer would
  overdraw by `shortfall = amount − balance`, the platform **lends** exactly `shortfall` if
  `platform_balance ≥ shortfall`: platform balance −= shortfall, the user's loan += shortfall, the
  transaction proceeds and the user ends at `0.00`. If the platform cannot cover the shortfall the
  transaction is **rejected** (nothing changes, no partial loan). The platform itself never borrows: an
  overdrawing platform debit/transfer is rejected.
- **Automatic repayment:** whenever a user with an outstanding loan receives money (a `credit`, or the
  receiving side of a `transfer`), `repay = min(loan, incoming)` goes straight back to the platform:
  platform balance += repay, loan −= repay, and only `incoming − repay` lands in the user's balance.
  Credits to `platform` itself repay nothing.
- `MAX_RESERVE` = the **peak total outstanding loans** (sum over users) observed after any single step,
  i.e. the most the platform ever had lent out at once. `0.00` if nothing was borrowed.
- Printed balances are cash balances (loans are not subtracted; the platform's printed balance is its
  cash after lending/repayments). `platform` is printed like any user when non-zero.
- Sorting/format as Part 1; then `REJECTED:` line; then `MAX_RESERVE:` line.

## Worked examples
```
PART 1
t1,alice,credit,100.00
t2,bob,credit,50.50
t3,alice,debit,30.25
t4,bob,debit,50.50
t5,carol,debit,10.00
->
alice 69.75
carol -10.00            (bob is exactly 0.00 → omitted)
```
```
PART 2                  (same five lines)
->
alice 69.75
REJECTED: t5            (carol had 0; t4 lands exactly on 0.00 and is accepted)
```
```
PART 2
t1,a,credit,10.00
t2,a,debit,10.00
t3,a,debit,0.01
t4,a,credit,5.00
->
a 5.00
REJECTED: t3
```
```
PART 3
t1,platform,credit,100.00
t2,alice,credit,20.00
t3,alice,debit,50.00            alice short 30 → borrows 30 (platform 70, loans 30, alice 0)
t4,bob,credit,10.00
t5,bob,transfer,alice,25.00     bob short 15 → borrows 15 (platform 55, loans 45 ← peak); alice receives
                                25 → repays 25 (platform 80, alice loan 5, alice still 0)
t6,alice,credit,10.00           repays her last 5 (platform 85), alice 5.00
t7,carol,debit,200.00           platform 85 < 200 → rejected
t8,bob,debit,100.00             bob short 100, platform 85 < 100 → rejected
->
alice 5.00
platform 85.00
REJECTED: t7,t8
MAX_RESERVE: 45.00
```

## Edge cases hidden tests are known to target
- `0.00` accounts omitted (including a user whose credits and debits cancel); empty input → nothing
  (Part 2 still prints `REJECTED: NONE`, Part 3 also `MAX_RESERVE: 0.00`)
- debit exactly equal to balance accepted; one cent more rejected; debit on unknown user rejected
- amounts `7`, `0.5`, `12.3` → cents 700 / 50 / 1230; `0.10 + 0.20` must print `0.30` (no float)
- Part 1 negative formatting `-3.50` (not `-3.5`, not `-0.-50`); sort is string order (`B` < `a`,
  `user10` < `user2`)
- Part 3: loan exactly equal to the platform balance allowed (platform → 0); shortfall one cent above →
  rejected; repayment capped at the loan (excess lands in the user's balance); repayment happens on
  the receiving side of a transfer; peak reserve is measured *before* any repayment in the same
  transfer; the platform never borrows; rejected transfer leaves both sides untouched
- rejected ids in input order, comma-separated without spaces; `REJECTED: NONE` when empty

## Variants seen in the wild
- `user event amount` space-separated logs with `event ∈ {credit, debit}` and output "final balance per
  user" (dev.to / programhelp) — same Part 1 with a different delimiter.
- prachub "Build an Account Transfer Ledger" (onsite): transfers only, plus "reject when
  `current_balance + amount < 0`" and the `platform_id` borrowing part reporting `max_reserve`.
- linkjob intern VO: identical three parts, output as returned dict/list instead of stdout.
- "Money transfer / rebalance to ≥ 100" (github joeytor, adonais0) is a different problem (q-later).

## What this tests
skills: S02 CSV parsing with a variable-length line · S03 per-account records + loan map · S05 strict
vs non-strict overdraft test · S06 integer cents from decimal strings, exact formatting · S08 sorted
output with stated order · S09 exact `REJECTED:` / `MAX_RESERVE:` formats · S10 ordered event stream ·
S17 ledger-style balance tracking · S19 incremental design

## Sources
- 1point3acres 题库 `account-balance-manager` (OA, Easy, last asked 2026-05-12)
- https://www.linkjob.ai/interview-questions/stripe-interview-questions/ (2025-12-07 "Transaction Balance Problem", intern VO, 3 parts)
- prachub 「Build an Account Transfer Ledger」 (onsite May 2026; `platform_id`, `max_reserve`)
- dev.to / programhelp 「transaction logs `user event amount` → final balance」
- GitHub Shivam5022 interview experience (OA: "parse a command string and execute commands simulating transactions between users' bank accounts")
- https://docs.stripe.com/payments/balances ; https://docs.stripe.com/reports/balance-transaction-types (ledger vocabulary)
