---
nodes: [toolbox.heap, model.entity-state, model.index, performance.budget, performance.amortized, output.ordering]
tags: [classic]
---
# Drill: least-loaded assignment under a performance budget

Forty-five minutes. The first line gives `num_targets max_per_target`. Then a
stream of `ASSIGN <id> <owner> [<group>]`, `RELEASE <id>` and `RETIRE <index>`
requests. Each `ASSIGN` goes to the target with the fewest live assignments,
ties to the smallest index. If the request carries a group that has already been
placed, it must go to that group's target even if a lighter one exists. A target
at capacity cannot be chosen — including a group's pinned target, in which case
the request is rejected outright. `RETIRE` evicts a target's assignments and
re-places them in original arrival order.

**Constraints to state and honor**
- `num_targets` up to 10^5 and up to 2·10^5 requests: 2 s, 256 MB.
- Target indices are 1-based in both input and output.
- Log only successful placements, as `id,owner,target`.

**Grading points**
- Both bounds are 10^5, so scanning targets per request is 10^10 — state the
  product before choosing ([[cc-performance-budget-bounds-multiply]]).
- A min-heap of `(load, index)` with lazy invalidation, and the amortized
  argument for why it is fast enough ([[cc-performance-amortized-lazy-heap]]).
- The tuple order gives the smallest-index tie-break for free
  ([[cc-python-stdlib-heapq-calls]]).
- Two indexes (id to placement, target to members) kept in step by one function
  per transition ([[cc-verification-invariant-two-indexes]]).
- Duplicate live id ignored; unknown `RELEASE` ignored; an id reusable after
  release ([[cc-verification-edge-duplicate-and-out-of-order]]).
- A pinned target at capacity rejects even when others have room — assert the
  invariant that no target exceeds capacity
  ([[cc-verification-invariant-conservation]]).

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
