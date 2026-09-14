---
nodes: [output.ordering, python.idioms, transfer.stripe-oa]
tags: [stripe-oa, q33]
---
# Drill: build a toy analytical database, one abstraction layer at a time

Sixty minutes, stdin to stdout. Records are JSON objects with string keys and integer values, held
in an array in input order; queries run against that array. Part 1 implements `min_by_key(key)`:
the record with the smallest value for that key, treating a missing key as 0. Part 2 generalizes
to `first_by_key(key, direction)` for both minimum and maximum, and `min_by_key` must now be
re-expressed in terms of it. Part 3 extracts the ordering into a `RecordComparator(key,
direction).compare(a, b)` returning -1/0/1, and `first_by_key` must now be re-expressed in terms
of the comparator. Part 4 chains multiple comparators into one, and implements a stable
multi-key `sort_by` and a `top_k` on top of the chain.

**Constraints to state and honor**
- A record missing the query key counts as having value 0 for that key — this sits strictly
  between negative and positive values, not at either extreme.
- Ties always resolve to the first record in input order, for both `asc` and `desc` — never
  "any" record, even though the original prompt allows it.
- An empty record array answers `null`; a comparator direction other than `asc`/`desc` answers
  `INVALID_DIRECTION`.
- Output is JSON with sorted keys and default separators; comparator answers print as the bare
  integers -1, 0, or 1.
- Up to 10^5 records: min/first must stay O(n) per query, and the multi-key sort O(n log n).

**Grading points**
- Each step must actually delegate to the next abstraction rather than duplicate logic — say out
  loud that `min_by_key` calling `first_by_key("asc", ...)`, and `first_by_key` calling the
  comparator's `compare`, is the point of the exercise, not an optional nicety.
- `.get(key, 0)` as the single place the missing-key rule lives, never an `if key not in record`
  branch duplicated across functions.
- Strict `compare(rec, best) == -1` (not `<= 0`) as what keeps ties resolving to the first record
  in both directions.
- Never mutating or copying an input record to compute `desc` — the comparator flips a sign, it
  doesn't negate stored values.
- A comparator that is provably antisymmetric (`compare(a, b) == -compare(b, a)`), checked as an
  explicit case, not just assumed from the code shape.
- The chained comparator returning the first non-zero result, and `sort_by` implemented as one
  stable sort (`functools.cmp_to_key` or equivalent) so equal-key records keep their input order.
- `top_k` boundaries: `k <= 0` returns empty, `k` beyond the record count returns everything.

**Source**
- `vault/interviews/companies/stripe/problems/q33_analytical_db_min_by_key/problem.md`, `vault/interviews/companies/stripe/problems/q33_analytical_db_min_by_key/REPORT.md`, `vault/interviews/companies/stripe/problems/q33_analytical_db_min_by_key/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q33_analytical_db_min_by_key.md`, `vault/interviews/companies/stripe/study/10-solutions/q33_analytical_db_min_by_key.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
