---
nodes: [input.malformed, output.ordering, transfer.stripe-oa]
tags: [stripe-oa, q17]
---
# Drill: register datacenters and route requests to the nearest healthy one

Sixty minutes, one command processor, no `PART` line — rules accumulate as you go.
Commands: `REGISTER region lat lon capacity`, `SET_HEALTHZ region true|false`,
`DISTANCE lat1 lon1 lat2 lon2`, `ROUTE lat lon`, and `RELEASE region`. `REGISTER`
succeeds only for a new region with in-range coordinates and positive capacity;
anything invalid — bad arity, non-integer tokens, an unknown command, an already-used
region name — prints `ERROR` and must not touch state at all. `DISTANCE` reports the
Haversine great-circle distance rounded half-up to the nearest kilometer. `ROUTE` ranks
every healthy region by unrounded distance (ties by name), routes to the first one with
spare capacity, consumes one unit of that capacity, and reports the chosen region plus
the full ranked candidate list — `NONE 0` plus the (still-listed) candidates when nothing
has room. `RELEASE` frees one unit of capacity.

**Constraints to state and honor**
- Coordinate bounds are inclusive: latitude in `[-90, 90]`, longitude in `[-180, 180]`;
  capacity must be strictly positive.
- Haversine uses R = 6371 km; the printed distance is `floor(d + 0.5)`, never Python's
  `round()`, which breaks ties to even.
- An unhealthy region is invisible to `ROUTE` entirely — not listed as a candidate, not
  routable — but keeps its accumulated load across health flips.
- Up to 10^5 commands total; every command produces exactly one output line.

**Grading points**
- Validation runs to completion before any state changes — a candidate should describe
  this as "commit only after every check passes," since a failed `REGISTER` must leave
  an existing region's coordinates and capacity untouched.
- Distance has two separate roles that must not be conflated: the unrounded value drives
  candidate ranking and the capacity check, while the rounded value is only ever a
  display detail computed at the very last step.
- A healthy-but-full region still appears in the candidate list under `NONE 0`; only
  unhealthy regions disappear from it.
- Capacity boundary tested directly: the `capacity`-th `ROUTE` to a region succeeds, the
  next one does not, and `RELEASE` cannot take a region below zero load.
- Tie-break by region name when two candidates are equidistant, using the exact
  (unrounded) distance for the comparison even when both round to the same displayed
  kilometer count.
- `DISTANCE` performs no range validation on its coordinates and needs no registered
  regions — it is a pure function, unlike every other command here.

**Source**
- `vault/interviews/companies/stripe/problems/q17_datacenter_router_haversine/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q17_datacenter_router_haversine.md`
- `vault/interviews/companies/stripe/problems/q17_datacenter_router_haversine/problem.md`, `vault/interviews/companies/stripe/problems/q17_datacenter_router_haversine/REPORT.md`
- `vault/interviews/companies/stripe/study/10-solutions/q17_datacenter_router_haversine.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
