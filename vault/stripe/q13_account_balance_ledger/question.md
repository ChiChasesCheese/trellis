# q13 · Account Balance Ledger — balances, rejected debits, platform loans and MAX_RESERVE

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
| 格式 | 说明 |
|---|---|
| `txn_id,user_id,credit,amount` | add amount to user_id |
| `txn_id,user_id,debit,amount` | subtract amount from user_id |
| `txn_id,from_user,transfer,to_user,amount` | (Part 3) debit from_user, credit to_user |
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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]]
- [[s17-ledger-balance-tracking|S17 台账式余额跟踪]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
