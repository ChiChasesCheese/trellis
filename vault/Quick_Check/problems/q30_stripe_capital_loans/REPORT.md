# q30 Stripe Capital — report

## Summary
Command-stream bookkeeping for Stripe Capital loans: create / pay / increase / withhold a
percentage of a processed transaction, then print each merchant's outstanding debt. Stripe asks
it because it is the Capital product reduced to a ledger: integer cents, balances that must never
go negative, truncation of withheld amounts, and graceful handling of invalid API calls.

## Sources & confidence
high — verbatim statement + 3 examples in joeytor/StripeInterview `StripeCapital.java` (phone
interview); sahaia1 Python port; 1point3acres 2020-08 "Stripe OA(Capital)"; Shivam5022 2025 OA
description of the same command-parsing shape. Conflict resolved: the prose Example 0 says
`PAY_LOAN: acct_foobar,loan,1000` (unknown id) but expects 4000 — the repo's own runner uses
`loan1`; treated as a typo, and the verbatim line is tested as a Part 4 no-op (→ 5000).
Duplicate `CREATE_LOAN`: Java replaces, Python adds — default is "ignore", both variants exposed
via `process(lines, duplicate_create=...)` and tested.

## Approach by part
1. `merchant -> {loan -> cents}`; `PAY_LOAN` = `max(0, bal - amt)`; print `id,total` for total > 0, sorted.
2. `TRANSACTION_PROCESSED` withholds `amount * pct // 100` (integer truncation) and repays like Part 1.
3. `INCREASE_LOAN` adds; totals sum all loans; loan ids scoped per merchant. Reconstructed
   variant: 3-parameter transaction (no loan id) repays oldest-first over the insertion-ordered dict.
4. Validation gate before every mutation: unknown merchant/loan, negative amount, pct ∉ [1,100],
   duplicate create, unknown method, too few params → no-op.

## Pitfalls hidden tests target
- overpayment must cap at 0 and **not** spill into other loans; fully repaid merchants disappear
- truncation (`433.64 → 433`, `99×1/100 → 0`), pct boundaries 0/1/100/101
- `m10 < m2`, `acct_barfoo < acct_foobar` (string order); `id,total` with no space and no `$`
- spaces after commas in parameters; unknown ids must not raise KeyError

## Complexity & measured cost
O(n + m log m) for n lines, m merchants. Measured: 0.12s, 34 MB (perf test: 6k creates + 100k actions).

## Test inventory
23 tests — part1: 5 · part2: 3 · part3: 5 · part4: 10 (incl. 2 io, 1 perf); edge 13 · fmt 1.

## Skills exercised
S02 parsing · S03 records keyed by id · S06 integer money/truncation · S08 sort · S09 format ·
S17 ledger balances · S18 validation · S19 incremental design · S24 domain literacy
