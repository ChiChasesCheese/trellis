# q21 · Currency Conversion — direct, inverse and multi-hop best rate

**Type:** bespoke · **Stage:** phone screen (also recycled into OA) · **Last asked:** 2025–2026 (1point3acres 電面帖 1048313 / 1088332; 题库 25b1c004)
**Frequency:** 4 independent mentions (1point3acres 1048313, 1088332, 题库 25b1c004, jointaro "Evaluate Division"; programhelp lists "currency-conversion payouts" as an OA topic) · **Confidence:** high

## Context
Stripe settles payouts in the merchant's local currency. The treasury desk publishes a small
table of exchange rates, but not every pair is quoted directly: `AUD → JPY` may only be
reachable through `USD`. Given the rate table, compute the rate between any two currencies —
first only direct quotes, then allowing the inverse of a quote, then multi-hop paths, and
finally apply the rates to a batch of payouts, rounding to cents.

## Input (stdin)
```
PART n
<rate string>
<query lines...>
```
* `<rate string>`: comma-separated `FROM:TO:RATE` triples, e.g.
  `USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110`. Spaces around separators are tolerated. Currency codes
  are compared as given (case-sensitive). `RATE` is a positive decimal; **a rate ≤ 0 or a
  non-numeric rate is invalid and the whole input is rejected (`ValueError`)**. If the same
  ordered pair appears twice, **the last quote wins**.
* Parts 1–3 queries: one `SRC DST` per line. Part 4 queries: one `amount,from,to` per line.
* Blank lines are ignored. Up to ~50 currencies, ~100 quotes, up to 10^5 query lines.

## Output
One line per query line, in input order.
* Parts 1–3: the rate formatted with **`f"{x:.6f}".rstrip("0").rstrip(".")`** (at most 6
  decimals, trailing zeros and a trailing dot removed: `1.4`, `0.714286`, `88`, `1`), or `N/A`
  when no conversion exists. Part 3 appends the path: `78.571429 AUD->USD->JPY`.
* Part 4: `<amount> <from> -> <to> = <x.xx>` with the converted amount rounded **half-up** to
  2 decimals (`decimal.Decimal`, `ROUND_HALF_UP`), or `= N/A`.

## Rules
### Part 1 — direct rate  `convert(rates, src, dst) -> float | None`
Return the quoted rate for the ordered pair `(src, dst)`, `None` if it is not quoted or either
currency is unknown. **`src == dst` always returns `1.0`** (identity; needs no quote).

### Part 2 — inverse rate  `convert_with_inverse(rates, src, dst) -> float | None`
As Part 1, but if `(src, dst)` is not quoted and `(dst, src)` is, return `1 / rate(dst, src)`.
A direct quote always beats the inverse of the opposite quote (even when both exist and are
inconsistent).

### Part 3 — multi-hop  `find_path(rates, src, dst) -> list[str] | None` and `best_conversion(rates, src, dst) -> tuple[float, list[str]] | None`
Build the graph with every quote and (when the opposite pair is not quoted) its inverse.
* `find_path` (BFS): *any* path with the fewest hops; neighbours are explored in the order
  their quotes first appear in the rate string. Returns the currency list, e.g.
  `['AUD', 'USD', 'JPY']`, `[src]` when `src == dst`, `None` if disconnected/unknown.
* `best_conversion` (DFS): the rate is the **maximum product of edge rates over all simple
  paths** from `src` to `dst`; the path that attains it is returned with it. **Cycles are
  ignored** (each currency at most once on a path), so inconsistent quotes cannot create an
  arbitrage loop that inflates the answer. Ties: fewer hops first, then lexicographically
  smaller path. `src == dst` → `(1.0, [src])`.
The rate to print in Part 3 is `best_conversion`'s rate and path.

### Part 4 — payouts (reconstructed)  `convert_payouts(rates, payouts) -> list[str]`
Each payout line is `amount,from,to` (`amount` is a decimal string, may be `0`). Rate = Part 3's
best path, but the product is **recomputed in `Decimal`** along that path (inverse = `1 /
Decimal(rate)` at 28 significant digits) so the cent rounding is not disturbed by float noise.
Result = `Decimal(amount) × product`, quantized to `0.01` with `ROUND_HALF_UP`. Unknown or
disconnected → `N/A`. Best rates are cached per `(from, to)` so 10^5 payouts stay fast.

## Worked examples
Rates: `USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110`
```
PART 1
USD AUD   -> 1.4
CAD USD   -> 0.8
AUD USD   -> N/A          (only USD->AUD is quoted)
USD USD   -> 1
USD GBP   -> N/A          (unknown currency)

PART 2
AUD USD   -> 0.714286     (1 / 1.4 = 0.7142857…)
USD CAD   -> 1.25         (1 / 0.8)
USD AUD   -> 1.4          (direct still wins)

PART 3
AUD JPY   -> 78.571429 AUD->USD->JPY     ((1/1.4) × 110)
CAD AUD   -> 1.12 CAD->USD->AUD          (0.8 × 1.4)
CAD JPY   -> 88 CAD->USD->JPY
JPY JPY   -> 1 JPY
```
Best path (the source's `AUD->GBP->CAD` vs `AUD->USD->CAD` comparison), rates
`AUD:USD:0.7,USD:CAD:1.2,AUD:GBP:0.5,GBP:CAD:1.7`:
```
PART 3
AUD CAD   -> 0.85 AUD->GBP->CAD          (0.5 × 1.7 = 0.85 beats 0.7 × 1.2 = 0.84)
```
(`find_path` would return `['AUD', 'USD', 'CAD']` — the first 2-hop path BFS finds.)

Part 4, rates `USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110`:
```
PART 4
100,USD,AUD        -> 100 USD -> AUD = 140.00
100,AUD,JPY        -> 100 AUD -> JPY = 7857.14        (7857.142857…)
0.375,USD,AUD      -> 0.375 USD -> AUD = 0.53         (0.525 → half-up 0.53; banker's would give 0.52)
0.15625,CAD,USD    -> 0.15625 CAD -> USD = 0.13       (0.125 → 0.13)
50,USD,GBP         -> 50 USD -> GBP = N/A
7,EUR,EUR          -> 7 EUR -> EUR = 7.00
```

## Edge cases hidden tests are known to target
- `src == dst` → 1 (even for a currency that appears nowhere in the table)
- unknown currency on either side → `N/A` / `None`, never an exception
- Part 1 must **not** use the inverse; Part 2 must prefer the direct quote when both exist
- disconnected components (`USD:AUD:1.4,EUR:GBP:0.9`, query `USD GBP`) → `N/A`
- duplicate ordered pair: last quote wins (`USD:AUD:1.4,USD:AUD:1.5` → 1.5)
- rate `0` (or negative / non-numeric) → `ValueError` at parse time
- multi-hop must pick the **best** product, not the first or the shortest path
- a longer path may beat a shorter one (3 hops at 1.1 each beats 1 hop at 1.2)
- inconsistent quotes both ways (`USD:AUD:1.4,AUD:USD:0.8`) must not loop / inflate
- formatting: `88` not `88.0`, `1` not `1.000000`, `0.714286` (6 decimals, rounded)
- half-up cent rounding on `x.xx5` (0.525 → 0.53, 0.125 → 0.13)

## Variants seen in the wild
- Rate string `AUD:USD:0.7,AUD:JPY:100,USD:CAD:1.2` (1point3acres 1088332) — same rules.
- jointaro frames it as LeetCode 399 "Evaluate Division" (`a/b = 2.0` equations) — identical
  graph, answer `-1.0` for unknown instead of `None`.
- Some tellings ask only "can you convert?" (boolean reachability, Part 3's `find_path`).
- Payout batch (Part 4) is reported by programhelp as "currency-conversion payouts" without
  a format; the format here is reconstructed.

## What this tests
skills: S02 parsing · S03 modelling (graph as dict of dicts) · S06 Decimal money + half-up
rounding · S08 deterministic tie-breaks · S09 exact float formatting · S18 validation (unknown
currency, zero rate) · S19 incremental design (P1 → P2 → P3 reuse one adjacency builder)

## Sources
- 1point3acres thread 1048313「Stripe 電面新題」(rate string `USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110`; P1 direct, P2 inverse, P3 multi-hop)
- 1point3acres thread 1088332「Stripe滇缅」(LC medium; `AUD:USD:0.7,AUD:JPY:100,USD:CAD:1.2`; compare `AUD->GBP->CAD` vs `AUD->USD->CAD`)
- 1point3acres 题库 problems/25b1c004 (Currency Conversion)
- jointaro "Evaluate Division" (LeetCode 399 framing)
- programhelp: "currency-conversion payouts" listed among OA topics (catalog/raw/process_and_jd.md §A.8)
