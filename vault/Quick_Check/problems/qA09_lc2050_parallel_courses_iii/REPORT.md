# qA09 LC 2050 Parallel Courses III — report

## Summary
Weighted DAG longest path (Kahn + `finish[j] = time[j] + max finish of prerequisites`): the Stripe-tag
Hard that models every batch pipeline / deploy train question. Follow-ups: the critical path (what to
speed up) and a k-worker bound where the clean answer becomes list scheduling with longest-tail
priority — a heuristic the candidate must name as such.

## Sources & confidence
tag freq 61.2 / 67.1 (liquidslr 2025-06 All / >6mo), 44.6 (shreeratn 2025-05), 62.5 / 62.5
(snehasishroy 2026-07); premjm-67 `PL.java` asked-list → high on tag data, medium as no dated
write-up. Part 3 is designed (marked so in problem.md).

## Approach by part
1. `_graph` (0-based adjacency from 1-based relations) → `_topo` (Kahn, deque, smallest-id-first
   among ready) → `_finish_and_pred`: relax every edge once in topological order; strict `>` keeps the
   smaller-id predecessor on ties. O(n + m). Iterative, so a 5·10^4 chain is fine.
2. `critical_path`: pick the end job by `(finish, -id)`, walk `pred` back, reverse.
3. `schedule_k_workers`: `tail[j]` by reverse topological order; ready-heap `(-tail, id)`; running-heap
   `(end, id)`; fill free workers, jump `now` to the earliest end, retire, release successors. Slots
   sorted by `(start, job)`. O((n + m) log n). Documented as list scheduling (not optimal in general).

## Pitfalls hidden tests target
- 1-based `relations` vs 0-based `time` (off-by-one both ways)
- recursive DFS on a 5·10^4 chain → RecursionError; answer up to 5·10^8 (no int32 concern in Python)
- relaxing an edge before its source is final (wrong when edges are listed child-first)
- Part 2 ties: end-job tie and predecessor tie both go to the smallest id, independent of edge order
- Part 3: never exceed k concurrent jobs at an instant where ends and starts coincide (ends first);
  `k = 1` must equal `sum(time)`, `k ≥ n` must equal Part 1

## Complexity & measured cost
Parts 1–2 O(n + m) time and memory; Part 3 O((n + m) log n). Measured: 0.31 s for the perf test
(n = m = 5·10^4 random DAG through Parts 1, 2 and 3 with k = 8 in-process + one script run); script
run alone 0.07 s, ~40 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 8 (incl. 1 io, 1 perf) · part2: 3 · part3: 4; edge 6 · fmt 1.

## Skills exercised
A11 topological order with weights · S08 deterministic tie-breaks · S19 incremental design · S21 deque/heapq fluency
