# qA12 LC 399 Evaluate Division — report

## Summary
The LeetCode twin of Stripe's currency-conversion phone screen (q21): `a/b = v` quotes, answer
`c/d` through the graph or `-1`. Drilled here are the two techniques an interviewer expects by name
(BFS with inverse edges; weighted union-find with path compression) plus the FX-desk follow-ups: best
rate across disagreeing quotes (max product over simple paths) and flagging inconsistent quotes with a
relative tolerance. q21's bespoke parts (string table, direct/inverse, payouts in cents) are linked,
not duplicated.

## Sources & confidence
tag freq 76.9 / 83.5 (liquidslr 2025-06), 68.2 (shreeratn 2025-05), 87.5 / 100.0 (snehasishroy
2026-07); asked-list repos Hazeera65, premjm-67 `ED.java`, TWINSRIRAM; LC 5150083 comments (2024-05)
→ high. Parts 3–4 are designed follow-ups (Part 3 mirrors q21 Part 3's rule).

## Approach by part
1. `_adjacency`: `A→B = v`, `B→A = 1/v`. BFS per query with a `seen` dict holding the product; seed
   `seen[src] = 1.0` gives `x/x = 1` for known x; unknown variable → `-1.0`. O(V+E) per query.
2. `_WeightedUF`: `weight[x] = x/parent[x]`; `find` re-multiplies weights while compressing;
   `union(a, b, v)` sets `weight[ra] = v·wb/wa`; `ratio` = `wa/wb` when roots match. Near O(1)/query.
3. `best_rate_path`: DFS over simple paths, neighbours in sorted order; keep the max `(product, −hops)`
   with strict `>` so the first (lexicographically smallest) path wins ties. Exponential in theory,
   trivial at LC size (≤ 20 equations).
4. `find_conflicts`: register both variables, compute the implied ratio via UF; `|implied − v| >
   rel_tol·v` → `Conflict(index, a, b, given, implied)` and the equation is **not** applied.

## Pitfalls hidden tests target
- `x/x` for an unknown variable is `-1.0`, for a known one `1.0`
- forgetting the inverse edge (`b/a`), or adding it with `v` instead of `1/v`
- union-find weight not re-multiplied during path compression; joining two trees via non-roots
- Part 3: cycles with product > 1 must not be looped (simple paths); best ≠ shortest
- Part 4: relative tolerance (2.0 vs 2.0000000001 is fine); rejected quotes stay rejected; `a/a = 2`

## Complexity & measured cost
Part 1 O(Q·(V+E)); Part 2 O((E+Q)·α); Part 3 exponential in V (LC-size only); Part 4 O(E·α).
Measured: 0.20 s for the perf test (20 equations × 10^4 BFS and UF queries + 2·10^4 equations /
2·10^4 UF queries + conflict scan + one script run); script run alone (2·10^4 eq + 2·10^4 queries,
Part 2) 0.07 s, ~33 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 5 (incl. 1 io) · part2: 4 (incl. 1 perf) · part3: 3 · part4: 3; edge 5 · fmt 1.

## Skills exercised
A02 weighted graph path product · A16 union-find · S08 deterministic tie-breaks · S19 incremental design · S21 deque/dict fluency
