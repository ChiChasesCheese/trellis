---
nodes: [output.ordering, toolbox.heap, transfer.stripe-oa]
tags: [stripe-oa, q28]
---
# Drill: route tasks to the least-busy qualified worker

Sixty minutes, stdin to stdout, language-agnostic (a priority-queue primitive is the only
structure you need beyond plain records). A WORKERS section and a TASKS section describe agents
with skills and capacity and work items with a required skill and cost; tasks are assigned in
input order to the worker with the smallest current load, and each part narrows or refines the
pool. Part 1 ignores skills and capacity entirely — least load, ties by worker id. Part 2
restricts candidates to workers whose skill list contains the task's required skill, printing
UNASSIGNED when nobody qualifies. Part 3 breaks equal-load ties by preferring the specialist —
the worker with fewer distinct skills — before falling back to id. Part 4 adds a hard capacity
ceiling: a worker is only a candidate if load + cost fits within capacity, still ranked by the
Part 3 key among those that fit.

**Constraints to state and honor**
- WORKERS lines carry id, `;`-separated skills, and capacity; TASKS lines carry id, required
  skill, non-negative cost; tasks are processed strictly in input order and every worker is
  printed at the end, including those still at load 0.
- The tie-break is one growing key: `(load, id)` in Parts 1-2, `(load, distinct skill count, id)`
  in Parts 3-4 — never a separate comparison function per part.
- Up to 10^5 tasks against 10^3 workers: a linear min-scan per task is ~10^8 comparisons, too slow
  for the time budget.
- Capacity sits on every worker line but is inert until Part 4, where `load + cost <= capacity`
  (not strict `<`) decides fit.
- No candidate — unknown skill, or nobody fits within capacity — prints `task_id -> UNASSIGNED`
  and leaves every load untouched.

**Grading points**
- One engine parameterized by which rules are active, not four rewrites — say out loud that each
  part only appends a term to the same selection key.
- A heap per skill (or one shared heap) instead of a re-scan per task, with lazy invalidation: an
  entry popped with a stale load is discarded and the worker's current state re-pushed.
- Duplicate skills in a worker's list count once for the specialist tie-break — dedupe before
  counting, not before storing.
- String tie-break, not numeric: `w10` sorts before `w2`.
- Part 4's twist that the least-loaded worker may not fit while a busier one does, so the
  pop-and-check loop must be able to skip past the top of the heap rather than trust the first pop.
- Zero-cost tasks fit a worker already at capacity; a capacity of 0 accepts only zero-cost tasks.
- Empty WORKERS or empty TASKS sections fall out of the same loop without a special case.

**Source**
- `vault/interviews/companies/stripe/problems/q28_worker_task_assignment/problem.md`, `vault/interviews/companies/stripe/problems/q28_worker_task_assignment/REPORT.md`, `vault/interviews/companies/stripe/problems/q28_worker_task_assignment/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q28_worker_task_assignment.md`, `vault/interviews/companies/stripe/study/10-solutions/q28_worker_task_assignment.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
