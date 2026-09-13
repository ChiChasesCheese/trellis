---
nodes: [input.delimited, output.ordering, transfer.stripe-oa]
tags: [stripe-oa, q14]
---
# Drill: join a legacy processor's export into Stripe customer data

Sixty minutes. Implement `join_dataset(field_name, customer_csv, processor_csv,
skip_unmatched=True) -> str`: two CSV files (full text, header first) keyed by a shared field,
joined into one CSV whose columns are every customer column followed by every processor column.
Part 1 is an inner join with a fully specified four-level sort. Part 2 turns it into a left join:
an unmatched customer row is still emitted once, with every processor column empty. Part 3 is
one-to-many: a customer row matching several processor rows produces one output row per match,
customer fields repeated, ordered by the processor side's own sort key.

**Constraints to state and honor**
- Both inputs are full CSV text; standard quoting applies on both read and write (values with
  commas or quotes round-trip through the `csv` module, not string splitting); header names and
  cell values are stripped; a short row is padded, a long one truncated to header length;
  matching is exact and case-sensitive.
- Sort key is four levels: customer `order` column (numeric ascending, falling back to input
  position if absent or non-integer), then customer input position, then processor `order`
  column the same way, then processor input position.
- `field_name` missing from either file's header raises `ValueError("missing join column
  '<field_name>'")`; the stdin driver prints that to stderr, exits 1, and prints nothing to
  stdout — an empty file (no header at all) hits this same path.
- Up to 10^5 rows per file; must index one side by key once, never a nested-loop join.

**Grading points**
- Building a dict/defaultdict index over the processor rows once, each bucket pre-sorted by its
  own `(order, position)` key, so the whole join is O(n + m) rather than quadratic.
- Using the stdlib `csv` module on both the read and write side — a hand-rolled `split(",")`
  silently breaks the moment a value contains a comma or an embedded quote.
- The sort key's fallback rule stated explicitly: no `order` column, or a non-integer value in
  it, degrades to input position, which is what keeps the whole ordering deterministic instead of
  implementation-defined.
- Left-join padding produces exactly `len(processor header)` empty cells, including the
  processor's own copy of the join column — not zero cells, not customer-header-length cells.
- The error path prints nothing on stdout in the failure case — a candidate who lets partial
  output leak before raising loses this silently in hidden tests.
- One-to-many is not a special case of the code — it falls out of iterating the whole processor
  bucket instead of taking its first element.

**Source**
- `vault/Quick_Check/problems/q14_join_dataset/problem.md`, `vault/Quick_Check/problems/q14_join_dataset/REPORT.md`, `vault/stripe/q14_join_dataset/question.md`, `vault/stripe/q14_join_dataset/solution.md`, `vault/Quick_Check/study/10-solutions/q14_join_dataset.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
