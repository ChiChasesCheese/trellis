# q22 Shipping Cost — report

## Summary
The most-cited Stripe phone-screen question of 2025–26 ("Shipping Cost" is named alongside
"Currency Conversion" as *the* prep pair). Two different problems hide behind the title, so both
are implemented: (A) a carrier-route table `SRC:DST:CARRIER:COST` queried direct → one transfer →
cheapest path (the same parse-then-graph shape as q21), and (B) a country×product price matrix
priced per item and then with Stripe Billing's two tier semantics, *volume* (whole quantity at
one band's price) vs *graduated* (each band priced on its own units, flat bands charged once).

## Sources & confidence
high — route version: csoahelp ×3 (2024-11 → 2025-01), libaedu, 1024bbs 5821, three leetcode
discuss posts (5647506 / 5883672 / 6006563), Glassdoor QTN_7989241, TWINSRIRAM repo; matrix
version: SabihaNazKhan phone-screen repo (verbatim prompt + tiered driver data, 2025-11-24),
1point3acres 题库 (phone screen, last asked 2025-12-19) + two threads, programhelp, oavoservice,
linkjob, medium, Glassdoor QTN_8206177, PracHub, InterviewDB; Blind Jul-2026 mention.

## Approach by part
1. `parse_routes` (auto-detects `:`/`,` as the leg separator); Part 1 is a filter over the legs
   out of `src` — exact directed leg + carrier, cheapest if duplicated, else −1.
2. One transfer: direct legs (any carrier) always win; otherwise `min` over `src→X→dst` pairs;
   tuple comparison `(cost, path)` gives the lexicographic tie-break for free. `src==dst → 0`.
3. Dijkstra with heap entries `(cost, legs, path)` and a done-set — the tuple order is the
   documented tie-break (cost, fewer legs, lexicographic path). `main()` builds the adjacency
   once for all queries (`_adj` accepts a prebuilt dict) — without that, 20k queries × 600 legs
   blew the 2 s budget.
4. Matrix: normalise list/dict entry forms into `product → bands`, sum duplicate products in the
   order, `qty × cost`; `ValueError` for unknown country/product and negative quantity.
5. `price_quantity(bands, qty, mode)`: volume = find the band containing `qty` (inclusive `max`);
   graduated = walk the bands, `units = min(qty, max) − min + 1`, flat bands once; `qty == 0 → 0`.

## Pitfalls hidden tests target
- treating legs as undirected; Part 1 returning a leg with the wrong carrier; preferring a
  cheaper transfer over a direct leg in Part 2; `src == dst` (0, not a loop / not −1)
- inclusive band upper bounds (qty 5 with `1-5` is still the first band; 6 starts the second)
- Stripe-doc numbers: graduated 6 → 4150 (5×700 + 650) vs volume 6 → 3900 (6×650)
- flat band charged once, not per unit; quantity 0 must not charge a flat band
- same product twice in an order must be merged before tiering (3+3 ≠ 2×price(3))
- unknown country / product error path (phone-screen rubric explicitly grades it)

## Reconstructed rules / conflicts
- Merging duplicate products before tiering and the `ValueError` messages are reconstructions.
- Sources describe matrix Part 3 as "`incremental` vs `fixed` per tier"; this is exposed as
  `mode="graduated"` with `flat` bands, and `mode="volume"` covers the "whole quantity at the
  tier price" reading (1point3acres "0–2 件 1000c，3+ 900c"). Both modes are tested.

## Complexity & measured cost
Part 3 O(Q · E log V); matrix O(items + bands).
Measured: 0.10 s / 54 MB (1 000 orders × 100 items, graduated) and 0.90 s / 21 MB (600 legs, 20 000
Dijkstra queries) — perf test budget 2 s / 256 MB.

## Test inventory
22 tests — part1: 3 · part2: 5 · part3: 3 · part4: 4 · part5: 7; edge 12 · fmt 1 · io 2 · perf 1.
(`PART 5` covers both tier modes via `MODE volume|graduated`, so the five pytest part markers suffice.)

## Skills exercised
S02 parsing · S03 records + dict by (src,dst) · S06 integer cents · S07 graduated vs volume tiers · S08 tie-breaks · S13 inclusive bands · S18 validation paths · S19 incremental design · A03 shortest path
