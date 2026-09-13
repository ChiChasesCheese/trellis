# q17 · Datacenter Request Router — registry, health, Haversine distance, proximity routing

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

## 关联知识点

- [[s01-read-full-spec-first|S01 先读完整份规格，为 Part N+1 而设计]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s21-python-stdlib-fluency|S21 语言熟练度与标准库]]
