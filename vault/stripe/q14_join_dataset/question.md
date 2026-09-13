# q14 · Join Dataset — merge a legacy processor's export into Stripe customer data

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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
