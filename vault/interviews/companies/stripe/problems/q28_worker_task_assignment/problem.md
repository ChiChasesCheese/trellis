# q28 · Worker Task Assignment — least-busy worker, required skills, specialists, capacity

**Type:** bespoke OA / onsite · **Stage:** HackerRank OA or onsite coding (60 min, 4 parts) · **Last asked:** 2025-10-09 (1point3acres 题库 `worker-task-assignment`)
**Frequency:** 1 independent source (1point3acres 题库 summary: "balance workload to the least-busy worker, restrict to workers with the required skills, prefer the …", Medium, 4 parts) · **Confidence:** low-medium — only the summary is public; the I/O format, the Part 3 "prefer the specialist" rule and the Part 4 capacity rule are **reconstructed** and marked.

## Context
Stripe's support and risk-review queues route work items (disputes, KYC reviews, refund
approvals) to agents. Each item needs a skill (`kyc`, `disputes`, `fraud`), costs some effort, and
should go to the agent with the least work in their queue so nobody drowns. Later rules refine the
choice: only qualified agents, prefer specialists over generalists when the load is equal, and
never push an agent past their capacity.

## Input (stdin)
First line `PART n` (1–4). Then a `WORKERS` section and a `TASKS` section:
```
PART 3
WORKERS
w1,python;go,10             worker_id, skills (';'-separated, may be one), capacity
w2,python,5
TASKS
t1,python,5                 task_id, required_skill, cost (non-negative integer)
t2,go,3
```
Blank lines are ignored; spaces around separators are tolerated. Task lines are processed
**in input order**. Worker ids and task ids are unique. `capacity` is present in every part but
only used in Part 4.

## Output
One line per task in input order, `task_id -> worker_id` (or `task_id -> UNASSIGNED`), then one
line per worker `worker_id load` **sorted by worker_id (plain string order)**, `load` = sum of the
costs assigned to that worker. Every worker is listed, including load 0.

## Rules
### Part 1 — least-busy worker
Skills and capacity are ignored: every worker can take every task. Assign each task to the worker
with the **smallest current load**; ties → smallest worker id (string order). The load is updated
immediately, so the next task sees it.

### Part 2 — required skill
Only workers whose skill list contains the task's `required_skill` (exact, case-sensitive match)
are candidates. Same tie-break as Part 1. If no worker has the skill → `UNASSIGNED` (no load
change).

### Part 3 — prefer the specialist (reconstructed from "prefer the …")
Among candidates with equal load, prefer the worker with **fewer skills** (the specialist), then the
smallest id. Full key: `(load, number_of_skills, worker_id)`.

### Part 4 — capacity (reconstructed)
A worker can take a task only if `load + cost <= capacity` (`<=`: filling exactly to capacity is
fine). Among the workers that fit, apply the Part 3 key. If nobody fits (or nobody has the skill)
→ `UNASSIGNED`. A zero-cost task fits a full worker.

## Worked examples
Common worker set (`capacity` only matters in Part 4):
```
WORKERS
w1,python;go,10
w2,python,5
w3,go,3
TASKS
t1,python,5
t2,go,3
t3,python,4
t4,go,1
```
**Part 1** (skills ignored; least load, ties by id)
```
t1 -> w1        t2 -> w2        t3 -> w3        t4 -> w2   (loads 5,3,4 -> w2)
w1 5
w2 4
w3 4
```
**Part 2** (skill required)
```
t1 -> w1        t2 -> w3        t3 -> w2        t4 -> w3   (go: w1=5, w3=3)
w1 5
w2 4
w3 4
```
**Part 3** (equal load → fewer skills first)
```
t1 -> w2   (w1 and w2 at 0; w2 has 1 skill)
t2 -> w3   (w1, w3 at 0; w3 has 1 skill)
t3 -> w1   (w1 at 0 < w2 at 5)
t4 -> w3   (w3 at 3 < w1 at 4)
w1 4
w2 5
w3 4
```
**Part 4** (capacity 10 / 5 / 3) with two extra tasks `t5,rust,1` and `t6,go,9`
```
t1 -> w2   (0+5 <= 5)
t2 -> w3   (0+3 <= 3)
t3 -> w1   (w2 would be 9 > 5)
t4 -> w1   (w3 would be 4 > 3; w1 4+1 <= 10)
t5 -> UNASSIGNED   (nobody knows rust)
t6 -> UNASSIGNED   (w1 5+9 > 10, w3 3+9 > 3)
w1 5
w2 5
w3 3
```

## Edge cases hidden tests are known to target
- ties by id are **string** order (`w10` < `w2`); the load updates between consecutive tasks
- a task with an unknown skill → `UNASSIGNED`; workers with zero load must still be printed
- zero-cost tasks are assigned (and fit a full worker); equal loads after several assignments
- Part 3: a generalist with lower load still beats a specialist with higher load (load first)
- Part 4: `load + cost == capacity` accepted, one more rejected; capacity 0 takes only zero-cost
  tasks; the least-loaded worker may not fit while a busier one does
- duplicate skills in a worker's list (`python;python`) count once for the specialist rule
- empty task list → only the worker lines; empty worker list → every task `UNASSIGNED`
- 10^5 tasks × 10^3 workers: a linear scan per task is 10^8 comparisons — use per-skill heaps

## Variants seen in the wild
- The 1point3acres summary ends "prefer the …" — the third rule may be "prefer the worker with
  the fewest assigned *tasks*" or "the worker who has waited longest (round robin)" instead of
  "fewest skills"; the solution takes a `specialist_key` hook so the tie-break can be swapped.
- Onsite version reportedly asks the same as an in-memory class (`add_worker`, `assign(task)`),
  with a discussion of the heap/lazy-invalidation upgrade for scale.

## What this tests
skills: S02 parsing (sections, `;` lists) · S03 modeling workers as records in dicts ·
S04 grouping by skill · S05 `<=` capacity threshold · S08 deterministic multi-key tie-break ·
S09 exact formatting · S19 incremental design (each part adds one term to the key) ·
S21 heap + lazy invalidation for performance

## Sources
- 1point3acres 题库 `worker-task-assignment` (OA / Onsite, Medium, last asked 2025-10-09) — catalog/raw/cn_sources.md §2.19
