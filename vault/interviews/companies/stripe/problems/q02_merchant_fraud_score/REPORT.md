# q02 Merchant Fraud Score — report

## Summary
Radar-style merchant risk scoring: a base score per merchant, one rule per transaction, three
rules applied as three ordered passes (amount multiplier, repeat-customer bonus, hourly-density
penalty). Stripe asks it because it is pure "parse → group by key → apply a threshold rule once
per group → render sorted" — the shape of most of their OA bank — and because the strict `>`,
the "count includes the current transaction" and the pass ordering each flip hidden tests.

## Sources & confidence
high — csoahelp 2026-07-06 (fullest statement, primary), oavoservice 2026-01-03, programhelp
2025-10 / 2025-12 / 2026-01, medium @program.net, 1024bbs/1point3acres mentions.
Conflict resolved: oavoservice phrases rule 2 as "add all the pair's additive factors as a
group"; csoahelp/programhelp phrase it per transaction ("3rd and later adds its factor").
Primary = cumulative per-transaction (more sources); the group reading is exposed as
`score(..., repeat_mode="group")` and tested. The stdin section protocol (`MERCHANTS` /
`TRANSACTIONS` / `RULES`) is reconstructed — the OA passes three lists as parameters.

## Approach by part
1. Pass 1: `amount > min_amount` (strict) → `score *= mult`. Applied to the base score only.
2. Pass 2: `Counter[(merchant, customer)]` incremented *before* the check; `>= 3` → `+= add` of
   the current rule.
3. Pass 3: `Counter[(merchant, customer, hour)]`; `>= 3` → `+= sign(hour) * penalty` with
   sign +1 for 12–17, −1 for 9–11 / 18–21, 0 otherwise.
   `score_variant_grouped` (programhelp NG): group sums, `len >= 3` adds the group's amount.

## Pitfalls hidden tests target
- `>=` instead of `>` on the amount threshold; equal amount; zero/negative amounts
- adding on the 2nd transaction (forgetting the current one counts) or adding on every transaction
- multiplying after adding (interleaving the rules per transaction instead of three passes)
- hour band edges 11/12, 17/18, 21/22; applying the penalty only once instead of on every ≥3rd
- dropping merchants with no transactions; string sort (`m10` < `m2`); `id, score` with one space

## Complexity & measured cost
O(n + m log n). 1 000 merchants / 100 000 transactions: 0.19 s, 97 MB RSS (budget 2 s / 256 MB).
Measured: 0.19s, 97 MB

## Test inventory
29 tests — part1: 6 · part2: 5 · part3: 18 (incl. 10 parametrized hour-band cases, 1 io, 1 perf); edge 21 · fmt 1 · io 1 · perf 1.

## Skills exercised
S02 parsing (sectioned input) · S03 records keyed by id · S04 grouping, once-per-group rules ·
S05 strict thresholds · S06 integer money · S08 deterministic sort · S09 exact format ·
S12 hour buckets · S19 incremental design (each pass is one block gated by `upto`)
