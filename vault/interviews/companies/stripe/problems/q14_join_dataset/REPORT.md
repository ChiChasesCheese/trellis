# q14 Join Dataset — report

## Summary
Join a merchant's Stripe customer CSV with a legacy processor's CSV on a shared column
(`joinDataSet(fieldName, customerFile, processorFile, skipUnmatched)`): inner join, then left
join with empty processor cells, then one-to-many expansion. It is the "data-migration script"
flavour of a Stripe OA — no algorithms, only careful CSV handling (quoted commas), an O(n + m)
index, a fully specified sort (`order` numeric → input position, on both sides) and byte-exact
CSV output.

## Sources & confidence
medium — 1 independent source, new in the April-2026 rotation: programhelp.net zh_tw 2026-04-28
「Stripe OA 2026 | 4月 新題庫」 (`joinDataSet(fieldName, customerFile, processorFile,
skipUnmatched)`; P1 inner join + ordering, P2 left join with empty strings, P3 one-to-many;
catalog/raw/cn_sources.md §2.9 — article URL not captured in the research sweep).

## Approach by part
1. `parse_csv` via the `csv` module: strip header names and cells, skip blank lines, pad short
   rows / truncate long ones to the header length. Validate `field_name` in **both** headers
   (else `ValueError("missing join column '<name>'")`). Index processor rows by join value once;
   each bucket pre-sorted by `(processor order, position)`. Emit `customer + processor` rows and
   sort by `(customer order, customer position, processor order, processor position)`;
   `order_key` falls back to `(position, position)` when the column is absent or non-integer.
2. `skip_unmatched=False`: unmatched customer row emitted once with `len(processor header)`
   empty strings and sort key `(customer order, position, -1, -1)`.
3. One-to-many falls out of the bucket loop: one output row per processor match, customer
   fields repeated; duplicate customer keys are joined independently.
   `drop_duplicate_key=True` (variant) drops the processor's copy of the join column.

## Pitfalls hidden tests target
- quoted values with commas / doubled quotes must round-trip (`"Baker, Bo"`, `"He said ""hi"""`)
- `order` compared numerically (`10` after `2`), negatives allowed; non-integer `order` → position
- whitespace around header names and cells; blank lines; ragged rows
- keys and header names are case-sensitive; header-only / empty files (empty file → no columns
  → missing-column error); no matches → header only
- left join: exactly one empty cell per processor column, including the processor's key column;
  unmatched rows keep their place in the customer-order sort
- error path: nothing on stdout, message on stderr, exit 1
- 5·10^4 × 5·10^4 rows: index once, never nested loops

## Complexity & measured cost
O((n + m) log(n + m)) for the sorts, O(n + m) memory. 50k customer rows × 50k processor rows,
every key matched once (with a quoted comma in every processor row): ~0.33 s, ~121 MB RSS
(budget 2 s / 256 MB).
Measured: 0.325s, 121 MB

## Test inventory
18 tests — part1: 9 · part2: 4 · part3: 5; edge 8 · fmt 3 · perf 1 · io 1.
`IMPL=starter`: 18 fail / 0 pass.

## Skills exercised
S02 CSV parsing with quoted fields · S03 records keyed by id · S04 grouping/indexing ·
S08 deterministic multi-key sort · S09 exact CSV formatting · S18 validation / error path ·
S19 incremental design
