# q99 Proximity Request Routing — report

## Summary

This is a sequential command processor with one mutable registry. Each datacenter has a unique
name, integer coordinates, a fixed positive capacity, mutable health, and mutable load. `ROUTE`
ranks every healthy datacenter by unrounded Haversine distance and then name, selects the first
one with `load < capacity`, and increments only that datacenter's load.

The clean solution is an in-memory simulation, not a distributed-systems implementation and not
a spatial-index problem. Because every `ROUTE` must emit the complete distance-sorted list of
healthy datacenters, it already has an output-size lower bound of O(H), where H is the number of
healthy datacenters.

## Source assessment

### Direct source for this implementation

- The two prompt screenshots supplied with this task are authoritative for command names,
  validation, output spelling, and Part 1–3 behavior. In particular, the screenshot spells the
  exhausted result as uppercase `NONE`.
- The UK Department for Transport's GPS technical report gives the same Haversine equation,
  describes it as great-circle distance on a sphere, and uses `R = 6,371 km`:
  https://assets.publishing.service.gov.uk/media/5a7c710f40f0b62aff6c1b14/Processing_of_NTS_GPS_Pilot_Data_a_technical_report.pdf
- NASA WorldWind's reference implementation converts degrees to radians and evaluates the same
  half-angle formula for great-circle angular distance. It is explicitly a spherical model:
  https://worldwind.arc.nasa.gov/autodocs/WebWorldWind/geom_Location.js.html
- Python's official docs define `math.radians`, `math.atan2`, and `round`. `round(x)` returns the
  nearest integer but uses ties-to-even when the value is exactly halfway:
  https://docs.python.org/3/library/math.html#math.radians
  https://docs.python.org/3/library/math.html#math.atan2
  https://docs.python.org/3/library/functions.html#round
- JPL lists Earth's mean radius as `6371.0084 km`. That is useful scientific context, but the judge
  requires the prompt's exact constant `6371`, so substituting the more precise value would be a
  correctness bug:
  https://ssd.jpl.nasa.gov/planets/phys_par.html

### Same-problem clues, not authoritative sources

- FastPrep publishes a near-verbatim third-party reconstruction:
  https://www.fastprep.io/problems/stripe-request-routing-system
- 1Point3Acres publishes another third-party reconstruction:
  https://www.1point3acres.com/interview/problems/995dee64-8b12-588f-a8ec-0b6998b518bb

These pages are useful only for discovery. They are not official Stripe or HackerRank statements,
and no public official HackerRank URL for this exact challenge was found. They also conflict with
the screenshot: FastPrep prints `None`, while the screenshot requires `NONE`; one reconstruction
claims half-up rounding, while the screenshot only says to round. Neither page may override the
provided prompt.

## Model

```text
Datacenter
  latitude: int
  longitude: int
  capacity: int
  healthy: bool = true
  load: int = 0

Router
  datacenters: dict[name, Datacenter]
```

The dictionary owns the datacenter objects for the full command stream. Commands execute in input
order. A failed command must not partially mutate registry, health, or load.

## Approach by part

### Part 1 — registry and health

`REGISTER name latitude longitude capacity` parses all numeric fields first, validates latitude in
`[-90, 90]`, longitude in `[-180, 180]`, `capacity > 0`, and name uniqueness, then inserts exactly
one datacenter with `healthy = true` and `load = 0`. Return `OK`; otherwise return bare `ERROR`.

`SET_HEALTHY name true|false` performs an O(1) name lookup and changes only `healthy`. Health
changes do not reset load. Reject an unknown name and, defensively, any boolean token other than
the exact lowercase values `true` and `false`.

The prompt does not fully specify malformed lines, wrong arity, non-integer fields, or unknown
commands. Treating all of them as `ERROR` is the safest command-processor behavior, but it should
be documented as defensive handling rather than a sourced rule.

### Part 2 — Haversine distance

For coordinates `(lat1, lon1)` and `(lat2, lon2)`, convert angles to radians and compute:

```text
dlat = radians(lat2 - lat1)
dlon = radians(lon2 - lon1)
a = sin(dlat / 2)^2
    + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)^2
a = min(1.0, max(0.0, a))
c = 2 * atan2(sqrt(a), sqrt(1 - a))
distance_km = 6371 * c
```

`DISTANCE` parses four integers. Per the confirmed q99 scope, it does not apply registration's
latitude/longitude range validation. Malformed arguments or non-integer values return `ERROR`.

The clamp is necessary even for legal integer coordinates: CPython double precision produces
`a = 1.0000000000000002` for antipodal `(-82, -180)` and `(82, 0)`, which otherwise makes
`sqrt(1 - a)` fail. Longitude deltas need no separate wrap because the squared half-angle sine is
periodic.

Keep two representations: raw float distance for ranking and rounded integer distance for output.
The screenshot's examples evaluate to `0`, `4080`, `1112`, and `17167`. The prompt does not define
the exact `.5` tie rule. The selected q99 contract uses `floor(distance + 0.5)` for non-negative
distances. Python's built-in `round` uses ties-to-even, so it is intentionally not used here.

### Part 3 — routing with capacity

For each `ROUTE latitude longitude`:

1. Parse both request coordinates as integers before doing any work; malformed input returns
   `ERROR` and changes no load. Per the confirmed scope, no coordinate-range check is applied.
2. Build `(raw_distance, name, datacenter)` tuples for all and only healthy datacenters.
3. Sort by the explicit tuple key `(raw_distance, name)`. Sort stability alone is insufficient:
   preserving registration order on a distance tie would violate alphabetical tie-breaking.
4. Build `attempted_order` from the entire sorted healthy list. Healthy datacenters already at
   capacity remain in this list.
5. Scan in sorted order and choose the first datacenter with `load < capacity`.
6. On success, increment its load exactly once and emit
   `<name> <rounded_selected_distance> <attempted_order>`.
7. If every healthy datacenter is full, emit `NONE <attempted_order>` and mutate nothing.

There is a real wording ambiguity: Part 2 exposes an integer distance and Part 3 says all values
are integers, which could suggest sorting by rounded distance. The selected q99 contract resolves
this explicitly: rank by unrounded Haversine distance, use the name only for a true distance tie,
and round only the selected distance shown in output. For request `(37,-122)`,
datacenter `z-near` at `(36,-116)` is about `547.6122 km`, while `a-far` at `(40,-127)` is about
`548.1130 km`; both display as `548`. Sorting displayed integers would incorrectly choose
`a-far` by name.

Do not introduce a heap, k-d tree, geohash, cache, or strategy hierarchy. Request coordinates can
change every time, health and load mutate, and the required full ordered output still has to be
constructed.

## Related official problems and systems

These are algorithm or modeling analogies, not the same problem:

| Source | What it supports | Important mismatch |
| --- | --- | --- |
| LeetCode 1847, Closest Room: https://leetcode.com/problems/closest-room/ | Filter candidates by a capacity-like threshold, minimize distance, then apply a deterministic tie-break. | Static offline queries; its distance is ID difference and it does not consume capacity. |
| LeetCode 1603, Design Parking System: https://leetcode.com/problems/design-parking-system/ | Capacity is mutable state across calls; a successful allocation consumes one slot and later calls can fail. | No geography, health, or ranked fallback. |
| LeetCode 2353, Design a Food Rating System: https://leetcode.com/problems/design-a-food-rating-system/ | Mutable per-entity state and lexicographic tie-breaking under repeated queries. | No capacity or distance. |
| LeetCode 1912, Design Movie Rental System: https://leetcode.com/problems/design-movie-rental-system/ | Multi-command state transitions and explicit multi-field ordering. | Its availability transitions and ranking fields differ. |
| HackerRank, Simple Text Editor: https://www.hackerrank.com/challenges/simple-text-editor/problem | Parse one command per line and preserve state across the whole stream. | Text editing and undo, not routing. |
| HashiCorp Consul prepared queries: https://developer.hashicorp.com/consul/api-docs/query | Official production analogue: `OnlyPassing` filters health and `Near` returns nearest instances first. | Uses estimated network coordinates/RTT and has no per-request capacity decrement. |
| IETF ALTO/CDN Internet-Draft: https://datatracker.ietf.org/doc/html/draft-penno-alto-cdn-03 | Describes proximity routing to closest CDN nodes and says health, load, cache utilization, and CPU status should inform request routing. | Expired Internet-Draft, conceptual architecture, not this coding challenge or an implementation spec. |

## Pitfalls hidden tests should target

- Inclusive coordinate boundaries: latitudes `-90/90`, longitudes `-180/180`; reject one beyond.
- Duplicate registration is atomic; failed registration does not overwrite the original object.
- Capacity `0` and negative capacity fail; load starts at zero only on successful registration.
- Unknown datacenter and invalid boolean for `SET_HEALTHY`; toggling health preserves load.
- Same point, same meridian, International Date Line, poles, and antipodal Haversine inputs.
- Clamp `a` before both square roots; use `6371`, not `6371.0084` or another Earth model.
- Alphabetical tie with identical coordinates; do not rely on dictionary insertion order.
- Raw-distance ordering when two different raw distances round to the same integer.
- Nearest full datacenter falls through to the next candidate; successful route increments once.
- Unhealthy datacenters are absent from attempted order; healthy-but-full datacenters are present.
- All healthy datacenters full; no healthy datacenters; failed route leaves all loads unchanged.
- Exact formatting: `OK`, `ERROR`, lowercase booleans in input, comma-separated names with no
  spaces, uppercase `NONE`, and one output line per command.
- Empty attempted order leaves a minor prompt ambiguity about a trailing space. Prefer emitting
  `NONE` with no trailing whitespace unless the repository's I/O contract explicitly requires the
  empty third field.

## Complexity

- `REGISTER`: expected O(1) time, O(1) additional space.
- `SET_HEALTHY`: expected O(1) time, O(1) space.
- `DISTANCE`: O(1) time and space.
- `ROUTE`: O(H log H) time and O(H) temporary space for H healthy datacenters.
- Persistent registry: O(D) space for D registered datacenters.

The command requires the complete sorted attempted order, so O(H) output is unavoidable. Without
that field, linear selection or a spatial index could become relevant; adding either here would be
premature and would not remove the required sort.

## Test inventory

28 tests — Part 1: 7 · Part 2: 8 · Part 3: 13 · edge cases: 16 · formatting: 1 ·
stdin/stdout: 2 · performance: 1. Markers overlap.

Three additional milestone tests execute each milestone's `main()` and prove that Part 1 rejects
Part 2 commands, Part 2 rejects Part 3 commands, and Part 3 exposes the complete cumulative API.
The final solution has a separate structural regression test proving that legacy `handle_partN`
and `partN` entry points cannot reappear alongside the single dynamic dispatch path.

The performance case, strengthened after comparison with an independent implementation, runs
100,050 mixed commands against 50 datacenters: 100,000 deterministic `ROUTE`, `DISTANCE`, and
`SET_HEALTHY` commands after registration. Measured locally on 2026-08-30: 1.140 seconds and
48.0 MB peak RSS, below the 2-second / 256-MB test budget.

## Skills exercised

S01 read the whole spec · S02 parsing and typed fields · S03 state transitions · S08 deterministic
tie-breaks · S09 exact output · S18 validation and atomic errors · S19 incremental design · S21
Python standard library math.
