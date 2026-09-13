# q03 Chat Billing — report

## Summary
Metered + subscription billing with mid-month plan switch. It is Stripe Billing's "usage-based
price with an included allowance" reduced to arithmetic. The whole difficulty is in three rules
that are easy to get subtly wrong: per-session block rounding, allowance consumption order, and
prorated-fee rounding.

## Sources & confidence
high — 1point3acres 题库 (2 entries, last asked 2026-04-17), 1point3acres company page, 1024bbs mention.

## Approach by part
1. `billable(tokens) = tokens // 100 * 100` **per session**; payg cost = 3¢/4¢ per block.
2. fixed: fee 1500¢ + combined 40,000-token allowance consumed in input order (input before
   output within a session); overage priced at payg block rates.
3. switching: `r = fixed/total` sessions; fee = `round_half_up(1500·r)` done as
   `(2·1500·fixed + total) // (2·total)`; allowance = `40000·fixed // total`.

## Pitfalls hidden tests target
- $0.00 users omitted; `x.xx5` fee rounding (r = 1/8 → 1.875 → **1.88**); allowance exactly hit;
  overage split across input/output; remainders pooled across sessions (wrong); float drift on
  10^9 tokens; string-order sort (`user10` < `user2`).

## Complexity & measured cost
O(n log u). 100k sessions / 5k users: ~0.15 s, ~15 MB RSS (perf test budget 2 s / 256 MB).

## Test inventory
21 tests — part1: 6 · part2: 5 · part3: 10 (incl. 2 io, 1 perf); edge 9 · fmt 2.

## Skills exercised
S02 parsing · S04 grouping · S06 integer money/rounding · S07 metered math · S08 sort · S09 format · S19 incremental design
