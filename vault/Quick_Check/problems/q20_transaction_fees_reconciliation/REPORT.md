# q20 Transaction Fees / Receivables / Reconciliation — report

## Summary
The "money pipeline" phone screen: per-event processing fees from a CSV (percentage + fixed on
completed payments, flat dispute fees, provider-dependent won-dispute fee), a provider/country
rate table override, payout-level receivables grouped by (merchant, card type, payout date), and
a system-vs-gateway reconciliation report. It is the fee schedule of Stripe's pricing page and
the daily job of the Payments/Financial-Reporting teams reduced to CSV arithmetic; it drills
integer-cent money, two different rounding modes, header-driven CSV parsing and set diffs.

## Sources & confidence
medium — 1point3acres 1150184 (phone, 2025-10), programhelp VO 2025-12-04 / 2026-01-08 (the 2.1 %
+ $0.30 / $15 dispute rules), PracHub ×2 (floor `amount*bps//10000` rule, provider+country
rates), Glassdoor/linkjob CSV column list, csoahelp receivables 2024-10/11 ("Brazil group by"),
1point3acres 1093626, 1point3acres 41eadf8b + OJ "Payment Reconciliation", InterviewDB.

## Approach by part
1. `parse_csv` → `csv.DictReader` with stripped keys/values (column order free); `fee_cents(row)`
   dispatches on `status`: completed → `(amount*21 + 500)//1000 + 30` (2.1 % half-up + 30¢),
   `dispute_lost` → 1500, `dispute_won` → 1500 iff provider == `card`, else 0.
2. `parse_rates` → `{(provider, country): (bps, fixed)}`; lookup precedence exact → `(p,*)` →
   `(*,c)` → `(*,*)` → default; table fee is `amount*bps // 10000 + fixed` (**floor**, PracHub),
   applied to completed payments only.
3. `receivables`: `defaultdict` keyed by the three strings, `net += amount − fee` (fee 0 when
   the CSV has no `status` column — the csoahelp pure-sum shape), header + `sorted(keys)`.
4. `reconcile`: sum amounts per id on each side (duplicates summed), walk the sorted union and
   tag `MISSING_IN_GATEWAY` / `MISSING_IN_SYSTEM` / `AMOUNT_MISMATCH id sys gw`; `include_matches`
   adds `MATCH id`.

## Pitfalls hidden tests target
- 500 cents → 10.5 → **11** (half-up), not banker's 10; 0 cents still costs 30
- `dispute_won` fee only for provider `card` (exact match, `Card` ≠ `card`)
- table rule floors (1234 × 290 bps → 35) while the default rounds half-up (1234 → 56)
- table must not touch disputes; wildcard precedence
- string sort on the three keys (`m10` < `m2`), zero/negative nets printed, header on empty input
- reconciliation: duplicates on one side, ids on one side only, mismatch line carries both amounts

## Reconstructed rules / conflicts
- Part 3 `net = amount − fee` with statuses only changing the fee, and the missing-status → fee 0
  rule, reconcile the csoahelp pure-sum version with the brief's net version (both are tested).
- Reconciliation duplicate-id summation and the `(*, *)` catch-all rate are reconstructions.
- Default rounding half-up vs table floor: both sources are kept as stated rather than unified.

## Complexity & measured cost
O(n) per part plus the group / id sort.
Measured: 0.37 s, 159 MB for 10^5 receivables rows (8 columns) and 0.34 s, 159 MB for a 200k vs
190k reconciliation — perf test budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 4 · part2: 3 · part3: 5 (incl. 1 perf) · part4: 3 (incl. 1 io); edge 6 · fmt 2 · io 1 · perf 1.

## Skills exercised
S02 header-driven CSV · S04 group-by · S06 cents + half-up vs floor · S07 percent + fixed · S08 three-key sort · S09 exact lines · S11 duplicate ids · S18 unknown status/provider · S19 · S21 `csv`/`Decimal` · S24 domain vocabulary
