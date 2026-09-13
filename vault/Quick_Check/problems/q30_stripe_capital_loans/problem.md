# q30 · Stripe Capital — loan bookkeeping (CREATE / PAY / INCREASE / TRANSACTION_PROCESSED)

**Type:** phone screen / old OA (2020–2022) · **Stage:** phone interview (joeytor README) and HackerRank OA
(1point3acres 2020-08 "Stripe OA(Capital)") · **Last asked:** 2022 (repo commits); 2025 Shivam5022 describes
the same "parse a command string and execute commands" OA · **Frequency:** 4 independent sources
(joeytor Java header, sahaia1 Python, 1point3acres thread-662909, Shivam5022) · **Confidence:** high

## Context
Stripe Capital lends merchants funds and, instead of interest, charges a fixed fee on top of the
principal; the merchant repays by having a percentage of every future sale withheld until the
outstanding amount is zero. You are writing the bookkeeping system: a merchant can create a loan,
pay it down manually, increase it, and process sales transactions from which a percentage is
withheld toward a specific loan. At the end you print each merchant's total outstanding debt.

## Input (stdin)
One API action per line: `METHOD: p1,p2,...` — the method name, a colon and a space, then
comma-separated parameters (optional spaces after the commas are tolerated, e.g.
`CREATE_LOAN: merchant1, loan1, 1000`). Blank lines are ignored. All amounts are **integer U.S.
cents**. Lines are processed in input order; there is **no `PART n` header** — the rules of all
parts accumulate in one program. Up to 10^5 lines.

| Method | Parameters | Meaning |
|---|---|---|
| `CREATE_LOAN` | merchant_id, loan_id, amount (≥ 0) | merchant initiates a loan |
| `PAY_LOAN` | merchant_id, loan_id, amount (≥ 0) | one-time manual repayment |
| `INCREASE_LOAN` | merchant_id, loan_id, amount (≥ 0) | increase an existing loan |
| `TRANSACTION_PROCESSED` | merchant_id, loan_id, amount (≥ 0), repayment_percentage (1..100) | a sale; `amount × pct / 100` is withheld toward the loan |

## Output
After all lines: one line per merchant with a **non-zero** outstanding balance, formatted
`merchant_id,total_outstanding` (no space after the comma), **lexicographically sorted by
merchant_id** (plain string order). Merchants whose loans are all fully repaid (or who never had a
positive balance) are skipped. Empty output if nobody owes anything.

## Rules
### Part 1 — create and pay
`CREATE_LOAN` opens a loan with the given balance. `PAY_LOAN` subtracts the amount from that
loan's balance; **a balance never goes negative — overpayment is capped at 0 and the remainder is
ignored** (not carried to other loans). Print `merchant,total` for merchants with total > 0.

### Part 2 — repayment from processed transactions
`TRANSACTION_PROCESSED: m, loan, amount, pct` withholds `floor(amount × pct / 100)` cents
(**truncate**, e.g. 433.64 → 433) and pays it toward `loan` exactly like `PAY_LOAN` (capped at 0).

### Part 3 — increase and multiple loans
`INCREASE_LOAN` adds the amount to an existing loan. A merchant may hold several loans (loan ids
are unique **per merchant** — `loan1` of two merchants are different loans); the printed number is
the **sum** of all that merchant's loan balances. Several merchants → sort output by merchant id.
*(reconstructed variant, exposed as the same command with 3 parameters)*: a
`TRANSACTION_PROCESSED: m, amount, pct` line **without a loan id** applies the withheld amount to
the merchant's loans **oldest-first** (creation order), spilling over to the next loan when one is
paid off; anything left after all loans are at 0 is ignored.

### Part 4 — invalid actions (source: "handle invalid API actions appropriately")
Every invalid line is a **no-op** (silently ignored, nothing printed to stdout):
`PAY_LOAN` / `INCREASE_LOAN` / `TRANSACTION_PROCESSED` on an unknown merchant or unknown loan;
negative amounts; `repayment_percentage` outside 1..100; a `CREATE_LOAN` whose (merchant, loan)
already exists (the original loan is kept — see Variants); an unknown method name. A
`CREATE_LOAN` with amount 0 is valid but contributes nothing, so the merchant is not printed
unless the loan is later increased.

## Worked examples
```
Example 0 (manual repayment)                   Output
CREATE_LOAN: acct_foobar,loan1,5000            acct_foobar,4000
PAY_LOAN: acct_foobar,loan1,1000

Example 1 (transaction repayment)              Output
CREATE_LOAN: acct_foobar,loan1,5000            acct_foobar,9945
CREATE_LOAN: acct_foobar,loan2,5000            (loan1: 5000 − 500·10/100 = 4950;
TRANSACTION_PROCESSED: acct_foobar,loan1,500,10   loan2: 5000 − 500·1/100 = 4995)
TRANSACTION_PROCESSED: acct_foobar,loan2,500,1

Example 2 (multiple actions)                   Output
CREATE_LOAN: acct_foobar,loan1,1000            acct_barfoo,2000
CREATE_LOAN: acct_foobar,loan2,2000            acct_foobar,3999
CREATE_LOAN: acct_barfoo,loan1,3000            (foobar: loan1 1000−1 = 999, loan2 2000+1000;
TRANSACTION_PROCESSED: acct_foobar,loan1,100,1    barfoo: 3000−1000)
PAY_LOAN: acct_barfoo,loan1,1000
INCREASE_LOAN: acct_foobar,loan2,1000

Example 3 (invalid actions, Part 4)            Output
CREATE_LOAN: m1,l1,100                         m1,100
PAY_LOAN: m1,l9,50          <- unknown loan: ignored
PAY_LOAN: m2,l1,50          <- unknown merchant: ignored
TRANSACTION_PROCESSED: m1,l1,1000,0   <- pct 0 invalid: ignored
CREATE_LOAN: m1,l1,999      <- duplicate create: ignored
CREATE_LOAN: m3,l1,40
PAY_LOAN: m3,l1,45          <- overpay: capped at 0, m3 not printed
```
Note: the source's Example 0 literally reads `PAY_LOAN: acct_foobar,loan,1000` (loan id `loan`)
yet expects `4000`; the same repo's runnable code uses `loan1`. We treat `loan` as a typo in the
prose — paying an unknown loan is a no-op (Part 4), so the verbatim line would print `5000`.

## Edge cases hidden tests are known to target
- overpayment: `PAY_LOAN` larger than the balance → 0, remainder **not** applied to other loans
- truncation of the withheld amount (`433.64 → 433`; `500 × 1 / 100 = 5`; `99 × 1 / 100 = 0`)
- a merchant whose loans are all repaid must **not** be printed; a merchant with two loans prints one summed line
- loan ids are per merchant (`m1/loan1` and `m2/loan1` are independent)
- pay / increase / transaction on an unknown merchant or loan → ignored, not crash
- lexicographic order: `acct_barfoo` < `acct_foobar`; `m10` < `m2`
- output format is `id,amount` with no space; amounts are plain integers (cents), never `$x.xx`
- spaces after commas in parameters (`merchant1, loan1, 1000`) must be stripped
- 10^5 lines and balances up to 10^12 — integers only

## Variants seen in the wild
- **Duplicate `CREATE_LOAN`**: joeytor's Java replaces the balance, sahaia1's Python adds to it. We
  ignore the duplicate by default; `process(lines, duplicate_create="replace")` /
  `"add"` switch the behaviour (tested).
- **Loan-less transaction (oldest-first)** — Part 3 variant above, reconstructed from the prose
  "some percentage of the merchant's future sales goes towards repayment".
- Shivam5022 (2025 OA): the same command-parsing shape but "transactions between users' bank
  accounts" — see q13 / q32.
- sahaia1 prints `merchant: total` (colon-space); the verbatim examples use `merchant,total`.

## What this tests
skills: S02 parsing · S03 domain records keyed by id · S06 integer money (truncation) · S08
deterministic sort · S09 exact formatting · S17 ledger-style balances never negative · S18
validation / invalid actions · S19 incremental design · S24 domain literacy (Capital)

## Sources
- https://github.com/joeytor/StripeInterview (`src/main/java/StripeCapital.java`, README → Phone Interview; verbatim statement + 3 examples)
- https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/capital.py (Python variant)
- https://github.com/Shivam5022/Interview-Experiences (2025 OA: "parse a command string and execute commands simulating transactions")
- 1point3acres thread-662909「热乎 Stripe OA(Capital)」(2020-08, content not visible)
