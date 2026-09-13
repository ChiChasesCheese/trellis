# q20 · Transaction Fees, Receivables and Reconciliation — fees per CSV row, rate table, payout aggregation, system-vs-gateway diff

## Context
Stripe charges a merchant a processing fee per event: a percentage plus a fixed amount on a
completed payment (the public "2.9% + 30¢" shape), a flat dispute fee when a chargeback is lost,
and — on some rails — even when it is won. Fees vary by payment provider and buyer country, so
a rate table overrides the default. Receivables are then rolled up per merchant, card type and
payout date (the "Brazil" question), and finally the processor's ledger is reconciled against
the payment gateway's ledger to find missing and mismatched transactions.

## Input (stdin)
```
PART 1                                     PART 2
id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
py_1,1,1000,eur,2025-01-01,acct_1,ie,payment,card,payment_completed        RATES
...                                        card,ie,140,25            (provider,country,rate_bps,fixed_cents)
                                           klarna,*,290,0            (* = any)
                                           TRANSACTIONS
                                           <same CSV as Part 1, with header>
PART 3                                     PART 4
customer_id,merchant_id,payout_date,card_type,amount[,status,payment_provider,buyer_country]
c1,m1,2024-10-01,visa,1000                 SYSTEM
...                                        txn_1,1000
                                           GATEWAY
                                           txn_1,1000
```
CSV rows have a **header**; columns are looked up **by name** (any column order; extra columns
ignored). `amount` is an integer in the smallest currency unit (cents); a decimal such as
`10.00` is also accepted and converted exactly to cents (`Decimal`). Whitespace around fields
and blank lines are ignored. Up to 10^5 rows (Part 3: 2×10^5 for Part 4).

## Output
* Part 1 / 2: one line per transaction row, in input order: `<id>,<fee_cents>`.
* Part 3: header `merchant_id,card_type,payout_date,net` then one line per group
  `merchant_id,card_type,payout_date,net` sorted by `merchant_id`, then `card_type`, then
  `payout_date` (plain string order). The header is printed even when there are no rows.
* Part 4: one line per discrepancy, sorted by transaction id: `MISSING_IN_GATEWAY <id>`,
  `MISSING_IN_SYSTEM <id>`, `AMOUNT_MISMATCH <id> <system_amount> <gateway_amount>`. Nothing
  for matching ids (unless `include_matches=True`, which adds `MATCH <id>` lines).
All amounts print as integer cents (no `$`, no decimals).

## Rules
### Part 1 — fee per row by status  `fee_cents(row: dict) -> int`
| `status` | fee (cents) |
|---|---|
| `payment_completed` | `amount × 2.1 %` rounded **half-up to the cent**, `+ 30` |
| `dispute_lost` | `1500` |
| `dispute_won` | `1500` if `payment_provider == "card"` else `0` |
| anything else (`payment_pending`, `payment_failed`, `refund_completed`, …) | `0` |

Integer implementation of the percentage: `pct = (amount_cents × 21 + 500) // 1000`, i.e.
2.1 % = 21 / 1000 and adding 500 before the floor division rounds half-up. Hand checks:
1000 → 21 + 30 = **51**; 1234 → 25.914 → 26 + 30 = **56**; 500 → 10.5 → **11** + 30 = **41**
(banker's rounding would wrongly give 40); 99 → 2.079 → 2 + 30 = **32**; 0 → **30**.
Comparisons of `status` and `payment_provider` are exact (case-sensitive) after stripping.

### Part 2 — provider/country rate table  `fee_cents(row, rates)`
`rates` maps `(provider, country) → (rate_bps, fixed_cents)`. For `payment_completed` rows
only, if the row matches an entry the fee is `amount_cents × rate_bps // 10000 + fixed_cents`
(**floor**, as the PracHub spec states; note the different rounding from Part 1's default).
Match precedence: exact `(provider, country)` → `(provider, "*")` → `("*", country)` →
`("*", "*")` → no match → Part 1 default. Dispute rows ignore the table.

### Part 3 — receivables  `receivables(rows, rates=None) -> list[str]`
Group rows by `(merchant_id, card_type, payout_date)` and sum `net = amount − fee`, where `fee`
is Part 1/2's `fee_cents(row)` when the row has a `status` column and **0 when it has none**
(the original csoahelp question has no status: it is a pure sum of `amount`). Every row
contributes (reconstructed — statuses only change the fee). Groups with net 0 or negative are
still printed.

### Part 4 — reconciliation  `reconcile(system, gateway, include_matches=False) -> list[str]`
Each list holds `id,amount` lines. Duplicate ids inside one list are **summed** (a gateway may
report a payment as several captures — reconstructed). Then, per id in sorted order:
present only in `system` → `MISSING_IN_GATEWAY id`; only in `gateway` → `MISSING_IN_SYSTEM id`;
in both with different totals → `AMOUNT_MISMATCH id <system> <gateway>`; equal → nothing
(or `MATCH id` with `include_matches=True`).

## Worked examples
```
PART 1
id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
py_1,1,1000,eur,2025-01-01,acct_1,ie,payment,card,payment_completed      -> py_1,51
py_2,2,500,eur,2025-01-01,acct_1,ie,payment,klarna,payment_completed     -> py_2,41
py_3,3,1000,eur,2025-01-02,acct_1,ie,payment,card,payment_pending        -> py_3,0
dp_1,4,1000,eur,2025-01-03,acct_1,ie,dispute,card,dispute_lost           -> dp_1,1500
dp_2,5,1000,eur,2025-01-03,acct_2,de,dispute,card,dispute_won            -> dp_2,1500
dp_3,6,1000,eur,2025-01-03,acct_2,de,dispute,klarna,dispute_won          -> dp_3,0
rf_1,7,1000,eur,2025-01-04,acct_2,de,refund,card,refund_completed        -> rf_1,0
```
```
PART 2  RATES: card,ie,140,25 / klarna,*,290,0   + the rows above
  py_1 (card, ie)     -> 1000*140//10000 + 25 = 14 + 25 = 39
  py_2 (klarna, ie)   -> 500*290//10000 + 0  = 14   (14.5 floored)
  py_3 pending        -> 0 ; dp_1 -> 1500 ; dp_2 -> 1500 ; dp_3 -> 0 ; rf_1 -> 0
  a card/de completed row of 1234 has no entry -> default 56
```
```
PART 3 (csoahelp shape, no status column)
customer_id,merchant_id,payout_date,card_type,amount
c1,m1,2024-10-01,visa,1000
c2,m1,2024-10-01,visa,500
c3,m1,2024-10-01,master,200
c4,m2,2024-09-30,visa,700
->
merchant_id,card_type,payout_date,net
m1,master,2024-10-01,200
m1,visa,2024-10-01,1500
m2,visa,2024-09-30,700
With a status column (c1 payment_completed/card, c2 dispute_lost/card, c3 & c4 payment_completed/card):
m1,master,2024-10-01,166   (200 - 34)      m1,visa,2024-10-01,-51   (1000-51 + 500-1500)
m2,visa,2024-09-30,655     (700 - 45)
```
```
PART 4
SYSTEM: txn_1,1000 / txn_2,2000 / txn_4,300      GATEWAY: txn_1,1000 / txn_3,500 / txn_4,350
->
MISSING_IN_GATEWAY txn_2
MISSING_IN_SYSTEM txn_3
AMOUNT_MISMATCH txn_4 300 350
```

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s07-tiered-metered-proration|S07 阶梯 / 计量 / 按比例分摊]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s21-python-stdlib-fluency|S21 语言熟练度与标准库]]
- [[s24-payments-domain-vocab|S24 领域词汇（支付）]]
