# q33 · Analytical Database — `min_by_key` / `first_by_key` / comparator / `sort_by`

**Type:** phone screen / technical screen (2019–2023) · **Stage:** technical screen (freecodemessiah
notebooks "This is what my stripe interview was like", 2019-01; Glassdoor QTN_3113468 Senior SWE) ·
**Last asked:** 2023 (Glassdoor) · **Frequency:** 3 independent sources (freecodemessiah ×2 notebooks,
Glassdoor) · **Confidence:** high for Steps 1–3 (verbatim prompt + asserts); Step 4 lower confidence
(reported as "multi-key / chained comparators, sort_by with a list of (key, direction) pairs")

## Context
"Throughout this interview, we'll pretend we're building a new analytical database. Don't worry
about actually building a database though – these will all be toy problems. Here's how the
database works: all records are represented as maps, with string keys and integer values. The
records are contained in an array, in no particular order." Example use: each record is a school
student; `min_by_key` answers "who is the youngest student?" or "who has the lowest GPA?".

## Input (stdin)
First line `PART n`. Then, in any order: **record lines** — one JSON object per line with string
keys and integer values (e.g. `{"a": 1, "b": 2}`, `{}`), and **query lines** (commands below). All
record lines form the record array in input order; every query is answered against that array, in
query order. Blank lines ignored. Up to 10^5 records.

## Output
One answer per query. A record is printed as JSON with keys sorted and the default separators
(`{"a": 1, "b": 2}`, `{}`); "no record" prints `null`. Comparator results print `-1` / `0` / `1`.
A direction other than `asc` / `desc` prints `INVALID_DIRECTION`.

## Rules
### Part 1 — `min_by_key(key, records)` (verbatim Step 1)
`MIN key` → the record with the minimum value for `key`. **Records that do not contain the key are
considered to have value 0** ("Note that keys may map to negative values!"). Empty array → `null`
(`None` from the function — "handle an empty array idiomatically"). "If several records share the
same minimum value, you may return any of them" — **we return the first one in input order**
(deterministic).

### Part 2 — `first_by_key(key, direction, records)` (verbatim Step 2)
`FIRST key asc|desc` → with `asc` the minimum record, with `desc` the maximum; missing key = 0;
ties → first in input order; empty → `null`. `min_by_key` must be re-implemented as
`first_by_key(key, "asc", records)`.

### Part 3 — `RecordComparator(key, direction).compare(a, b)` (verbatim Step 3)
Returns `-1` if `a` comes before `b` according to key and direction, `0` if neither comes before
the other, `1` if `a` comes after `b`. Missing key = 0. `first_by_key` must be implemented **via the
comparator** (keep `best`, replace when `compare(rec, best) == -1` — strict, so ties keep the
first). `COMPARE key asc|desc` → compares the **first two** record lines. The class is also exposed as
`Comparator` (the prompt uses both names).

### Part 4 — chained comparators and `sort_by` (lower confidence, from the reported Steps 4–5)
`ChainedComparator([RecordComparator, ...])` compares by the first comparator that is not `0`.
`sort_by(specs, records)` with `specs = [(key, direction), ...]` returns the records **stably**
sorted by the chain (equal records keep input order). `top_k(specs, k, records)` = the first `k`
of that order (`k ≤ 0` → empty; `k > n` → all). Queries: `SORT k1:asc,k2:desc` prints every record
in sorted order, one per line; `TOP n k1:asc,...` prints the first `n`.

## Worked examples
```
PART 1                              Output
MIN a                               {"a": 1, "b": 2}
{"a": 1, "b": 2}
{"a": 2}

PART 1                              Output
MIN b                               {"a": 2}        (missing b counts as 0 < 2)
{"a": 1, "b": 2}
{"a": 2}

PART 1                              Output
MIN b                               {"b": -1}       (0 for the first record > -1)
{"a": -1}
{"b": -1}

PART 2                              Output
FIRST a asc                         {"b": 1}        (a missing in both first records = 0; first wins the tie)
FIRST a desc                        {"a": 10}
FIRST b asc                         {"b": -2}
FIRST b desc                        {"b": 1}
{"b": 1}
{"b": -2}
{"a": 10}

PART 2                              Output
FIRST a desc                        {"a": 10, "b": -10}
{}
{"a": 10, "b": -10}
{}
{"a": 3, "c": 3}

PART 3                              Output
COMPARE a asc                       -1
{"a": 1}
{"a": 2}
  (records swapped -> 1; equal -> 0)

PART 4                              Output
SORT a:asc,b:desc                   {"b": 9}            (a missing = 0 -> smallest a)
TOP 2 a:asc,b:desc                  {"a": 1, "b": 5}    (a ties at 1 -> b descending)
{"a": 2, "b": 1}                    {"a": 1, "b": 3}
{"a": 1, "b": 3}                    {"a": 2, "b": 1}
{"a": 1, "b": 5}                    {"b": 9}            (TOP 2: first two of the same order)
{"b": 9}                            {"a": 1, "b": 5}
```
Verbatim Python asserts from the prompt (all reproduced in the tests):
```python
assert min_by_key("a", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 1, "b": 2}
assert min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
assert min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
assert min_by_key("a", [{}]) == {}
assert min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}
assert first_by_key("a", "asc", [{"a": 1}]) == {"a": 1}
assert first_by_key("a", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) in [{"b": 1}, {"b": -2}]
assert first_by_key("a", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"a": 10}
assert first_by_key("b", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": -2}
assert first_by_key("b", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": 1}
assert first_by_key("a", "desc", [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]) == {"a": 10, "b": -10}
cmp = Comparator("a", "asc")
assert cmp.compare({"a": 1}, {"a": 2}) == -1
assert cmp.compare({"a": 2}, {"a": 1}) == 1
assert cmp.compare({"a": 1}, {"a": 1}) == 0
```

## Edge cases hidden tests are known to target
- missing key = 0 sits **between** negative and positive values (`{"a": -1}` beats `{}` for min; `{}` beats `{"a": -1}` for max)
- empty record list → `None` / `null`; a single `{}` record → `{}`
- ties → first in input order for both `asc` and `desc` (do not use `<=`)
- `desc` is not "negate the value then min" if you mutate records; never modify input dicts
- the comparator must be antisymmetric: `compare(a, b) == -compare(b, a)`
- stable multi-key sort: equal keys keep input order; second key only breaks ties of the first
- large values (±10^18) and 10^5 records — O(n) for min/first, O(n log n) sort

## Variants seen in the wild
- Java signature `Map<String,Integer> minByKey(String key, List<Map<String,Integer>> records)`.
- Functional-language phrasing: `comparator(key, direction)` returns a two-argument function
  (`make_comparator` is exposed too).
- Glassdoor QTN_3113468 (Senior SWE): same three steps in a 45-minute screen.

## What this tests
skills: S02 parsing (JSON lines) · S03 records as dicts · S08 deterministic ties · S09 exact
formatting · S18 missing-key handling · S19 incremental design (re-implement via the comparator) ·
S21 stdlib fluency (`functools.cmp_to_key`, `json`)

## Sources
- https://github.com/freecodemessiah/stripe-interview (`Stripe Technical Screen.ipynb`, `Stripe-Interview.ipynb`; verbatim prompt + asserts)
- Glassdoor QTN_3113468 (Senior SWE technical screen; same min_by_key / first_by_key / comparator steps)
