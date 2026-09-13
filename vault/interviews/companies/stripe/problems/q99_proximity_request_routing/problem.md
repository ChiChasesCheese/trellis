# q99 · Proximity Request Routing

**Type:** bespoke multi-part OA · **Stage:** stdin/stdout coding assessment · **Confidence:**
high for Parts 1–3 because the supplied screenshots contain the commands, rules, and examples

## Context

A global payment platform has datacenters in multiple geographic regions. The router must keep
their registration and health state, calculate great-circle distance, and send each request to
the nearest healthy datacenter that still has capacity.

This is an in-memory command processor. It is not asking for a real distributed routing service,
network protocol, database, spatial index, or concurrency design.

## Relationship to q17

This is the same problem family as `q17_datacenter_router_haversine`, but it is not a drop-in
duplicate. The supplied q99 screenshot has a stricter, different interface:

| Contract | q99 | q17 reconstruction |
| --- | --- | --- |
| Health command | `SET_HEALTHY` | `SET_HEALTHZ` |
| Attempted order | comma-separated | space-separated |
| Exhausted route | `NONE <order>` | `NONE 0 <order>` |
| Parts | 1–3 | reconstructed Part 4 `RELEASE` |

q99 follows its screenshot and does not inherit q17's alternate syntax or reconstructed part.

## Cumulative milestone files

Every `main()` is stage-agnostic: it creates one `Router`, reads commands sequentially, and calls
`router.handle(line)`. The command table inside that milestone determines which commands exist.
For step-by-step study, use the standalone milestone files:

- `milestone_part1.py`: complete runnable code after Part 1; later commands return `ERROR`.
- `milestone_part2.py`: a complete copy of Part 1 plus distance calculation; `ROUTE` still returns
  `ERROR`.
- `milestone_part3.py`: a complete copy of Parts 1–2 plus routing, equivalent to the final stage.

Each file intentionally repeats the previous milestone instead of importing it. That duplication
makes the exact code added by each newly unlocked part visible and keeps every milestone runnable
by itself.

## Input

Read commands from stdin, one command per line. State persists for the entire input stream. Blank
lines are ignored.

```text
REGISTER <name> <latitude> <longitude> <capacity>
SET_HEALTHY <name> <true|false>
DISTANCE <latitude1> <longitude1> <latitude2> <longitude2>
ROUTE <latitude> <longitude>
```

All numeric tokens are integers. Command names and boolean tokens are case-sensitive. Defensive
parser behavior used by this implementation: wrong arity, a non-integer numeric field, an unknown
command, or any other malformed command returns `ERROR` and does not mutate state.

## Output

Emit exactly one line for every non-blank command, in input order.

- Successful state-changing commands return `OK`; rejected commands return bare `ERROR`.
- `DISTANCE` returns one integer number of kilometers.
- A successful route returns `<selected_name> <distance_km> <attempted_order>`.
- If no healthy datacenter has capacity, return `NONE <attempted_order>`.
- If there are no healthy datacenters, return bare `NONE`.
- `attempted_order` is comma-separated with no spaces, for example `dc1,dc2,dc3`.
- Boolean values in input are lowercase `true` or `false`.

## Part 1 — Datacenter registry and health

### `REGISTER <name> <latitude> <longitude> <capacity>`

Register a new datacenter and return `OK` only when all rules hold:

- `name` has not already been registered;
- latitude is in the inclusive range `[-90, 90]`;
- longitude is in the inclusive range `[-180, 180]`;
- capacity is greater than zero.

A newly registered datacenter starts with `healthy = true` and `load = 0`. A failed registration
does not overwrite or partially create anything.

### `SET_HEALTHY <name> <true|false>`

Change the health of an existing datacenter and return `OK`. Return `ERROR` for an unknown name or
an invalid boolean token. Changing health never resets load.

### Screenshot example

```text
Input:                                  Output:
REGISTER us-west 38 -122 100            OK
REGISTER us-east 41 -74 150             OK
REGISTER eu-west 52 0 200               OK
SET_HEALTHY us-east false               OK
REGISTER us-west 50 -100 50             ERROR
REGISTER invalid 91 0 100               ERROR
REGISTER invalid2 0 0 0                 ERROR
```

## Part 2 — Distance calculation

`DISTANCE lat1 lon1 lat2 lon2` calculates great-circle distance with the Haversine formula and
Earth radius `6371 km`:

```text
lat1_radians = lat1 * pi / 180
lat2_radians = lat2 * pi / 180
delta_lat = (lat2 - lat1) * pi / 180
delta_lon = (lon2 - lon1) * pi / 180

a = sin(delta_lat / 2)^2
    + cos(lat1_radians) * cos(lat2_radians) * sin(delta_lon / 2)^2
c = 2 * atan2(sqrt(a), sqrt(1 - a))
distance = 6371 * c
```

Clamp `a` into `[0, 1]` before taking square roots because floating-point arithmetic can produce a
value just outside the mathematical range near antipodal points. Return `floor(distance + 0.5)`,
so a non-negative exact half rounds upward. This is the selected q99 rounding contract; the
screenshot says only “round the value.”

Per the confirmed scope, `DISTANCE` requires integer tokens but does not apply the registration
coordinate-range validation.

### Screenshot example

```text
Input:                                  Output:
DISTANCE 0 0 0 0                        0
DISTANCE 38 -122 41 -74                 4080
DISTANCE 0 0 10 0                       1112
DISTANCE 36 140 -33 -71                 17167
```

## Part 3 — Geographic routing with capacity

`ROUTE latitude longitude` processes one request:

1. Consider every healthy datacenter, including healthy datacenters already at capacity.
2. Calculate each raw, unrounded Haversine distance from the request.
3. Sort by `(raw_distance ascending, name ascending)`.
4. Save the names of that entire sorted list as `attempted_order`.
5. Select the first datacenter with `load < capacity`.
6. Increment only the selected datacenter's load by one.
7. Print the selected name, its rounded display distance, and `attempted_order`.

If every healthy datacenter is full, return `NONE <attempted_order>` without changing state.
Unhealthy datacenters are not selected and do not appear in `attempted_order`. Load persists across
multiple `ROUTE` commands and health changes.

Per the confirmed scope, `ROUTE` requires integer tokens but does not apply the registration
coordinate-range validation.

### Screenshot example

```text
Input:                                  Output:
REGISTER us-west 38 -122 2              OK
REGISTER us-east 41 -74 100             OK
ROUTE 38 -122                           us-west 0 us-west,us-east
ROUTE 38 -122                           us-west 0 us-west,us-east
ROUTE 38 -122                           us-east 4080 us-west,us-east
```

## Edge cases

- Duplicate registration returns `ERROR` and preserves the original coordinates and capacity.
- Coordinate boundaries are inclusive for `REGISTER`; capacity zero and negative capacity fail.
- Repeating the same valid health value is still `OK`; health changes preserve load.
- Identical points have distance zero; antipodal inputs must not trigger a square-root error.
- Equal raw distances use alphabetical name order, not registration order.
- Two different raw distances can round to the same displayed integer; raw distance still wins.
- A healthy-but-full datacenter remains in `attempted_order`; an unhealthy one does not.
- A malformed `ROUTE` never consumes capacity.
- No registered or no healthy datacenters returns `NONE` without trailing whitespace.

## Complexity

Let `D` be registered datacenters and `H` healthy datacenters.

- `REGISTER` and `SET_HEALTHY`: expected `O(1)` time.
- `DISTANCE`: `O(1)` time.
- `ROUTE`: `O(H log H)` time and `O(H)` temporary space.
- Persistent registry: `O(D)` space.

The full sorted attempted order is required output, so `O(H)` output and sorting are part of the
problem contract. A heap, k-d tree, geohash, or distributed routing abstraction adds complexity
without solving that output requirement.

## Related problems and sources

The screenshots are authoritative for this implementation. Public pages for the exact challenge
are third-party reconstructions and may disagree with the screenshot:

- [FastPrep reconstruction](https://www.fastprep.io/problems/stripe-request-routing-system)
- [1Point3Acres reconstruction](https://www.1point3acres.com/interview/problems/995dee64-8b12-588f-a8ec-0b6998b518bb)

Useful official analogies, not the same problem:

- [LeetCode 1603 — Design Parking System](https://leetcode.com/problems/design-parking-system/):
  successful allocation consumes persistent capacity.
- [LeetCode 1847 — Closest Room](https://leetcode.com/problems/closest-room/): filter candidates,
  minimize distance, and apply a deterministic tie-break.
- [LeetCode 2353 — Design a Food Rating System](https://leetcode.com/problems/design-a-food-rating-system/):
  mutable entity state with lexicographic tie-breaking.
- [HackerRank — Simple Text Editor](https://www.hackerrank.com/challenges/simple-text-editor/problem):
  one-command-per-line parsing with state across the stream.
- [NASA WorldWind Haversine implementation](https://worldwind.arc.nasa.gov/autodocs/WebWorldWind/geom_Location.js.html):
  spherical great-circle calculation.
- [HashiCorp Consul prepared queries](https://developer.hashicorp.com/consul/api-docs/query):
  a production analogy for health filtering and nearest-first routing.

## What this tests

Skills: S01 read the whole spec · S02 parsing and typed fields · S03 state transitions · S08
deterministic tie-breaks · S09 exact output · S18 validation and atomic errors · S19 incremental
design · S21 Python standard library math.
