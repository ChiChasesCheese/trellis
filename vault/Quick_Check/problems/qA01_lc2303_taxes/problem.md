# qA01 · LC 2303 Calculate Amount Paid in Taxes — graduated brackets, breakdown, cents, volume mode

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** phone screen warm-up / OA part 1 · **Last asked:** tag snapshot 2026-07-12 (>6 months bucket)
**Frequency:** tag freq 92.7 (liquidslr All, 2025-06), 100.0 (liquidslr >6mo), 87.5 all / 100.0 >6mo (snehasishroy 2026-07) · 3 tag mirrors · **Confidence:** high (tag data), medium (no dated candidate write-up names it explicitly)

LC 2303 · *Calculate Amount Paid in Taxes* · Easy · https://leetcode.com/problems/calculate-amount-paid-in-taxes

## Context
Stripe Tax and Stripe Billing both compute **graduated** amounts: the first N units at one rate, the
next band at another, and so on. LC 2303 is exactly that loop with a single income and a bracket table.
The tag data says Stripe interviewers use it as a warm-up; the phone-screen version then grows into
the same follow-ups Billing engineers deal with daily: show the customer a per-band breakdown, do it in
integer cents with a stated rounding mode, and support Stripe's *volume* pricing (whole quantity at one
band's rate) next to *graduated* pricing (each band priced separately). The tiered half of this
problem is the same rule as `q22_shipping_cost` Part 5.

## The problem (restated)
You get `brackets`, a list of `[upper_i, percent_i]` pairs with **strictly increasing** `upper_i`, and an
integer `income`. Money is taxed in bands: the first `upper_0` dollars at `percent_0 %`, the next
`upper_1 - upper_0` dollars at `percent_1 %`, …; income above the last upper bound never happens
(guaranteed `income ≤ upper_last`). Return the total tax as a float (LC accepts an error ≤ 1e-5).
LC limits: `1 ≤ len(brackets) ≤ 100`, `1 ≤ upper_i ≤ 1000`, `0 ≤ percent_i ≤ 100`, `0 ≤ income ≤ 1000`.

## Input (stdin)
```
PART n                         # 1..4
income                         # integer dollars (Part 3: integer cents)
MODE graduated|volume          # Part 4 only
upper,percent                  # one bracket per line, ascending upper (Part 3: upper in cents)
...
```
Blank lines are ignored. Whitespace around `,` is tolerated.

## Output
* Part 1: one line, the tax with two decimals (`2.65`).
* Part 2: one line per bracket that received taxable income: `lower-upper @percent%: taxable -> tax`
  with `tax` two decimals, in bracket order. Income 0 prints nothing.
* Part 3: one line `$x.xx` (cents).
* Part 4: one line, two decimals (same as Part 1) under the chosen mode.

## Rules
### Part 1 — LC signature  `calculate_tax(brackets, income) -> float`
Walk brackets in order; the taxable slice of bracket `i` is `min(income, upper_i) - upper_{i-1}`
(with `upper_{-1} = 0`), clamped at 0. Sum `slice * percent_i / 100`.

### Part 2 — per-bracket breakdown  `tax_breakdown(brackets, income) -> list[BracketLine]`
`BracketLine(lower, upper, percent, taxable, tax)` (NamedTuple) for **every bracket whose taxable
slice is > 0**, in bracket order. `lower` is the previous upper (0 for the first). `sum(line.tax) ==
calculate_tax(...)`.

### Part 3 — integer cents, half-up  `calculate_tax_cents(brackets_cents, income_cents) -> int`
Same table but uppers and income are integer **cents**. Each bracket's tax
`taxable_cents * percent / 100` is rounded **half-up to the cent per bracket** (each band is its own
invoice line, as Stripe Tax rounds per line), then the rounded lines are summed. Never use floats.
`0.125 → 0.13` (half-up, not banker's).

### Part 4 — graduated vs volume  `calculate_tax_mode(brackets, income, mode="graduated") -> float`
`mode="graduated"` is Part 1. `mode="volume"`: the **whole** income is taxed at the percent of the single
bracket that contains it — the first bracket with `upper_i ≥ income`. Income 0 → 0.0 in both modes.
(Stripe Billing "volume" vs "graduated" tiers; identical rule to q22 Part 5.)

## Worked examples
```
LC ex1  brackets=[[3,50],[7,10],[12,25]] income=10 -> 2.65   (3×.5 + 4×.1 + 3×.25 = 1.50+0.40+0.75)
LC ex2  brackets=[[1,0],[4,25],[5,50]]  income=2  -> 0.25   (1×0 + 1×.25)
LC ex3  brackets=[[2,50]]               income=0  -> 0.00
Part 2  ex1 -> [(0,3,50,3,1.5), (3,7,10,4,0.4), (7,12,25,3,0.75)]
        ex2 -> [(0,1,0,1,0.0), (1,4,25,1,0.25)]        (bracket 3 gets nothing -> omitted;
                                                        the 0% bracket still gets a line)
Part 3  brackets=[[300,50],[700,10],[1200,25]] income=1000 (cents) -> 265  ($2.65)
        brackets=[[25,50],[50,50]] income=50 -> 13 + 13 = 26  (0.125 per band -> 0.13 each; a single
                                                              rounding of 0.25 would give 25)
Part 4  ex1 volume -> income 10 lies in bracket (7,12] @25% -> 10×.25 = 2.50   (graduated 2.65)
        income 7 volume -> bracket (3,7] @10% -> 0.70 ; income 8 volume -> 25% -> 2.00
```
stdin for Part 1 ex1:
```
PART 1
10
3,50
7,10
12,25
```
→ `2.65`

## Edge cases hidden tests are known to target
- income 0 → 0.0; income exactly on an upper bound (== upper_i) goes to bracket i, not i+1
- single bracket; percent 0 brackets; percent 100 brackets
- income equal to the last upper (all brackets fully used)
- floating error: `3*0.5 + 4*0.1 + 3*0.25` vs computing in integers then dividing once
- Part 3 half-up on `x.xx5`; rounding per bracket, not once on the total
- Part 4 volume with income on a boundary (`income == upper_i` → bracket i's percent)

## Variants seen in the wild
- Rounding the **total** once instead of per bracket (state which one you do — both are defensible).
- Brackets given as `(lower, upper, rate)` triples or as widths instead of cumulative uppers.
- Same loop as q22 Part 5 tiered shipping and as Stripe Billing's graduated tiers with a flat fee
  per band (`upper,percent,flat`).

## Why Stripe asks it
It is a 5-line loop that still separates candidates who read "strictly increasing uppers" and
"income ≤ last upper" from those who guess; and the follow-ups are Stripe's real Billing/Tax rules.

## Stripe-flavored follow-ups
1. Breakdown per band (the invoice line items) — Part 2.
2. Integer cents with explicit rounding — Part 3.
3. Volume vs graduated pricing — Part 4; then add a flat fee per band (q22 Part 5).

## What this tests
skills: A06 tiered brackets · S06 integer money + rounding · S07 tiered math · S13 boundary discipline · S19 incremental design

## Sources
- https://leetcode.com/problems/calculate-amount-paid-in-taxes
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 92.7)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (freq 100.0)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (freq 87.5 all / 100.0 >6mo)
- catalog/raw/github_repos.md §30 (tag table, freq 92.7)
