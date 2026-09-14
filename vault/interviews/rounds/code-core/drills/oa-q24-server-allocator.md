---
nodes: [toolbox.heap, model.idempotency, transfer.stripe-oa]
tags: [stripe-oa, q24]
---
# Drill: hand out the smallest free server number per host type

Sixty minutes, four parts. A hostname is a type plus a number (`apibox1`, `apibox2`,
`sitebox1`); allocating a type returns its smallest currently-free number, and
deallocating a hostname returns that number to the pool. Part 1 is the pure function:
given a list of currently-allocated numbers, return the smallest missing positive integer.
Part 2 wraps it in a stateful tracker with one independent counter and pool per host type.
Part 3 is a performance requirement — O(log n) per operation instead of an O(n) rescan.
Part 4 drives the tracker from a command stream.

**Constraints to state and honor**
- Part 1's input may contain duplicates, zero, negative numbers, or non-integers; none of
  them can be the answer and none of them block one.
- A hostname splits at its trailing run of digits (`apibox12` -> type `apibox`, number 12);
  a host type may not itself end in a digit, and a number with a leading zero is unknown.
- Deallocating an unknown, already-freed, or malformed name is a silent no-op, never an error.
- Up to 10^6 commands; every allocate/deallocate must be O(log n).

**Grading points**
- Per type: a high-water counter for numbers never yet issued, plus a min-heap of freed
  numbers — allocate pops the heap if non-empty, else advances the counter. A design that
  tracks only `len(live) + 1` breaks the moment a number is freed and the pool isn't empty.
- A `live` set of currently-allocated names makes deallocate idempotent — without it, a
  double free pushes the same number onto the heap twice and two hosts end up with the same
  name.
- After freeing several numbers, the next several allocations come out in ascending order
  purely from heap semantics, not from any extra bookkeeping.
- Host types are completely independent pools; freeing a number in one type never affects
  another.
- Splitting a hostname at its trailing digit run (not just the last character) so
  `apibox10` parses as `(apibox, 10)`, and rejecting shapes that would make that split
  ambiguous.
- The O(n) rescan version of Part 2 is the wrong answer for Part 3 — say why the heap
  version is O(log n) per operation before writing it.

**Source**
- The full statement, solution notes and report: `vault/interviews/companies/stripe/problems/q24_server_allocator/problem.md`,
  `vault/interviews/companies/stripe/study/10-solutions/q24_server_allocator.md`,
  `vault/interviews/companies/stripe/problems/q24_server_allocator/problem.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
