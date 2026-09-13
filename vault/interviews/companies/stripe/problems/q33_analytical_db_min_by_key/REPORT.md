# q33 Analytical DB min_by_key — report

## Summary
A toy analytical database over dict records: find the record with the minimum value for a key
(missing key = 0), generalise to `first_by_key(key, asc|desc)`, extract the ordering into a
comparator object, then chain comparators for a stable multi-key `sort_by` / `top_k`. Stripe's
technical screen uses it to watch incremental design: each step must be re-implemented in terms of
the next abstraction without changing behaviour.

## Sources & confidence
high for Steps 1–3 — verbatim prompt and Python asserts in freecodemessiah's two notebooks
(2019 technical screen) and Glassdoor QTN_3113468 (Senior SWE). Step 4 (chained comparators /
`sort_by` with a list of (key, direction)) is reported only by title — implemented as a stable
`functools.cmp_to_key` sort over a `ChainedComparator` and marked lower confidence. No conflicts;
the prompt names the class both `Comparator` and `RecordComparator`, both are exposed. Ties: the
prompt allows any record; we fix "first in input order" (the notebook's own asserts assume it).

## Approach by part
1. `min_by_key = first_by_key(key, "asc", records)`; empty list → `None` (`null` on stdout).
2. `first_by_key`: single pass keeping `best`, replaced only when `compare(rec, best) == -1`.
3. `RecordComparator(key, direction)`: `sign = ±1`, values via `dict.get(key, 0)`, returns
   `sign * (-1 | 0 | 1)`; `ValueError` for a direction other than asc/desc (`INVALID_DIRECTION` line).
4. `ChainedComparator` returns the first non-zero result; `sort_by` = `sorted(key=cmp_to_key(...))`
   (stable); `top_k` slices (`k ≤ 0` → empty).

## Pitfalls hidden tests target
- missing key is 0, which sits *between* negative and positive values (`{}` beats `{"a": -1}` for max)
- ties must return the first record for both directions (strict `== -1`, not `<= 0`)
- do not mutate or copy records — return the same object; empty input → `None`, not an exception
- comparator antisymmetry and `desc == -asc`; stable multi-key sort keeps input order on full ties
- JSON output with sorted keys and default separators; `null` for no record

## Complexity & measured cost
Parts 1–3 O(n); Part 4 O(n log n) with a Python-level comparator. Measured: 0.45s, 60 MB
(100k JSON records: MIN + FIRST + two-key SORT).

## Test inventory
18 tests — part1: 5 · part2: 4 · part3: 4 · part4: 5 (incl. 1 io, 1 perf); edge 7 · fmt 1.

## Skills exercised
S02 parsing (JSON lines) · S03 records as dicts · S08 deterministic ties · S09 exact formatting ·
S18 missing-key handling · S19 incremental design · S21 stdlib fluency (`cmp_to_key`, `json`)
