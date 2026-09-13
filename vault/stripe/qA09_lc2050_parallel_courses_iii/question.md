# qA09 · LC 2050 Parallel Courses III — weighted DAG longest path, the critical path, k-worker scheduling

LC 2050 · *Parallel Courses III* · Hard · https://leetcode.com/problems/parallel-courses-iii

## Context
A payout run, a data-pipeline DAG, a deploy plan (q29) — Stripe's batch systems are dependency graphs
of jobs with durations, and the first question any on-call engineer asks is "how long until the whole
thing is done, and which chain of jobs is the bottleneck?". LC 2050 is exactly that: jobs with
durations, prerequisite edges, unlimited parallelism → the longest weighted path. Interviewers then
push toward what production really has: *which* jobs form the critical path (what to optimize first),
and a bounded worker pool (only k jobs can run at once), where the clean answer becomes a heuristic
that must be named as such.

## The problem (restated)
There are `n` jobs numbered `1..n`. `time[i]` (0-based list) is the number of months job `i+1` takes.
`relations` is a list of `[prev, next]` pairs: `next` cannot start until `prev` has finished. Any
number of jobs may run at the same time, and a job starts as soon as all of its prerequisites are done.
Return the minimum number of months until every job has finished. The graph is guaranteed acyclic.
LC limits: `1 ≤ n ≤ 5·10^4`, `0 ≤ len(relations) ≤ min(n(n−1)/2, 5·10^4)`, `1 ≤ time[i] ≤ 10^4`,
no duplicate edges.

## Input (stdin)
```
PART n                 # 1..3
K k                    # Part 3 only, positive integer (worker count)
n
t1 t2 ... tn           # n durations, space separated
prev,next              # one relation per line (may be absent)
...
```
Blank lines are ignored; whitespace around `,` is tolerated.

## Output
* Part 1: one line, the minimum number of months.
* Part 2: line 1 the critical path as job ids joined by ` -> ` (e.g. `3 -> 4 -> 5`), line 2 its length
  in months (equals Part 1).
* Part 3: line 1 the makespan with `k` workers, then one line per job `job start end` in order of
  (start, job).

## Rules
### Part 1 — LC signature  `minimum_time(n, relations, time) -> int`
Kahn's algorithm. `finish[j] = time[j] + max(finish[p] for p → j)` (0 when `j` has no
prerequisites); process jobs in topological order so every predecessor is final before it is used.
Answer `max(finish)`. Must be O(n + m); a recursive DFS is acceptable but n = 5·10^4 deep chains
overflow Python's default recursion limit — iterate.

### Part 2 — the critical path  `critical_path(n, relations, time) -> list[int]`
Return one longest chain of jobs, in execution order, as 1-based ids. Deterministic choice: the
path ends at the job with the largest `finish` (smallest id on ties) and walks backwards, at each
step picking the prerequisite with the largest `finish` (smallest id on ties). `sum(time[j-1] for j
in path) == minimum_time(...)`. A single job → `[1]`.

### Part 3 — k workers  `schedule_k_workers(n, relations, time, k) -> list[Slot]`   (designed)
At most `k` jobs may run at the same time. Return `Slot(job, start, end)` for every job, sorted by
`(start, job)`; the makespan is `max(end)`. This is the classic list-scheduling heuristic (documented
as such — the k-bounded problem is NP-hard, so the interviewer wants a *good, deterministic* plan and
an honest statement that it is not always optimal):
1. `tail[j] = time[j] + max(tail[s] for j → s)` — the longest chain from `j` to any sink (Part 1 on the
   reversed graph). This is the priority: a job with a long tail is more urgent.
2. Event simulation from `now = 0`. Whenever a worker is free and jobs are ready (all prerequisites
   finished), start the ready job with the largest `tail`, then smallest id. When no worker is free
   (or nothing is ready), jump `now` to the earliest running job's end, retire everything ending then
   and release their successors.
3. `k ≥ n` (or `k` ≥ the width of the DAG) reproduces Part 1; `k = 1` gives `sum(time)`.
Jobs are never pre-empted. Expose `makespan_k_workers(n, relations, time, k) -> int` as
`max(end)` (0 for `n == 0`).

## Worked examples
```
LC ex1  n=3 relations=[[1,3],[2,3]] time=[3,2,5]                -> 8
        finish: 1→3, 2→2, 3→5+max(3,2)=8
LC ex2  n=5 relations=[[1,5],[2,5],[3,5],[3,4],[4,5]] time=[1,2,3,4,5] -> 12
        finish: 1→1, 2→2, 3→3, 4→3+4=7, 5→5+max(1,2,7)=12
Part 1  no relations, time=[4,9,2]                              -> 9   (all in parallel)
        chain 1→2→3, time=[4,9,2]                               -> 15  (sum)
Part 2  ex1 -> [1, 3]           (3's prerequisites: 1 finishes at 3, 2 at 2 → pick 1)
        ex2 -> [3, 4, 5]
        n=2, no relations, time=[5,5] -> [1]   (tie on finish → smallest id)
        n=3 relations=[[1,3],[2,3]] time=[2,2,1] -> [1, 3]     (prereqs tie at 2 → smallest id 1)
Part 3  ex2 with k=1 -> makespan 15 = 1+2+3+4+5
        ex2 with k=2 -> tails: 5→5, 4→9, 3→12, 2→7, 1→6. Ready at 0: {1,2,3} → start 3 (tail 12) and
        2 (tail 7). t=2: 2 ends → start 1. t=3: 3 ends, 4 ready → start 4 (needs only 3). t=7: 4 ends;
        5 needs 1,2,3,4 → all done → start 5, ends 12. makespan 12 (= Part 1, k=2 was enough)
        slots: (3,0,3) (2,0,2) (1,2,3) (4,3,7) (5,7,12) → printed sorted by (start, job):
        2 0 2 / 3 0 3 / 1 2 3 / 4 3 7 / 5 7 12
        no relations, time=[4,9,2], k=2 -> tails 4,9,2; start 2 (tail 9) and 1 (tail 4); t=4: start 3
        (ends 6); t=9 done -> makespan 9
        no relations, time=[3,3,3], k=2 -> 6 (third job waits for a worker)
```
stdin for Part 1 ex1:
```
PART 1
3
3 2 5
1,3
2,3
```
→ `8`
stdin for Part 3 (`PART 3` / `K 2` / `5` / `1 2 3 4 5` / relations of ex2) →
```
12
2 0 2
3 0 3
1 2 3
4 3 7
5 7 12
```

## 关联知识点

- [[a11-weighted-topological-order|A11 带权拓扑序]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s21-python-stdlib-fluency|S21 语言熟练度与标准库]]
