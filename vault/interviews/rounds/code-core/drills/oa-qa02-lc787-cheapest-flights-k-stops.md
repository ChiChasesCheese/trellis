---
nodes: [algorithms.shortest-path]
tags: [stripe-oa, qa02, leetcode]
---
# Drill: cheapest flight within k stops, two ways, then the itinerary and carrier filters

Forty-five minutes, stdin to stdout. This is LeetCode 787, Cheapest Flights
Within K Stops: given a directed weighted graph of flights, a source, a
destination and a maximum number of intermediate stops, find the cheapest
total price, returning -1 if none exists. Part 1 solves it with Bellman-Ford
run for exactly `k+1` rounds. Part 2 solves the identical problem by
expanding a frontier one hop at a time and must agree with Part 1 on every
input. Part 3 returns the actual sequence of cities of a cheapest itinerary,
with a deterministic tie-break. Part 4 restates the routes as carrier-tagged
strings and adds an optional filter to only one carrier's flights, echoing
Stripe's own shipping-route problem.

**Constraints to state and honor**
- Up to `n` cities and one directed weighted edge per ordered city pair; `k`
  intermediate stops means at most `k+1` flights.
- `src == dst` returns 0 immediately; no path within the hop budget returns
  -1.
- Part 4's routes are strings `FROM:TO:CARRIER:price`; a named carrier
  restricts which edges may be used, `*` allows any mix, and an unknown city
  or carrier returns -1.
- Part 2 must match Part 1 exactly on every input, including graphs with
  cycles.
- Part 3's tie-break among equal-cost itineraries is fewer flights first,
  then the lexicographically smallest list of city ids.

**Grading points**
- Each Bellman-Ford round must relax from a copy of the previous round's
  distances, not update in place — say out loud that updating in place lets
  one round silently cross several flights and breaks the hop bound, and
  verify it against the worked example that relies on it.
- Explain why plain Dijkstra is wrong here: its greedy invariant assumes the
  first-popped cost is final, but a cheaper route can need too many stops to
  be usable within `k`.
- Part 2's frontier pruning compares against the best cost ever seen for a
  city, not just the current layer's cost, or it can re-expand dominated
  states.
- Cycles in the graph must never help — a solution that doesn't explicitly
  guard against looping through one should be tested against a graph that
  has one.
- Part 3's tie-break is two-level and order-independent of how edges were
  listed in the input — carrying `(cost, hop count, path)` through the same
  layered search gets it for free.

**Source**
- `vault/interviews/companies/stripe/problems/qA02_lc787_cheapest_flights_k_stops/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/qA02_lc787_cheapest_flights_k_stops.md`, `vault/interviews/companies/stripe/problems/qA02_lc787_cheapest_flights_k_stops/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
