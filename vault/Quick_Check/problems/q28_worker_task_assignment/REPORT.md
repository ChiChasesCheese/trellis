# q28 Worker Task Assignment — report

## Summary
Queue routing for support/risk work items: each task goes to the least-loaded worker, restricted
to workers with the required skill, preferring specialists on ties, and never exceeding capacity.
Four parts that each add one term to a single selection key — the textbook "incremental design"
OA where a candidate who hard-codes Part 1 has to rewrite for Parts 2–4.

## Sources & confidence
low-medium — a single 1point3acres 题库 summary (`worker-task-assignment`, OA / Onsite, Medium,
last asked 2025-10-09): "balance workload to the least-busy worker, restrict to workers with the
required skills, prefer the …". The I/O format (WORKERS/TASKS sections, `->` lines, `id load`
lines), the Part 3 "prefer the specialist (fewer skills)" rule and the Part 4 capacity rule are
reconstructed and marked; problem.md lists the alternative Part 3 readings.

## Approach by part
One engine `assign(lines, use_skills, specialist, use_capacity)`:
1. key `(load, id)`; all workers live in one pseudo-skill heap `*`.
2. a heap per skill; a task pops from its skill's heap; missing skill → `UNASSIGNED`.
3. key `(load, len(set(skills)), id)` — duplicates in the skill list count once.
4. popped candidates with `load + cost > capacity` are parked and pushed back; `<=` fits.
Each successful assignment bumps the worker's version and re-pushes it into all its skill heaps;
stale entries are skipped on pop (lazy invalidation).

## Pitfalls hidden tests target
string-order ties (`w10` < `w2`); load carried between consecutive tasks; unknown / case-different
skill → `UNASSIGNED`; zero-load workers still printed; zero-cost tasks fit a full worker;
Part 3 only breaks *equal* load; capacity `==` accepted and `+1` rejected; least-loaded worker
not fitting while a busier one does; an `UNASSIGNED` task leaves the pool intact; empty sections.

## Complexity & measured cost
O((W·k + T·k) log(W·k)) with k skills per worker; worst case O(W log W) for a task nobody fits.
100k tasks × 1000 workers (≤3 skills each, 20 skills): 0.154 s, 50.4 MB. A `min()` scan per
task would be ~10^8 comparisons (≈10 s in CPython).
Measured: 0.154s, 50.4 MB

## Test inventory
16 tests — part1: 4 · part2: 3 · part3: 3 · part4: 6; edge 8 · fmt 1 · io 1 · perf 1.
`IMPL=starter`: 16 failed / 0 passed.

## Skills exercised
S02 parsing (sections, `;` lists) · S03 records in dicts · S04 grouping by skill ·
S05 `<=` capacity threshold · S08 multi-key deterministic tie-break · S09 exact formatting ·
S19 incremental design · S21 heap + lazy invalidation
