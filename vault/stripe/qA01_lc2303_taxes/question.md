# qA01 · LC 2303 Calculate Amount Paid in Taxes — graduated brackets, breakdown, cents, volume mode

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

## 关联知识点

- [[a06-graduated-tax-brackets|A06 累进税 / 阶梯]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s07-tiered-metered-proration|S07 阶梯 / 计量 / 按比例分摊]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
