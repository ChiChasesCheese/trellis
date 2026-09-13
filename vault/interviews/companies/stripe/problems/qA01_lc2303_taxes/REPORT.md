# qA01 LC 2303 Calculate Amount Paid in Taxes — report

## Summary
Graduated tax brackets: the LeetCode Easy that heads the Stripe tag (freq 87–100). Stripe uses it as
a warm-up because it is the same loop as Billing's graduated tiers and Tax's per-band computation;
the follow-ups (breakdown lines, integer cents with half-up rounding, volume vs graduated) are the
production version of the same rule and reuse q22 Part 5's tier logic.

## Sources & confidence
high (tag data): liquidslr All 92.7 / >6mo 100.0 (2025-06-20), snehasishroy all 87.5 / >6mo 100.0
(2026-07-12), github_repos.md §30. No dated candidate write-up names the problem explicitly → the
follow-ups are designed (marked as Stripe-flavored), not reported.

## Approach by part
1. `_slices()` yields `(lower, upper, percent, taxable)` with `taxable = min(income, upper) - lower`,
   stopping at the first empty slice (uppers strictly increasing). Sum `taxable*percent` as an
   integer and divide once → no float drift. O(n).
2. Same generator wrapped in `BracketLine` NamedTuples; only brackets with taxable > 0.
3. Integer cents; per-bracket half-up = `(taxable*percent + 50) // 100`; lines summed after rounding.
4. `volume`: first bracket with `upper >= income` supplies the single rate; income 0 → 0.

## Pitfalls hidden tests target
- income exactly on an upper bound belongs to that bracket (both modes)
- breaking early only valid because uppers are strictly increasing
- float accumulation across 100 brackets (`0.03` × 100 ≠ 3.0) — compute in hundredths
- half-up vs banker's rounding at `x.5` cents; per-bracket rounding (26) ≠ total rounding (25)
- 0% bracket still gets a breakdown line; income 0 gets no lines

## Complexity & measured cost
O(n) per query, O(1) extra. Measured: 0.08s (10^4 in-process calls at LC max + one script run),
script run at LC max 0.02s, ~10 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 6 (incl. 1 io, 1 perf) · part2: 4 (incl. 1 io) · part3: 3 · part4: 2; edge 7 · fmt 1.

## Skills exercised
A06 tiered brackets · S06 integer money/rounding · S07 tiered math · S13 boundary discipline · S19 incremental design
