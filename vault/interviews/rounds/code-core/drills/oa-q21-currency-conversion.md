---
nodes: [algorithms.shortest-path, rules.rounding, transfer.stripe-oa]
tags: [stripe-oa, q21]
---
# Drill: convert between currencies through direct, inverse and best multi-hop rates

Sixty minutes, four parts, stdin to stdout. A comma-separated rate string gives directed
`FROM:TO:RATE` quotes. Part 1 answers direct-quote conversion queries only. Part 2 also
accepts the inverse of the opposite quote when the direct one is missing. Part 3 builds the
full graph and answers with the rate of the *best* — not the shortest, not the first —
simple path between two currencies, along with that path. Part 4 applies the Part 3 rate to
a batch of payout amounts, rounded to cents.

**Constraints to state and honor**
- Currency codes are case-sensitive; a duplicate ordered quote means the last one wins; a
  rate that is zero, negative, or non-numeric makes the whole input invalid.
- Up to ~50 currencies, ~100 quotes, up to 10^5 queries.
- `src == dst` always converts at exactly `1.0`, even for a currency absent from the table.
- Parts 1-3 print a rate formatted to at most 6 decimals with trailing zeros trimmed, or
  `N/A`; Part 4 prints an amount rounded half-up to the cent, or `N/A`.

**Grading points**
- Part 1 never uses the inverse, and Part 2's direct quote always wins over the inverse of
  the opposite quote even when both exist and disagree — say this ordering out loud before
  writing either function.
- Part 3's "best" is the maximum product of edge rates over *simple* paths (each currency
  visited at most once) — a longer path can beat a shorter one, and allowing cycles would
  let an inconsistent pair of quotes create unbounded arbitrage.
- `find_path` (shortest, any path, BFS) and `best_conversion` (maximum product, DFS over
  simple paths) are different functions answering different questions — conflating them is
  the most common mistake.
- Part 4 recomputes the chosen path's product in `Decimal`, not by reusing the float rate
  from Part 3 — float noise on the six-hundredths place changes which way half-up rounds.
- Best rates cached per `(from, to)` pair so a batch of 10^5 payouts doesn't re-search the
  graph per line.
- Disconnected currencies and unknown currencies both resolve to `N/A`/`None`, never an
  exception, once past the initial rate-string validation.

**Source**
- The full statement, solution notes and report: `vault/interviews/companies/stripe/problems/q21_currency_conversion/problem.md`,
  `vault/interviews/companies/stripe/study/10-solutions/q21_currency_conversion.md`,
  `vault/interviews/companies/stripe/problems/q21_currency_conversion/problem.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
