# q14 · Join Dataset — merge a legacy processor's export into Stripe customer data

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 3 parts) · **Last asked:** 2026-04 (programhelp zh_tw 2026-04-28 "Stripe OA 2026 | 4月 新題庫")
**Frequency:** 1 independent source (new problem in the April-2026 rotation) · **Confidence:** medium

## Context
A merchant is migrating from a legacy payment processor to Stripe. Stripe has a CSV export of the
merchant's customers; the legacy processor has its own CSV export keyed by the same identifier
(a customer id, an email, …). Before the migration can finish, the two datasets have to be joined
on that shared field so every Stripe customer row is paired with the processor's record(s) for it.
This is the "data-migration script" flavour of a Stripe OA: no algorithms, just careful CSV
handling, a join, a deterministic sort, and exact output.

## API
```
join_dataset(field_name: str, customer_csv: str, processor_csv: str, skip_unmatched: bool = True) -> str
```
Both inputs are the full text of a CSV file (first row = header). The result is CSV text
(header + rows, `\n`-terminated lines, standard `csv` quoting: a value containing `,` or `"` is
quoted). Header-only inputs are legal and produce a header-only output.

## Input (stdin protocol for `main()`)
```
JOIN <field_name> <true|false>      # third token = skip_unmatched
<customer CSV, header first>
---
<processor CSV, header first>
```
Header names and cell values are stripped of surrounding whitespace. Blank lines inside a CSV are
ignored. A data row shorter than its header is padded with empty strings; a longer one is
truncated. Values are matched **exactly and case-sensitively** after stripping.

## Output
CSV text. Columns = **all customer columns, in order, followed by all processor columns, in
order** (the join column therefore appears twice — once per side — exactly as the sources describe
"customer file's columns + processor file's columns"). Rows sorted as described in Part 1.

## Rules
### Part 1 — inner join
Emit one row for every (customer row, processor row) pair whose `field_name` values are equal.
Customer rows with no processor match are dropped (`skip_unmatched=True`).
**Sort:** by the customer file's `order` column (numeric, ascending), then by the customer row's
input position, then by the processor file's `order` column (numeric), then by the processor row's
input position. `order` values are integers; if a file has no `order` column, or a value is not an
integer, that row's input position is used instead — so the output is always deterministic.

### Part 2 — left join
`skip_unmatched=False`: every customer row is kept. A customer row with no processor match is
emitted once with **empty strings in every processor column** (including the processor's copy of
the join column). Sorting is unchanged.

### Part 3 — one-to-many
A customer row that matches several processor rows produces one output row **per processor row**,
with the customer's fields repeated on each; the matches are ordered by the processor `order`
column (then processor input position). Duplicate keys on the customer side are treated the same
way: each customer row is joined independently.

### Error path
If `field_name` is not a column of **both** files, `join_dataset` raises `ValueError("missing join
column '<field_name>'")`; `main()` prints that message to stderr and exits with status 1, printing
nothing to stdout. An empty file (no header row at all) has no columns and therefore triggers the
same error.

## Worked examples
**Example 1 — Part 1, inner join** (`join_dataset("customer_id", C, P, True)`)
```
C:                          P:
customer_id,name,order      customer_id,ref,order
c1,Alice,2                  c2,p-200,1
c2,Bob,1                    c1,p-100,2
c3,Carol,3                  c9,p-900,3
```
Output (c3 and c9 have no partner; c2's customer `order` 1 sorts before c1's 2):
```
customer_id,name,order,customer_id,ref,order
c2,Bob,1,c2,p-200,1
c1,Alice,2,c1,p-100,2
```

**Example 2 — Part 2, left join** (same files, `skip_unmatched=False`)
```
customer_id,name,order,customer_id,ref,order
c2,Bob,1,c2,p-200,1
c1,Alice,2,c1,p-100,2
c3,Carol,3,,,
```

**Example 3 — Part 3, one-to-many with a quoted comma**
```
C:                          P:
email,name,order            email,charge,order
a@x.com,Ann,1               b@x.com,ch_3,3
b@x.com,"Baker, Bo",2       a@x.com,ch_2,2
                            a@x.com,ch_1,1
```
Output (Ann's two charges ordered by processor `order`; the quoted name survives round-trip):
```
email,name,order,email,charge,order
a@x.com,Ann,1,a@x.com,ch_1,1
a@x.com,Ann,1,a@x.com,ch_2,2
b@x.com,"Baker, Bo",2,b@x.com,ch_3,3
```

**Example 4 — header-only processor file, left join**
`join_dataset("id", "id,name,order\n1,Ann,1\n", "id,ref,order\n", False)` →
```
id,name,order,id,ref,order
1,Ann,1,,,
```

## Edge cases hidden tests are known to target
- header-only customer file → header-only output (still both headers concatenated)
- quoted fields containing commas / quotes must round-trip unchanged
- whitespace around header names and cells (` customer_id `) must not break matching
- `order` sorted **numerically** (`10` after `2`), not as strings
- ties on customer `order` → input position; ties on processor `order` → input position
- left join: unmatched rows get exactly `len(processor header)` empty cells
- one-to-many: customer values repeated verbatim on each row
- keys are case-sensitive (`C1` ≠ `c1`)
- join column missing in either file → error, nothing on stdout
- 10^5 rows per file: index the processor file by key once (O(n + m)), never nested loops

## Variants seen in the wild
- Only one copy of the join column in the output (processor's copy dropped). Supported by the
  keyword flag `drop_duplicate_key=True` on `join_dataset`.
- Function name in camelCase, `joinDataSet(fieldName, customerFile, processorFile, skipUnmatched)`,
  taking file paths instead of CSV text — same logic.

## What this tests
skills: S02 parsing (CSV, quoted fields) · S03 modelling records keyed by id · S04 grouping · S08
deterministic sort with full tie-break · S09 exact formatting · S18 validation/error path · S19
incremental design

## Sources
- programhelp.net zh_tw 2026-04-28 「Stripe OA 2026 | 4月 新題庫」 — `joinDataSet(fieldName, customerFile,
  processorFile, skipUnmatched)`; P1 inner join + ordering, P2 left join with empty strings, P3 one-to-many
  (catalog/raw/cn_sources.md §2.9; article URL not captured in the research sweep)
