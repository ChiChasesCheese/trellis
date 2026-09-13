# ps02 · Shipping Cost Pricing — flat price → quantity tiers → incremental/fixed mixed billing

**Type:** phone screen / intern tech screen (unlock-next-part, HackerRank) · **Stage:** Technical Phone Screen (~1 hour, "time is tight") · **Last asked:** 2025-10-20 (learncswithus.com) · **Frequency:** 2 independent write-ups (learncswithus.com detailed three-level breakdown; 1point3acres.com/interview/post/7100079 "Shipping Cost Calculator" TOC that matches it step-for-step) + linkjob.ai P9 "Accounting / tiered pricing" intern tech screen (`en_forums.md` line 151, 2025, "Part 1 order+shipping total → Part 2 tiered pricing, unit price decreases as quantity increases → Part 3 two billing models: incremental vs fixed-pricing") independently confirming the same three-level shape from the English-language side · **Confidence:** high (two Chinese sources with near-identical TOC + one English source confirming the same 3-part progression and, critically, the exact `incremental` / `fixed` terminology for Part 3)

## Context
An e-commerce platform on Stripe needs to price shipping at checkout: a country/product rate
table plus a list of orders. Level 1 is a flat per-unit price lookup (dict). Level 2 turns the
rate into quantity **tiers** (volume bands) — candidates in the wild report this as "the hardest
level, because there's no explicit type to distinguish it from Level 1, you have to notice the
interval logic yourself." Level 3 adds a `type` per band (`incremental` vs `fixed`), which is
exactly graduated/tiered pricing vs. a single flat-rate band — the same distinction Stripe
Billing's own pricing model draws between `graduated` and `tiered` (`volume`) pricing.

## Input (stdin)
```
PART n
RATES
<rate row>
<rate row>
...
ORDERS
<order row>
<order row>
...
```
* `PART n` — `n` ∈ {1,2,3}. The `RATES` and `ORDERS` literal marker lines are required and
  case-sensitive; everything between them is a rate row, everything after is an order row.
* **Order row** (all parts): `order_id,country,product,quantity` — `quantity` is a non-negative
  integer. Output is **one line per order, in input order** (orders are independent queries,
  not aggregated/grouped/sorted — unlike ps01/q03's per-user grouping).
* **Rate row**, schema depends on `PART n`:
  - Part 1 (flat): `country,product,unit_cost`
  - Part 2 (tiered): `country,product,min_qty,max_qty,cost` — `cost` is the **per-unit** rate
    for that band.
  - Part 3 (mixed): `country,product,min_qty,max_qty,cost,type` — `type` ∈
    `{incremental, fixed}`.
* All money fields (`unit_cost`, `cost`) are plain decimal strings with **0–2 decimal digits**,
  no currency symbol, no thousands separator (`5`, `5.0`, `5.00`, `12.50` all valid; `12.5000`
  is a format error). Parsed to integer cents — **never floats**.
* `min_qty`/`max_qty` are integers; `max_qty` may be the **literal token `inf`** (lowercase,
  exact) meaning open-ended. The interval is **closed on both ends**: `[min_qty, max_qty]`
  (a quantity exactly equal to either boundary is inside that band).
* Bands for the same `(country, product)` **do not overlap**, but **may appear in any order**
  in the rate table (sort by `min_qty` before using them — do not assume the file is sorted).
* Up to ~200 rate rows and 10^5 order rows.

## Output
One line per order, in input order: `order_id: $x.xx` (two decimals, `$` sign, `: ` separator,
same style as the OA convention), or `order_id: ERROR <message>` for a rejected order — see the
three error message formats below (pinned exactly, hidden tests match them verbatim).

## Rules

### Part 1 — flat unit price
`unit_cost × quantity`. If `(country, product)` has no rate row at all:
`ERROR unknown product <country>/<product>`. `quantity = 0` always prices at `$0.00` (still
requires the product to exist in the rate table — a zero-quantity order for an unknown product
is still an error).

### Part 2 — quantity tiers, single matched-band rate
Find the band whose `[min_qty, max_qty]` contains the order's `quantity` (closed interval,
`max_qty = inf` = no upper bound). The **entire** order quantity is billed at that one band's
rate: `cost × quantity` (not cumulative — a 15-unit order that lands in the "11–20" band pays
`15 × band_11_20.cost`, full stop; this is what Part 3 below calls the `fixed` billing type).
Errors (checked in this order):
1. `(country, product)` has no rate rows at all → `ERROR unknown product <country>/<product>`
2. rate rows exist but no band's interval contains `quantity` (a **gap** in coverage, or
   `quantity` below the first band's `min_qty`) → `ERROR no tier for <country>/<product> at qty=<quantity>`
`quantity = 0` prices at `$0.00` without a tier lookup (same product-must-exist rule as Part 1).

### Part 3 — mixed incremental/fixed billing
Same tier lookup as Part 2 (find the band containing `quantity`; same two error cases with the
same messages). The **type of the matched band** — not any other band — decides how the whole
order is priced:
* **`fixed`**: identical to Part 2 — `matched_band.cost × quantity`.
* **`incremental`**: graduated/progressive billing (tax-bracket style). Starting from `min_qty
  = 1`, walk every band in ascending `min_qty` order up through the matched band; each band
  contributes `(units of quantity that fall inside it) × that band's own cost`, where "falls
  inside it" is capped at `quantity` for the last (matched) band. The bands walked **must be
  contiguous starting at 1** (`band[i].min_qty == band[i-1].max_qty + 1`, first band's
  `min_qty == 1`) — a break in that chain **below or at** the matched band is a distinct error:
  `ERROR incremental gap for <country>/<product> at qty=<quantity>` (only raised if the order's
  quantity actually requires walking through the gap — a quantity fully inside a band **before**
  a gap never sees it, see worked example below).
* A gap check is per-order, not a rate-table validation pass — a rate table may contain gaps
  that no order ever queries into, and that is not an error.

## Worked examples
```
# Part 1
RATES
US,widget,5.00
CA,widget,7.25
ORDERS
o1,US,widget,3
o2,CA,widget,2
o3,US,gadget,1
-->
o1: $15.00
o2: $14.50
o3: ERROR unknown product US/gadget

# Part 2 (tiers unsorted in the file on purpose — must sort by min_qty before use)
RATES
US,widget,21,inf,4.00
US,widget,1,10,5.00
US,widget,11,20,4.50
ORDERS
o1,US,widget,5
o2,US,widget,15
o3,US,widget,50
-->
o1: $25.00     (5 units, all at the 1-10 band's 5.00 -> 5 * 5.00)
o2: $67.50     (15 units, all at the 11-20 band's 4.50 -> 15 * 4.50, NOT cumulative)
o3: $200.00    (50 units, all at the 21-inf band's 4.00 -> 50 * 4.00)

# Part 3 (same 1-10/11-20/21-inf US ladder, now 'incremental'; a separate CA ladder, 'fixed')
RATES
US,widget,1,10,5.00,incremental
US,widget,11,20,4.50,incremental
US,widget,21,inf,4.00,incremental
CA,widget,1,10,5.00,fixed
CA,widget,11,20,4.50,fixed
ORDERS
o1,US,widget,15
o2,CA,widget,15
-->
o1: $72.50     (incremental: 10 units @ 5.00 = 50.00, + 5 units @ 4.50 = 22.50 -> 72.50)
o2: $67.50     (fixed: matched band is 11-20 @ 4.50 -> 15 * 4.50, same number as Part 2's o2)

# Part 3 — incremental gap, order-dependent (this is the subtle one; verify it by hand)
RATES
US,widget,1,10,5.00,incremental
US,widget,15,inf,3.00,incremental
ORDERS
o1,US,widget,5
o2,US,widget,20
-->
o1: $25.00                                          (5 units, entirely inside 1-10, never
                                                       touches the 11-14 gap -> no error)
o2: ERROR incremental gap for US/widget at qty=20    (matched band is 15-inf, but walking the
                                                       chain from 1 hits the 11-14 hole first)
```

## Edge cases hidden tests are known to target
- Part 1: unknown `(country, product)` pair; `quantity = 0`; money strings with 0/1/2 decimal
  digits (`"5"`, `"5.5"`, `"5.50"` all mean the same 5.50).
- Part 2: tier rows out of order in the file (must sort); quantity exactly on a band boundary
  (`min_qty` and `max_qty` both inclusive — test both edges of the same band); quantity in a
  genuine gap between two bands; `max_qty = inf` open-ended top band; `quantity = 0`.
- Part 3: `fixed` vs `incremental` on the **same quantity** must give different, both-correct
  answers (the worked example above, `$67.50` vs `$72.50` on quantity 15); an order whose
  quantity is fully inside the first band never sees a downstream gap (no false error); an
  order whose quantity requires crossing a gap **does** error, with the `incremental gap`
  message (not the `no tier` message — the matched-band lookup itself succeeded).
- Format: money output always two decimals, always a `$` sign; error messages match the three
  templates **verbatim** (`unknown product`, `no tier`, `incremental gap`) — hidden tests do
  exact string comparison, not substring/prefix matching.
- Performance: up to ~200 rate rows and 10^5 order rows; a dict-of-lists rate table with O(log
  bands-per-product) lookup per order keeps this comfortably under budget (bands per product
  are few in practice — a linear scan per order is also fine at this scale, and is what the
  reference solution does; mention the `bisect` alternative as a follow-up, don't over-engineer
  it up front).

## Variants seen in the wild
- learncswithus.com explicitly reports "no explicit type to distinguish [Level 2 from Level 1],
  you have to notice the interval logic yourself" — i.e. in the real interview the tier schema
  isn't handed to you as cleanly as this drill's five-field CSV; expect to have to infer the
  shape from a natural-language spec or a nested dict, and to ask clarifying questions about
  half-open vs closed intervals (this drill nails that down; the real interview may not).
- linkjob.ai's P9 write-up (`en_forums.md` line 151) frames Part 1 as "order + shipping cost"
  rather than a pure per-unit lookup — i.e. some variants fold a flat shipping surcharge into
  Part 1's total. Not implemented here (out of scope per the CN source's three-level TOC), but
  worth naming as a live follow-up ("what if there's also a flat per-order shipping fee?").
- The grading note from the primary source: **no automated test harness in the real interview**
  ("you write and run your own test cases") and grading is "logic correctness + code structure,
  boundary handling not enforced" — i.e. real candidates are graded more leniently on the exact
  interval edge cases this drill's hidden tests pin down strictly. Treat the strictness here as
  interview *practice*, not a claim that Stripe's real rubric is this exacting.

## Sources
- https://learncswithus.com/2025/10/20/stripe-intern-screen/ (Stripe SDE Intern 面经｜Technical Screen, 2025-10-20) — primary source: three-level structure (flat -> tiered -> mixed incremental/fixed), HackerRank platform, ~1 hour, "no automated test cases", "time is tight" grading note.
- https://www.1point3acres.com/interview/post/7100079 ("Shipping Cost Calculator" — Problem Summary -> Step 1 Simple Fixed Price -> Step 2 Volume Discounts -> Step 3 Mixed Pricing Types -> How to Solve It -> Bonus Discussion Topics) — cross-confirms the exact same 3-level progression from a second, independent CN source.
- `loop/raw/en_forums.md` line 151, P9 "Accounting / tiered pricing" (linkjob.ai intern tech screen write-up, 2025) — English-side confirmation of the same 3-part shape and the `incremental` / `fixed` terminology for Part 3.
- `loop/raw/cn_forums.md` lines 43–56 (aggregated CN summary, cross-references both sources above).

## What this tests
skills: S02 parsing (fixed-width vs variable-width CSV rows, section markers) · S06 integer
money (cents, never floats) · S07 tiered/metered pricing math (closed-interval band lookup,
graduated vs flat billing) · S09 exact formatting (money + verbatim error strings) · S10 defined
error handling (three distinct, pinned error messages) · S19 incremental design (Part 2's single
lookup is reused unmodified as Part 3's `fixed` branch)

## 面试官会怎么追问
1. "如果同一个 `(country,product)` 在 Part 2 的费率表里出现了两条区间重叠的行,你的代码会怎么样?"
   — 题面保证"不重叠",但追问是在探你是否会做防御性校验,还是假设输入总是合法就直接崩。
2. "Part 3 的 `incremental` 类型,如果费率表从 `min_qty=1` 往上数不连续(有缺口),但订单数量恰好
   落在缺口*之前*的那个 band 里,你的代码会不会误报错?" — 直接对应 worked example 里 qty=5 vs
   qty=20 的区别,检验候选人是否真的理解"只在需要穿过缺口时才报错"这条设计。
3. "如果要求换成开区间 `(min_qty, max_qty]` 或半开区间,worked example 里 Part 2 的三个答案
   (25.00 / 67.50 / 200.00)哪些会变?" — 逼你现场证明"闭区间"是让边界值(qty=10、qty=21)有唯一
   归属的必要条件。
4. "现在货币是按美分存的整数,如果面试官要求支持 3 位小数的货币(比如某些中东货币),你的
   `parse_money_to_cents` 要怎么改?" — 考察是否把"两位小数"硬编码在了多处,还是只在一个地方。
5. "10 万条订单、200 条费率,如果要求把 `_find_band` 从线性扫描换成 `bisect` 二分,你会怎么改
   数据结构?" — 期望候选人指出"每个 (country,product) 的 band 数通常很小,线性扫描已经够快;
   只有 band 数很大时二分才有意义",而不是无脑上二分。
6. "如果一个订单里有多个 product(比如一次下单买 20 个 widget 和 5 个 gadget),现在的 CSV
   protocol 要怎么扩展?" — 检验候选人是否能在不推翻现有单行 order 设计的前提下,提出一个自然的
   扩展(比如允许同一个 `order_id` 出现多行,按 `order_id` 分组求和)。
7. "费率表本身没有校验步骤 —— 如果要在读入费率表时就检测出所有 `incremental` 链条的缺口(而不是
   等订单查询时才发现),你会怎么设计一个预处理校验函数?它的时间复杂度是多少?" — 把"运行时检测"
   升级成"静态校验",考察候选人对 O(bands log bands) 排序 + 一次线性扫描的复杂度分析能力。
