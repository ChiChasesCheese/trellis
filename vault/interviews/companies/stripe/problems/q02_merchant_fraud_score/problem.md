# q02 · Merchant Fraud Score — base score × amount factor, repeat-customer bonus, hourly-density penalty

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, one problem, rules unlocked progressively) · **Last asked:** 2026-07-06 (csoahelp write-up); Fall-2025 NG cycle (programhelp)
**Frequency:** 6 independent sources (csoahelp 2026-07, oavoservice 2026-01, programhelp ×3 (2025-10 / 2025-12 / 2026-01), medium @program.net 2025-12; 1024bbs/1point3acres mentions) · **Confidence:** high

## Context
Stripe Radar assigns every merchant a risk score. In this exercise every merchant starts with a
`base_score`, and a list of transactions — each paired **1:1 with a scoring rule** — moves the
score. Three rules exist: a large-amount multiplier, a repeat-customer bonus (a customer who
keeps coming back to the same merchant is a card-testing signal), and an hourly-density rule
(three or more purchases by the same customer at the same merchant within one hour is either
penalised or rewarded depending on the time of day). Rules are applied as **three separate
passes over the whole transaction list**, not interleaved per transaction. The #1 reported
failure is double-counting the group rules or using `>=` where the statement says `>`.

## Input (stdin)
First line `PART n` (n ∈ 1..3, optional — default 3, because the parts accumulate). Then three
sections introduced by header lines `MERCHANTS`, `TRANSACTIONS`, `RULES`; blank lines ignored,
optional spaces around commas tolerated. *(Section protocol reconstructed: the OA passes the three
lists as function parameters `merchants_list`, `transactions_list`, `rules_list`.)*

```
MERCHANTS
merchant_id,base_score              base_score integer 1–50
TRANSACTIONS
merchant_id,amount,customer_id,hour amount integer minor units (cents); hour 0–23
RULES
min_amount,multiplicative_factor,additive_factor,penalty   one rule per transaction, same order
```
n merchants, m transactions, m rules, n, m ≤ 1000 (no overflow concerns — use ints anyway).
The i-th rule belongs to the i-th transaction. All scores/factors are integers.

## Output
One line per merchant, **every merchant including those with no transactions**, sorted by
`merchant_id` in plain string order, formatted `merchant_id, score` (comma + one space).

## Rules
Scores start at `base_score`. Each pass walks **all** transactions in input order and updates the
transaction's merchant. Pass k runs only after pass k-1 has finished for every transaction.

### Part 1 — amount rule (pass 1)
If `amount > min_amount` (**strictly greater**) → `score *= multiplicative_factor`.
Equal amount does nothing. Zero or negative amounts are ordinary amounts (they never exceed a
non-negative threshold).

### Part 2 — repeat-customer rule (pass 2)
Count transactions per `(merchant_id, customer_id)` cumulatively in input order, **including the
current one**. When the running count is `>= 3` (i.e. the 3rd, 4th, … transaction of that pair)
→ `score += additive_factor` of *that* transaction's rule. The first two transactions of a pair
never add. Pairs are independent: the same customer at two merchants has two separate counters.

### Part 3 — hourly-density rule (pass 3)
Count transactions per `(merchant_id, customer_id, hour)` cumulatively; for the **3rd and every
later** occurrence in the same hour:
- `12 <= hour <= 17` → `score += penalty`
- `9 <= hour <= 11` or `18 <= hour <= 21` → `score -= penalty`
- any other hour (0–8, 22–23) → nothing.
Scores may go negative; print them as-is.

## Worked examples
Example 1 (Part 1 — strict `>`):
```
PART 1
MERCHANTS
m2,20
m1,10
TRANSACTIONS
m1,500,c1,13
m2,100,c2,10
RULES
100,2,5,3
100,3,1,1
```
→ `m1, 20` (500 > 100 → 10×2) and `m2, 20` (100 > 100 is false → unchanged). Output order m1, m2.

Example 2 (Part 2 — 3rd and later transactions of the pair add):
```
PART 2
MERCHANTS
shop,10
TRANSACTIONS
shop,50,alice,9
shop,50,alice,9
shop,50,alice,9
shop,50,alice,9
shop,50,bob,9
RULES
100,2,5,1
100,2,5,1
100,2,5,1
100,2,7,1
100,2,9,1
```
→ `shop, 22` (no amount exceeds 100; alice's 3rd adds 5, 4th adds 7; bob only once → nothing).

Example 3 (Part 3 — all three passes, with the hour bands):
```
PART 3
MERCHANTS
m1,5
m0,50
TRANSACTIONS
m1,1000,c1,13
m1,10,c1,13
m1,10,c1,13
m1,10,c1,10
m1,10,c1,10
m1,10,c1,10
RULES
500,3,1,4
500,3,1,4
500,3,1,4
500,3,1,4
500,3,1,4
500,3,1,4
```
pass 1: only txn 1 has 1000 > 500 → m1 = 15. pass 2: c1@m1 is 3rd..6th on txns 3–6 → +1 ×4 → 19.
pass 3: hour 13 has 3 txns → the 3rd one adds 4 → 23; hour 10 has 3 txns → the 3rd one
subtracts 4 → 19. Output: `m0, 50` then `m1, 19` (m0 has no transactions, still printed).

Example 4 (Part 3, programhelp-2026-01 style parameters — factor 2, bonus 1, penalty 5):
```
MERCHANTS
M1,10
M2,20
TRANSACTIONS
M1,30000,C1,14
M1,5000,C1,14
M1,5000,C1,14
M2,20000,C2,20
M2,20000,C3,20
M2,20000,C2,20
RULES
10000,2,1,5
10000,2,1,5
10000,2,1,5
10000,2,1,5
10000,2,1,5
10000,2,1,5
```
M1: pass1 30000>10000 → 20; pass2 3rd C1 → 21; pass3 hour 14 third → +5 → 26.
M2: pass1 three txns each >10000 → 20×2×2×2 = 160; pass2 C2 only twice → nothing; pass3 (M2,C2,20)
only twice → nothing → `M1, 26`, `M2, 160`.

## Edge cases hidden tests are known to target
- `amount == min_amount` must **not** multiply (strict `>`); amount 0 / negative never triggers
- merchants with no transactions are still printed with their base score
- duplicate identical transaction lines are separate transactions and count towards both group
  counters (a 3× duplicated line triggers both the repeat and the hourly rules)
- rule 2 counts the current transaction: the 3rd transaction adds, the 2nd does not
- the additive factor is the one belonging to the *current* transaction, not the first one
- hour band boundaries: 11 → subtract, 12 → add, 17 → add, 18 → subtract, 21 → subtract, 22 → nothing, 8 → nothing, 9 → subtract
- pass ordering: multipliers are applied to `base_score` only (before any additive terms) even if
  the multiplying transaction comes last in the list
- multiplicative_factor 0 or 1; additive factor 0; negative scores are printed with the minus sign
- output sort is plain string order (`m10` < `m2`), format `id, score` with exactly one space

## Variants seen in the wild
- **oavoservice group interpretation of rule 2** ("add *all* the corresponding rules' additive
  factors, process as a group"): if a `(merchant, customer)` pair has ≥ 3 transactions in total,
  add the additive factors of **every** transaction in the pair (including the first two), once.
  Supported as `score(..., repeat_mode="group")` and tested.
- **programhelp 2025-10 NG variant** (`score_variant_grouped`): no rule list. Group by
  `(merchant, customer)`; if the group has ≥ 3 transactions add the group's total amount to the
  merchant score. Then group by `(merchant, customer, hour)`; if ≥ 3, add that group's total
  amount again. Output identical. ~17 tests; edges: 0/negative amount, no-transaction merchants,
  duplicates, formatting, "floating point precision" (use integer cents).
- **medium @program.net simplified variant**: every transaction adds `amount × factor`; +1 bonus
  per transaction; if a merchant has more than `hour_threshold` transactions in the same hour,
  subtract `hour_penalty`. Not implemented (single low-confidence source).
- Output separator without the space (`merchant,score`) in some retellings — one-character change.

## What this tests
skills: S02 parsing · S03 records keyed by id · S04 grouping / once-per-group rules · S05 strict
thresholds · S06 integer money · S08 deterministic sort · S09 exact formatting · S12 hour buckets ·
S19 incremental design (three passes as three functions)

## Sources
- csoahelp.com 2026-07-06 「Stripe OA真题：Merchant Fraud Score」 (fullest statement; primary)
- https://oavoservice.com/en/articles/stripe-2025-hackerrank-oa-merchant-fraud-scoring-system-oavoservice (2026-01-03)
- https://programhelp.net/en/oa/stripe-2026-new-grad-oa-overview/ (2025-10-26, grouped NG variant, ~17 tests)
- https://programhelp.net/en/oa/stripe-oa-questions-software-engineer/ (2025-12-28)
- programhelp.net 2026-01-20 「HackerRank OA 真题解析」 (example parameters factor 2 / bonus 1 / threshold 3 / penalty 5)
- https://medium.com/@program.net/in-depth-breakdown-of-stripe-software-engineer-oa-333c7db9e033 (simplified variant)
- 1024bbs / 1point3acres summaries mentioning "merchant / customer / 3 次"

## Clarifications (from adversarial review, 2026-08-26)
- Transactions whose merchant is not declared in the merchants block are silently dropped (they never create a merchant).
