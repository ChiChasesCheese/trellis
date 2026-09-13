# q21 Currency Conversion — report

## Summary
Given a rate string `USD:AUD:1.4,CAD:USD:0.8,...`, answer conversion queries: direct quote
only, then the inverse of the opposite quote, then multi-hop (BFS path and best-product path
over simple paths), then a payout batch rounded half-up to cents in `Decimal`. It is the
treasury-desk FX table behind Stripe payouts — LeetCode 399 "Evaluate Division" with strict
formatting and money rounding on top.

## Sources & confidence
high — 4 independent mentions: 1point3acres thread 1048313 (rate string `USD:AUD:1.4,CAD:USD:0.8,
USD:JPY:110`; P1 direct, P2 inverse, P3 multi-hop), 1point3acres thread 1088332
(`AUD->GBP->CAD` vs `AUD->USD->CAD` best-path comparison), 1point3acres 题库 25b1c004, jointaro
"Evaluate Division"; programhelp lists "currency-conversion payouts" as an OA topic (Part 4
format reconstructed).

## Approach by part
`parse_rates`: split on commas and colons, `float(rate)`, reject `<= 0` / non-numeric with
`ValueError`, last quote for an ordered pair wins. `fmt_rate = f"{x:.6f}".rstrip("0").rstrip(".")`.
1. `convert`: identity `1.0` when `src == dst` (even unknown), else the direct quote or `None`.
2. `convert_with_inverse`: direct first, else `1 / rate(dst, src)`.
3. `adjacency`: insertion-ordered dict of dicts, direct edges first, inverse only where the
   opposite pair is unquoted. `find_path` is BFS in first-appearance order; `best_conversion` is
   a DFS over simple paths keeping the maximum product, ties → fewer hops, then lexicographically
   smaller path.
4. `convert_payouts`: best path per `(from, to)` cached, product recomputed in `Decimal` along
   the path (`1 / Decimal(rate)` for inverses), `Decimal(amount) × product` quantized to `0.01`
   with `ROUND_HALF_UP`; unknown / disconnected → `N/A`.

## Pitfalls hidden tests target
- `src == dst` → `1` even for a currency absent from the table; unknown currency → `N/A`
- Part 1 must not use the inverse; Part 2 prefers the direct quote when both exist
- disconnected components; duplicate ordered pair → last wins; rate `0` → `ValueError`
- best product, not first / shortest path (`0.5 × 1.7` beats `0.7 × 1.2`; three 1.1 hops beat
  one 1.2 hop); inconsistent two-way quotes must not loop or inflate (simple paths only)
- `88` not `88.0`, `1` not `1.000000`, `0.714286`; half-up cents (`0.525 → 0.53`, `0.125 → 0.13`)

## Complexity & measured cost
Parse O(q); BFS O(V + E); DFS over simple paths is exponential in the worst case but the
table is ~50 currencies / ~100 quotes; Part 4 caches per pair so 10^5 payouts are O(1) each.
30 currencies (hub + 6 cross rates), 100k payouts: ~0.14 s, ~39 MB RSS (budget 2 s / 256 MB).
Measured: 0.136s, 39 MB

## Test inventory
19 tests — part1: 6 · part2: 2 · part3: 7 · part4: 4; edge 7 · fmt 3 · perf 1 · io 2.
`IMPL=starter`: 19 fail / 0 pass.

## Skills exercised
S02 parsing · S03 graph as dict of dicts · S06 Decimal money + half-up rounding ·
S08 deterministic tie-breaks · S09 exact float formatting · S18 validation (unknown currency,
zero rate) · S19 incremental design (one adjacency builder reused by P2–P4)
