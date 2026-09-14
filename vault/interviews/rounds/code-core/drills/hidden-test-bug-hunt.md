---
nodes: [round.debugging, round.hidden-tests, verification.edge-catalog, verification.invariants, python.pitfalls, transfer.playbook]
---
# Drill: name the bug class from the failing-test description alone

Twenty-five minutes, no code at the start. You are given a solution that passes
every worked example and a list of hidden-test *names* that failed — nothing
else. For each one, write down the class of bug it points at, the smallest input
that would reproduce it, and the one-line fix. Only then open the code.

Work through descriptions of this shape:

- `test_threshold_exact_boundary` fails, `test_threshold_above` passes.
- `test_empty_input` fails with a `ValueError`.
- `test_duplicate_id` fails but `test_unknown_id` passes.
- `test_output_order_ties` fails on some runs and passes on others.
- `test_perf_1e5` times out; every correctness test passes.
- `test_reversal_of_last_event` fails with `ZeroDivisionError`.
- `test_large_amounts` is off by one unit.

**Constraints to state and honor**
- Diagnose from the name before reading the code; the point is the mapping from
  symptom to class, not the debugging.
- One minimal reproducing input per item, written out in full.
- Bug class must be one of: format, boundary, modelling, performance,
  determinism, arithmetic.

**Grading points**
- Exact-boundary failure means the comparison operator, not the arithmetic
  ([[cc-verification-edge-exact-threshold-triple]]).
- An intermittent ordering failure is `set` iteration or `hash()`, never "flaky"
  ([[cc-verification-determinism-set-iteration]], [[cc-verification-determinism-stable-hash]]).
- Timeout with all correctness tests green points at a re-scan, a re-sort or a
  re-parse inside a loop ([[cc-performance-hot-loop-resort]]).
- Off-by-one on large amounts is float accumulation
  ([[cc-python-pitfalls-float-equality]]).
- Each diagnosis becomes one general card, not a note about this exercise
  ([[cc-transfer-playbook-card-the-rule]]).

**Attempt log**
- [ ] Attempt 1 (date, 25 min, self-graded notes):
