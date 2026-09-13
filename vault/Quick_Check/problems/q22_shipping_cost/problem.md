# q22 · Shipping Cost — carrier routes (direct / one transfer / cheapest path) and country×product matrix (flat / tiered)

**Type:** bespoke · **Stage:** technical phone screen (also intern tech screen; recycled into VO) · **Last asked:** 2026-07 (Blind d4f50dzn names "Shipping Cost" as a phone-screen prep question); 1point3acres 题库 phone screen 2025-12-19; SabihaNazKhan repo 2025-11-24
**Frequency:** ≥ 15 independent mentions — route version: csoahelp 2024-11-20 / 2024-12-27 / 2025-01-18, libaedu, 1024bbs 5821, leetcode discuss 6006563 / 5883672 / 5647506, Glassdoor QTN_7989241, TWINSRIRAM repo; matrix version: SabihaNazKhan repo (verbatim prompt), 1point3acres 题库 shipping-cost-calculator + threads 1131552 / 7331443, programhelp 2025-11-21, oavoservice 2025-12-29, linkjob 2025-12-07, medium azn7u1, Glassdoor QTN_8206177, PracHub, codingkaro, InterviewDB "Shipping Cost — Phone" · **Confidence:** high

Two distinct questions share this title in the wild. Both are implemented here; the stdin
protocol selects one with `PART n` (Parts 1–3 = route version, Parts 4–5 = matrix version).

## Context
Stripe merchants ship physical goods and Stripe Checkout/Tax needs the shipping amount at
checkout time. Version A models the *carrier network*: a table of `origin:destination:carrier:
cost` legs; the question is what it costs to ship from A to B — first with a named carrier and no
transfer, then allowing one transfer (possibly switching carriers), then the cheapest route over
any number of legs. Version B models the *price list*: each destination country has a per-product
shipping price in the smallest currency unit; the order is priced item by item, and later parts
introduce Stripe-Billing-style quantity tiers (volume pricing vs graduated pricing, with flat
bands).

## Input (stdin)
```
PART n
...
```
**Parts 1–3 (route version).** Line 2 is the route string: comma-separated `SRC:DST:CARRIER:COST`
legs, e.g. `US:UK:FedEx:5,UK:US:UPS:4,UK:CA:FedEx:7,US:CA:DHL:10,UK:FR:DHL:2`. Legs are
**directed** (`US:UK` does not imply `UK:US`). `COST` is a non-negative integer. Spaces around
`:` and `,` are tolerated; codes are case-sensitive. The same `(SRC,DST,CARRIER)` may appear
twice — the cheaper leg is kept. Then one query per line: Part 1 `SRC DST CARRIER`; Parts 2–3
`SRC DST`. Up to ~100 legs and 10^5 queries.

**Parts 4–5 (matrix version).** In-memory shapes are the ones from the original prompt (you do
not parse JSON in the interview; the stdin encoding below is only for this drill):
```python
order  = {"country": "US", "items": [{"product": "mouse", "quantity": 20},
                                     {"product": "laptop", "quantity": 5}]}
matrix = {"US": [{"product": "mouse", "cost": 550}, {"product": "laptop", "cost": 1000}],
          "CA": [{"product": "mouse", "cost": 750}, {"product": "laptop", "cost": 1100}]}
# tiered entry (Part 5): a list of contiguous quantity bands starting at 1; "max": None = open-ended
{"product": "laptop", "tiers": [{"min": 1, "max": 2, "cost": 1000},
                                {"min": 3, "max": 4, "cost": 950},
                                {"min": 5, "max": None, "cost": 900}]}
# a band may carry a flat amount instead of a unit cost:
{"product": "rack", "tiers": [{"min": 1, "max": 1, "flat": 2500}, {"min": 2, "max": None, "cost": 900}]}
```
stdin encoding:
```
PART 4                      | PART 5
MATRIX                      | MODE volume            (or MODE graduated)
US mouse 550                | MATRIX
US laptop 1000              | US laptop 1-2:1000 3-4:950 5-:900
CA mouse 750                | US rack 1-1:=2500 2-:900      (=N is a flat band)
ORDER US                    | ORDER US
mouse 20                    | laptop 6
laptop 5                    | ORDER CA
ORDER CA                    | mouse 1
...
```
Matrix lines are `COUNTRY PRODUCT SPEC` where SPEC is a single unit cost (Part 4) or
space-separated bands `lo-hi:cost` / `lo-:cost` / `lo-hi:=flat`. Each `ORDER COUNTRY` line
starts an order; following `PRODUCT QUANTITY` lines are its items until the next `ORDER`.

## Output
One line per query / per order, in input order.
* Part 1: the cost, or `-1`.
* Parts 2–3: `<cost> <path>` where path is `US-FedEx->UK-DHL->FR` (country, `-carrier->`,
  country…); `-1` if unreachable; `0 US` when `SRC == DST`.
* Parts 4–5: the total in cents, or `ERROR: <message>` for a rejected order (see rules).

## Rules
### Part 1 — direct leg with a named carrier  `shipping_cost(routes, src, dst, method) -> int`
Return the cost of the leg `src -> dst` operated by `method`; `-1` if there is none. Only that
exact directed leg counts (no reverse, no transfer). Unknown countries/carriers → `-1`.

### Part 2 — at most one transfer, carrier may change  `shipping_cost_one_transfer(routes, src, dst) -> (cost, path)`
No carrier is given. **A direct leg is always preferred**: if any `src -> dst` leg exists return
the cheapest one (any carrier) even when a two-leg route would be cheaper. Otherwise return the
cheapest `src -> X -> dst` over all intermediates `X` and carrier combinations. Ties: the
lexicographically smallest alternating path `[src, carrier, X, carrier, dst]`. Nothing found →
`(-1, [])`. `src == dst` → `(0, [src])` (never a 2-leg loop).

### Part 3 — cheapest route over any number of legs  `cheapest_shipping(routes, src, dst) -> (cost, path)`
Dijkstra on the directed multigraph (costs ≥ 0). Ties: fewer legs first, then the
lexicographically smallest alternating path. `src == dst` → `(0, [src])`. Unreachable → `(-1, [])`.

### Part 4 — flat matrix  `calculate_shipping_cost(order, matrix) -> int`
`total = Σ quantity × unit cost` over the items, looked up as `matrix[country][product]`. The
country list form (`[{"product":…, "cost":…}, …]`) and the dict form (`{"mouse": 550}` or
`{"mouse": {"cost": 550}}`) are both accepted; if a product is listed twice the **last entry
wins**. Errors (raise `ValueError`; stdin prints `ERROR: <message>`):
* unknown country → `unknown country 'XX'`
* unknown product for that country → `unknown product 'foo' for country 'US'`
* negative quantity → `negative quantity for 'foo'`; quantity 0 contributes 0.
Quantities of the **same product inside one order are summed** before pricing (reconstructed —
sources say "no double billing" across the tiers; for flat prices this changes nothing).

### Part 5 — quantity tiers  `calculate_shipping_cost(order, matrix, mode="volume" | "graduated")`
A product's entry is a list of contiguous bands `[min, max]` (`max=None` = open) starting at 1.
* `mode="volume"` (Stripe *volume pricing*): find the band containing the **whole quantity**
  and charge `quantity × cost` at that band's unit cost (or the band's `flat` amount once).
* `mode="graduated"` (Stripe *graduated pricing*, "incremental"): each band is priced separately
  on the units that fall inside it — `units_in_band × cost`, or the band's `flat` amount once if
  at least one unit falls in it. No unit is billed twice.
A flat-price entry (`{"cost": 550}`) is a single open band. `quantity == 0` → 0 in both modes.
A quantity beyond the last (closed) band → `ValueError("no tier for quantity …")`.

## Worked examples
Route string `US:UK:FedEx:5,UK:US:UPS:4,UK:CA:FedEx:7,US:CA:DHL:10,UK:FR:DHL:2`
```
PART 1: US UK FedEx -> 5 ; US CA DHL -> 10 ; US CA FedEx -> -1 ; UK US UPS -> 4 ; US FR DHL -> -1
PART 2: US FR -> 7 US-FedEx->UK-DHL->FR      (no direct; US->UK 5 + UK->FR 2)
        US CA -> 10 US-DHL->CA               (direct preferred; US->UK->CA = 12 anyway)
        CA US -> -1                          (CA has no outgoing leg)
PART 3: US FR -> 7 US-FedEx->UK-DHL->FR ; US CA -> 10 US-DHL->CA ; UK UK -> 0 UK
```
Route string `A:B:UPS:1,B:C:UPS:1,C:D:UPS:1,A:D:DHL:5,A:C:FedEx:1`
```
PART 2: A D -> 5 A-DHL->D                    (direct beats the cheaper A->C->D = 2)
PART 3: A D -> 2 A-FedEx->C-UPS->D           (A->B->C->D = 3, direct = 5)
```
Matrix (verbatim from the phone-screen repo): US mouse 550 / laptop 1000; CA mouse 750 / laptop 1100
```
PART 4: ORDER US mouse 20, laptop 5 -> 16000   (20*550 + 5*1000)
        ORDER CA mouse 20, laptop 5 -> 20500   (20*750 + 5*1100)
        ORDER FR mouse 1              -> ERROR: unknown country 'FR'
```
Tiered matrix (verbatim repo driver data): US laptop 1-2:1000 3-4:950 5-:900, US mouse 1-:550;
CA laptop 1-2:1100 3-:1000, CA mouse 1-:750. Order: mouse 20, laptop 5.
```
MODE volume    : US -> 15500 (20*550 + 5*900)        CA -> 20000 (20*750 + 5*1000)
MODE graduated : US -> 15800 (11000 + 2*1000+2*950+1*900)   CA -> 20200 (15000 + 2*1100+3*1000)
```
Stripe docs tiers `1-5:700 6-:650`, quantity 6 → graduated **4150** (5×700 + 1×650), volume **3900** (6×650).
Flat band `rack 1-1:=2500 2-:900`: qty 1 → 2500 (both modes); qty 3 graduated → 4300 (2500 + 2×900); qty 3 volume → 2700; qty 0 → 0.

## Edge cases hidden tests are known to target
- legs are directed: `UK:US:UPS:4` does not make `US UK UPS` = 4
- Part 1 with the right pair but the wrong carrier → `-1`
- Part 2: direct leg preferred even when a transfer is cheaper; carrier switch at the transfer
- Parts 2–3: `src == dst` → `0 US` (not a `US->UK->US` loop); unreachable → `-1`; zero-cost legs; duplicate legs (cheaper kept)
- Part 4: unknown country / product, quantity 0, negative quantity, product duplicated in the
  order (summed) and in the matrix (last wins)
- Part 5: band boundaries (`max` inclusive: qty 2 vs 3 vs 4 vs 5), quantity exactly at the
  Stripe-docs boundary (5 → 3500 in both modes), open-ended last band with a huge quantity
  (integer arithmetic), flat bands charged once, graduated vs volume on the same input
- cents everywhere; never float

## Variants seen in the wild
- Route string with `,` inside legs and `:` between legs: `"US,UK,UPS,5:US,CA,FedEx,3"` (TWINSRIRAM) —
  `parse_routes` accepts this too (auto-detects which separator is the leg separator).
- FX flavour of the same parser: `"USD:CAD:DHL:5,USD:GBP:FEDX:10"` → `convert(amount, from, to)` (Glassdoor).
- Part 2 that also returns the carriers involved / Part 3 "minimum cost with at most one hop" (leetcode 6006563) — Part 2 here already returns the cheapest 2-leg route with carriers.
- Matrix Part 3 as `incremental` vs `fixed` per tier (en_forums §23) — that is `mode="graduated"` with `flat` bands.
- PracHub JS: `calculateShipping(destination, quantity, config)` returning `null` for unknown destination and 0 for `qty <= 0`.

## What this tests
S02 parsing · S03 modelling (records + dict keyed by (src,dst)) · S06 integer money · S07 tiered math (graduated vs volume) · S08 deterministic tie-breaks · S13 inclusive band boundaries · S18 validation/error paths · S19 incremental design · A03 shortest path with ≤K stops

## Sources
- https://github.com/SabihaNazKhan/StripePhoneScreen24Nov25/blob/master/src/Solution.java (verbatim matrix prompt + tiered driver data, phone screen 2025-11-24)
- https://github.com/TWINSRIRAM/Stripe_OA_Prep/blob/main/shipping_cost.cpp (route/Dijkstra variant)
- https://leetcode.com/discuss/post/6006563/ (Stripe screening US 2024 — 4-part route version)
- https://leetcode.com/discuss/post/5883672/ (Stripe Phone Screen 2024-10-07)
- https://leetcode.com/discuss/post/5647506/ (Stripe Technical Interview 2024-08-16)
- csoahelp 2024-11-20 / 2024-12-27 / 2025-01-18; libaedu; 1024bbs 5821 (route version, `shippingCost(str, src, dst, method)`, one-transfer follow-up)
- 1point3acres 题库 shipping-cost-calculator (phone screen, last asked 2025-12-19); 1point3acres threads 1131552, 7331443
- programhelp 2025-11-21; oavoservice 2025-12-29; linkjob 2025-12-07; medium @azn7u1 (matrix + tiers)
- Glassdoor QTN_8206177 (tier-based shipping), QTN_7989241 (`USD:CAD:DHL:5` parser); Blind d4f50dzn (Jul 2026); PracHub; InterviewDB "Shipping Cost — Phone"
