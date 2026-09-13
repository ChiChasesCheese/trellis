# q17 · Datacenter Request Router — registry, health, Haversine distance, proximity routing

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, stdin/stdout from scratch) · **Last asked:** 2026-08-19 (LeetCode post, SSE3); 2026-08-11 (1point3acres "L3 SWE OA")
**Frequency:** 4 independent sources (LeetCode 8470971 verbatim, PracHub full spec, 1point3acres 题库, InterviewDB "Proximity Request Routing") · **Confidence:** high (command set + samples verbatim; two samples conflict, see Variants)

## Context
Stripe runs API regions in several datacenters. A request from a client at a known latitude /
longitude must be routed to the nearest datacenter that is *healthy* and still has *capacity*.
Regions get registered and taken in and out of service (health checks) while requests keep
arriving. You build the command processor that keeps the registry and answers `ROUTE`.

## Input (stdin)
One command per line, space-separated tokens. Blank lines are ignored. Rules accumulate —
the same program handles every part, there is **no `PART n` line**. Up to 10^5 commands.

```
REGISTER <region> <lat> <lon> <capacity>
SET_HEALTHZ <region> <true|false>
DISTANCE <lat1> <lon1> <lat2> <lon2>
ROUTE <lat> <lon>
RELEASE <region>                      (Part 4, reconstructed)
```
`lat`, `lon`, `capacity` are **integers** (a non-integer token is an `ERROR`; see Variants for a
float-tolerant flag). `<true|false>` is case-insensitive.

## Output
Exactly one line per command, in input order:
* `OK` / `ERROR` for `REGISTER`, `SET_HEALTHZ`, `RELEASE`
* an integer number of km for `DISTANCE`
* `<region> <distance> <candidate1> <candidate2> ...` for `ROUTE` (see Part 3), or
  `NONE 0 <candidates...>` when nothing is routable
* `ERROR` for an unknown command or wrong arity / bad types. **An invalid command never
  mutates state.**

## Rules
### Part 1 — registry and health
* `REGISTER region lat lon capacity` → `OK` if the region does **not** exist yet, `lat ∈ [-90, 90]`,
  `lon ∈ [-180, 180]`, `capacity > 0`; otherwise `ERROR`. A new region is **healthy** with
  load 0.
* `SET_HEALTHZ region true|false` → `OK` if the region exists, else `ERROR`. Setting the same
  state twice is still `OK`. Health does not touch load.

### Part 2 — great-circle distance
`DISTANCE lat1 lon1 lat2 lon2` → Haversine distance with **R = 6371 km**:
```
a = sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2)      (φ, λ in radians)
d = 2 · R · asin(√a)
```
printed **rounded to the nearest integer, half-up** (`floor(d + 0.5)`). `DISTANCE` does not
range-check its coordinates (only type/arity); it needs no registered regions.

### Part 3 — proximity routing
`ROUTE lat lon`:
* **candidates** = every *healthy* region (even one that is at full capacity), ranked by
  **unrounded distance ascending, ties by region name ascending**;
* **chosen** = the first candidate with `load < capacity`; routing **consumes 1 unit of load**
  of the chosen region;
* output `<chosen> <rounded distance to chosen> <candidates in ranked order>`;
* if no candidate has spare capacity (or there are no healthy regions): `NONE 0 <candidates...>`
  (`NONE 0` alone when there are no healthy regions) and nothing changes.

Unhealthy regions are neither routable nor listed. Load survives health flips: a region that
goes `false` then `true` keeps its load.

### Part 4 — releasing capacity (reconstructed — the 1point3acres/InterviewDB titles mention
"capacity management"; the exact command is not in the sources)
`RELEASE region` → `OK` and `load -= 1` if the region exists **and** `load > 0`; `ERROR`
otherwise (unknown region, or load already 0). Works on unhealthy regions too.

## Worked examples
Example 1 (LeetCode post, Part 1):
```
REGISTER us-east-1 38 120 100   -> OK
REGISTER us-west-2 50 112 30    -> OK
SET_HEALTHZ us-west-2 false     -> OK
REGISTER eu-east-1 -10 15 0     -> ERROR      (capacity must be > 0)
```
Example 2 (PracHub, Parts 1–3; distance (41,-73)→(34,-118) = 4000.08 km):
```
REGISTER east 40 -74 10         -> OK
REGISTER west 34 -118 20        -> OK
SET_HEALTHZ east false          -> OK
ROUTE 41 -73                    -> west 4000 west
```
Example 3 (capacity is consumed; ties by name):
```
REGISTER us-east-1 0 0 1        -> OK
REGISTER ap-south-1 0 0 1       -> OK
ROUTE 0 0                       -> ap-south-1 0 ap-south-1 us-east-1
ROUTE 0 0                       -> us-east-1 0 ap-south-1 us-east-1
ROUTE 0 0                       -> NONE 0 ap-south-1 us-east-1
SET_HEALTHZ ap-south-1 false    -> OK
ROUTE 0 0                       -> NONE 0 us-east-1
RELEASE us-east-1               -> OK
ROUTE 0 0                       -> us-east-1 0 us-east-1
```
Example 4 (distances):
```
DISTANCE 0 0 0 0                -> 0
DISTANCE 0 0 0 180              -> 20015      (antipodes, 20015.09 km)
DISTANCE 0 0 1 0                -> 111        (one degree of latitude = 111.19 km)
DISTANCE 0 0 0 90               -> 10008      (10007.54 km)
DISTANCE 38 120 50 112          -> 1478       (1477.80 km)
```

## Edge cases hidden tests are known to target
- `REGISTER` of an existing region → `ERROR` and the original coordinates/capacity stay
- boundary coordinates: `90`, `-90`, `180`, `-180` are valid; `91`, `-181` are not; capacity `0`
  and negative are invalid
- wrong arity (`REGISTER a 1 2`, `ROUTE 1`), non-integer tokens (`1.5`, `abc`), unknown command
  → `ERROR`, no state change
- `SET_HEALTHZ` on an unknown region → `ERROR`; boolean must be `true`/`false` (any case)
- `ROUTE` with no regions at all → `NONE 0`; all unhealthy → `NONE 0`; healthy but full → `NONE 0`
  followed by the full regions as candidates
- ties at equal distance → alphabetical; ranking uses the **unrounded** distance (two regions
  that both round to 4000 are still ordered by the exact value)
- rounding: `x.5` rounds up (`floor(d + 0.5)`), never banker's rounding
- capacity exactly reached: the `capacity`-th `ROUTE` succeeds, the next returns `NONE`
- `RELEASE` below zero → `ERROR`

## Variants seen in the wild
- **Tie-break by registration order** — the LeetCode post's own sample prints
  `us-east-1 0 us-east-1 ap-south-1` for two regions both at distance 0 (us-east-1 registered
  first), while its prose and PracHub say "ties broken alphabetically". Supported via
  `process_commands(lines, tie="registration")`; the primary is `tie="name"`.
- The same post reports `DISTANCE 0 0 100 100 → 10200`; the standard formula gives 9815
  (10200 is the value for latitude 80 — almost certainly a transcription slip).
- PracHub JSON-array variant: `processDataCenterCommands([["REGISTER","east",40,-74,10], ...])`
  with the same semantics; float coordinates accepted — `process_commands(lines, allow_float=True)`.
- 1point3acres titles: "Data Center Registration and Health Management", "Datacenter Router
  Command Processor", "Proximity-Aware Datacenter Request Router" (same problem).

## What this tests
skills: S01 read-the-whole-spec · S02 parsing/typed fields · S03 state per region · S08
deterministic tie-breaks · S09 exact output · S18 validation & error paths · S19 incremental
design · S21 stdlib (`math`)

## Sources
- https://leetcode.com/discuss/post/8470971/ (Stripe OA 2026 | SSE3, 2026-08-19 — verbatim commands and samples)
- PracHub "Register Data Centers and Route to the Nearest Healthy Region" (full spec dated 2026-08-22; JSON-array form, R = 6371 km, `floor(d+0.5)`)
- 1point3acres 题库 `request-routing-haversine-oa` (OA · 60 min · Medium · last asked 2026-08-11)
- InterviewDB "Proximity Request Routing — OA" / "Request Router"

## Clarifications (from adversarial review, 2026-08-26)
- `ROUTE` accepts any numeric lat/lon without range validation (e.g. `ROUTE 100 200` is computed, not rejected) — the sources are silent; hidden tests are unlikely to probe it.
