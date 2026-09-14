---
nodes: [algorithms.topological]
tags: [stripe-oa, qa09, leetcode]
---
# Drill: longest path through a weighted job DAG, then its critical path, then k workers

Forty-five minutes, stdin to stdout. This is LeetCode 2050, Parallel
Courses III. `n` jobs (1-indexed) each take `time[i]` months (0-indexed);
`relations` gives `[prev, next]` prerequisite pairs; any number of jobs may
run at once once their prerequisites finish. Part 1 asks for the minimum
number of months until every job is done. Part 2 asks for the critical
path: one longest chain of jobs, in execution order, whose total duration
equals Part 1's answer. Part 3 bounds parallelism to `k` workers and asks
for a start/end slot per job — since the k-bounded version is NP-hard, this
is list scheduling by longest-remaining-tail priority, and the drill expects
you to name it as a heuristic rather than claim it's always optimal.

**Constraints to state and honor**
- Up to 5*10^4 jobs and 5*10^4 relations; the graph is guaranteed acyclic.
- `relations` uses 1-based job ids while `time` is 0-indexed — track both
  directions of that offset carefully.
- A deep chain of 5*10^4 jobs will blow Python's default recursion limit —
  the topological pass must be iterative (Kahn's algorithm).
- Part 2 ties (multiple prerequisites finishing at the same month, or
  multiple candidate end jobs) resolve to the smallest job id, both when
  choosing the end job and when walking backward.
- Part 3: no more than `k` jobs may overlap at any instant; `k = 1` must
  reduce to `sum(time)`, and `k >= n` (or the DAG's width) must reproduce
  Part 1 exactly; jobs are never pre-empted.

**Grading points**
- Kahn's algorithm with `finish[j] = time[j] + max(finish[p] for p -> j)`,
  relaxed in topological order so every predecessor is final before it's
  used — say why a naive recursive DFS is disqualified at this input size.
- The answer is `max(finish)` — state clearly that the critical path is not
  necessarily the path through the single longest-duration job.
- Part 2's backward walk needs a `pred` pointer recorded during the forward
  pass, plus a deterministic tie-break rule stated explicitly, not left to
  incidental iteration order.
- Part 3's priority signal (`tail[j]`, the longest remaining chain from `j`
  to any sink) comes from running Part 1's logic on the reversed graph —
  recognizing that reuse is the key insight, not building a separate
  algorithm.
- The event simulation for Part 3 must handle worker release and new-job
  readiness at the same instant correctly (an ending job frees its
  successors before new starts are chosen for that same timestamp).
- Explicitly flag Part 3 as list scheduling, a heuristic — sub-optimal in
  general — rather than presenting it as an exact solution.
- Edge cases: no relations at all (answer is `max(time)`); a single job;
  a 5*10^4-long chain (answer up to 5*10^8, no overflow concern in Python
  but recursion depth is real); ties on `finish` among several
  prerequisites.

**Source**
- `vault/interviews/companies/stripe/problems/qA09_lc2050_parallel_courses_iii/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/qA09_lc2050_parallel_courses_iii.md`
- `vault/interviews/companies/stripe/problems/qA09_lc2050_parallel_courses_iii/problem.md`, `vault/interviews/companies/stripe/problems/qA09_lc2050_parallel_courses_iii/REPORT.md`
- `vault/interviews/companies/stripe/study/10-solutions/qA09_lc2050_parallel_courses_iii.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
