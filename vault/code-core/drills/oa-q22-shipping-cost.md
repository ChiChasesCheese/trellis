---
nodes: [algorithms.shortest-path, rules.tiers, transfer.stripe-oa]
tags: [stripe-oa, q22]
---
# Drill: price shipping over a carrier network, then over a tiered price list

Sixty minutes, five parts, two unrelated problems sharing the same title (the stdin
protocol picks one with `PART n`). Parts 1-3: a table of directed `origin:destination:
carrier:cost` legs; find the shipping cost from A to B — first restricted to a named
carrier with no transfer, then allowing exactly one transfer (any carrier), then the
cheapest route over any number of legs. Parts 4-5: a per-country, per-product price list;
price an order item by item, then introduce Stripe-Billing-style quantity tiers with two
distinct pricing modes.

- Part 1: exact directed leg with a named carrier, or `-1`.
- Part 2: cheapest route with at most one transfer; a direct leg always wins over a cheaper
  multi-leg route.
- Part 3: cheapest route over any number of legs (Dijkstra), reporting cost and path.
- Part 4: sum `quantity x unit price` per item from a country/product matrix, with a defined
  error path for unknown countries and products.
- Part 5: quantity tiers, in `volume` mode (whole quantity priced at one band) and
  `graduated` mode (each band priced on its own units).

**Constraints to state and honor**
- Legs are directed; a duplicate `(src, dst, carrier)` keeps the cheaper one; up to ~100
  legs and 10^5 route queries.
- `src == dst` is always cost `0`, never a loop through the graph.
- Tier bands are contiguous closed intervals starting at 1, `max = None` meaning open-ended;
  a flat-amount band charges once regardless of how many units land in it.
- All money is integer cents throughout.

**Grading points**
- Part 2's "direct always wins" rule stated before coding it — a candidate who reaches for
  a general shortest-path routine here will produce a wrong answer on the worked example
  where a two-leg route is cheaper than the direct leg.
- Part 3 is plain Dijkstra with a documented tie-break: fewer legs, then the
  lexicographically smallest alternating path — and the adjacency list built once and
  reused across all queries, not per query.
- Volume vs graduated is the crux of Part 5: volume prices the *entire* quantity at the
  band it falls in; graduated prices each band's own units separately, and a candidate
  should be able to reproduce Stripe's own doc example (6 units: graduated 4150, volume
  3900) from memory of the rule, not the number.
- A flat band is charged once no matter how many units fall inside it, and a quantity of
  zero costs nothing in either mode.
- Unknown country, unknown product, and negative quantity are distinct, named errors — not
  a single generic failure.
- Duplicate products within one order are summed before tiering, so pricing 3 then 3 more
  of the same item is not double-priced against a per-call tier boundary.

**Source**
- The full statement, solution notes and report: `vault/stripe/q22_shipping_cost/question.md`,
  `vault/stripe/q22_shipping_cost/solution.md`,
  `vault/Quick_Check/problems/q22_shipping_cost/problem.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
