# q42 · Loose-Schema Record Aggregation — unknown fields, last-key-wins, schema inference

> ⚠️ **重建题（题面来自二手转录）**：本题面基于 1point3acres 的题目转录
> （https://www.1point3acres.com/interview/problems/621a72d2-59c8-498a-b252-50be658c6aae，
> 2026-04-13），转录文件开头自陈是 "as it would be delivered by the interviewer" ——
> **是转录者的重构，不是候选人逐字记录**。题材、part 划分、考点方向可信（解析可变字段的
> `key=value` 行、按 currency/任意 key 聚合、schema 推断）；**输入输出的精确格式、字段名、
> 样例数值是本仓库重新拟定的，不要当真题格式去背**。

**Type:** Stripe OA (coding, take-home style) · **Stage:** OA / phone screen ·
**Last asked:** 2026-04-13 (per 1p3a mirror date; may lag the real ask date)
**Frequency:** 1（1p3a 镜像单条，未见其他独立来源）· **Confidence:** medium
（题材/part 划分来自一份完整转录，但转录自陈是重构，非逐字候选人记录；格式与样例本仓库自拟）

## Sources
- https://www.1point3acres.com/interview/problems/621a72d2-59c8-498a-b252-50be658c6aae
- 本仓库镜像副本：`catalog/raw/mirror_1p3a_stripe/coding/009__20260413__parse_and_aggregate_records_with_potentially_unknown_fields__oj_621a72d2.txt`
- 抓取日 2026-09-03；镜像仓库自身 commit 日期 2026-06-01（**它也有滞后**）

## 上游给到的内容 vs. 本仓库自拟的内容
上游转录给了完整的三段 PART 划分、每条规则的文字描述（key/value 语法、字段顺序不保证、未知
key 忽略、同 key 重复取最后一次、amount 非负整数校验、group-by 的 `__none__` 兜底、SCHEMA 段
的用途）、Part 1/2 的输入输出样例，以及"Interviewer notes"里对实现结构的期望（parse 产出
`dict`、校验函数单独一个、聚合函数复用于 Part 2/3）。**这些都被原样保留在下面的 Rules 里。**
上游**没有**给 Part 3 的样例（原文只说"加一个 SCHEMA 块"，没给具体输入输出对）、没有给 Part 3
的 header 形状是否要继续带 `group_by_key`、也没有给字段/值长度以外更细的畸形行处理规则（比如
一个 token 没有 `=` 时怎么办）。**这几处是本仓库按上游"Interviewer notes"里的口径（宽松解析、
跳过不报错）自行补全的**，Worked examples 里会明确标出哪些是上游原样、哪些是本仓库新增。

## Context
An upstream payments pipeline emits loosely-typed records: each row is a bag of `key=value`
pairs, the set of keys varies row to row, and new keys appear over time without a schema
migration. Downstream tooling has to be tolerant of that — parse whatever is there, ignore keys
it doesn't understand, and still produce a reliable aggregate. This is the "webhook payload from
a system you don't control" shape that shows up constantly in payments integrations.

## Input (stdin)
```
PART n
<header line>
<record line>
...
```
`PART n` selects which part to run (`1`, `2`, or `3`). The header line and the `N` record lines
that follow are as described per part below. A line may have leading/trailing whitespace —
trim it before splitting on whitespace.

Each record line is zero or more space-separated `key=value` tokens:
```
id=1 amount=10 currency=USD
id=2 amount=5 currency=USD region=NA
id=3 currency=EUR amount=7 source=batch
```
- Keys are alphanumeric/underscore; values contain no spaces.
- Field order within a record is **not guaranteed**.
- Unknown keys are ignored for aggregation purposes (but still counted in Part 3's schema).
- If the same key appears more than once on one line, the **last** occurrence wins.
- A token with no `=` in it, or with an empty key (a token starting with `=`), is a malformed
  token: skip that token (do not fail the whole line, do not fail the whole input) — this is the
  repo's own extension of "be tolerant," since the upstream prompt does not specify it, but its
  "Interviewer notes" say to stay loose, so a silently-dropped bad token is more in the spirit of
  the problem than crashing.

## Output
One `str` per output line via `part1`/`part2`/`part3`; `main()` joins them with `\n` and writes
to stdout (trailing newline only if there is at least one line).

## Rules

### Part 1 — total amount per currency
Header line: a single integer `N` (`0 <= N <= 200_000`), the number of records that follow.

For each record, the relevant fields are `amount` (a non-negative integer, in the smallest
currency unit, up to `10**15`) and `currency` (any non-empty token — treat it as an opaque ISO
code, don't validate its shape). A record is **valid** for this part iff it has a non-empty
`currency` **and** `amount` parses as a non-negative base-10 integer (no leading `+`, no
underscores, no decimal point — `int()`-parseable and `>= 0`). Invalid records are skipped, not
errors.

Output: one line per currency that had at least one valid record, sorted alphabetically by
currency code ascending:
```
<currency> <total_amount>
```

### Part 2 — group by an arbitrary key
Header line: `<N> <group_by_key>` — `N` as above, then the name of one field to bucket by, in
**addition to** currency (e.g. `group_by_key=region` sums amounts per `(region, currency)`).

Same validity rule as Part 1 (must have `currency` and a non-negative integer `amount`). If a
valid record is missing `group_by_key`, classify it under the literal group `__none__`.

Output: one line per `(group, currency)` pair that had at least one valid record, sorted by
`(group, currency)` lexicographically ascending:
```
<group> <currency> <total_amount>
```

### Part 3 — schema inference
Header line: same shape as **either** Part 1 (`N`) or Part 2 (`N group_by_key`) — Part 3 is a
strict superset of whichever grouping was requested, so re-run Part 1 or Part 2's totals logic
(whichever the header shape implies) and then append a schema block.

After the per-currency (or per-group) total lines, print:
```
SCHEMA
<key1> <count1>
<key2> <count2>
...
```
Listing **every** key seen anywhere in the input — including unknown keys, and including keys
from records that were skipped as invalid for the amount aggregation — sorted alphabetically,
with `count` = the number of records that contained that key at least once (a key repeated
within one record via last-wins still counts as **one** record for that key's count, not one
count per occurrence). Use the exact literal header `SCHEMA` on its own line so a downstream tool
can find the split point.

## Worked examples
The first two are the upstream's own examples (values unchanged; only wrapped in this repo's
`PART n` / header framing). The Part 3 example is this repo's own addition (see "上游给到的内容"
above — the upstream never worked one).

```
# Part 1 (upstream example)
PART 1
4
id=1 amount=10 currency=USD
id=2 amount=5 currency=USD
id=3 amount=7 currency=EUR
id=4 currency=USD
-->
EUR 7
USD 15
```
(`id=4` has no `amount` -> skipped, not an error.)

```
# Part 2 (upstream example)
PART 2
5 region
id=1 amount=10 currency=USD region=NA
id=2 amount=5 currency=USD region=NA
id=3 amount=7 currency=EUR region=EU
id=4 amount=4 currency=USD
id=5 amount=3 currency=USD region=EU
-->
EU EUR 7
EU USD 3
NA USD 15
__none__ USD 4
```

```
# Part 3 (this repo's own example)
PART 3
3
id=1 amount=10 currency=USD
id=2 amount=5 currency=USD extra=x
id=3 currency=EUR
-->
USD 15
SCHEMA
amount 2
currency 3
extra 1
id 3
```
(`id=3` is missing `amount` so it contributes nothing to the `USD`/`EUR` totals -- there is no
`EUR` line at all, since no valid record used it -- but its `id` and `currency` keys still count
toward SCHEMA, per the "warts and all" rule.)

## Edge cases hidden tests are known to target
- `N == 0`: no record lines at all; Part 1/2 print nothing before their (absent) totals, Part 3
  prints just `SCHEMA` with no keys under it (empty output for Part 1/2, `["SCHEMA"]` for Part 3).
- A record with zero tokens (blank line among the `N` record lines) is a record that contributes
  no keys to the schema and is invalid for aggregation (missing both `amount` and `currency`).
- Duplicate keys on one line: `id=1 amount=5 amount=9 currency=USD` -> `amount=9` wins.
- Field order shuffled across records that should still merge into the same currency/group.
- `amount=0` is valid (non-negative includes zero); `amount=-1` is invalid (skip, don't crash);
  `amount=abc` and `amount=` (empty value) are both invalid (skip).
- `currency=` (present but empty) is treated as missing -- invalid, skipped (matches the
  upstream's own reference implementation, which strips and checks truthiness).
- Unknown keys (not `id`/`amount`/`currency`/the group key) are ignored for totals but still
  appear in Part 3's SCHEMA.
- Part 2: a record missing the `group_by_key` field entirely groups under `__none__`; a record
  where `group_by_key` is present but empty-string also groups under the literal empty string
  `""` (that is a real, distinct value from `__none__` -- presence of the key is what matters,
  not truthiness, unlike `currency`).
- Part 3: a key that appears twice in one record (duplicate token, last wins) contributes `1` to
  that key's SCHEMA count for that record, not `2`.
- A malformed token (no `=`, or an empty key) inside an otherwise fine record: that one token is
  dropped, the rest of the record still parses and can still be valid.
- Very large `amount` values (up to `10**15`) summed across up to `2*10**5` records must not
  lose precision -- use plain Python `int`, never `float`.

## Variants seen in the wild
None independently confirmed — this transcript is the only source found for this exact prompt.
The general shape ("parse loosely-typed key=value records, tolerate unknown/missing fields,
aggregate") is common across Stripe-flavored OAs that touch webhook or ledger-adjacent data (see
`q01`, `q16`'s malformed-line tolerance, and `q38`'s feature-flag key handling) but none of those
are claimed as the same problem.

## What this tests
skills: **S02** line-oriented `key=value` parsing with an explicit last-wins rule for duplicate
keys and a documented malformed-token skip · **S03** modeling a record as a loose `dict` rather
than a rigid class, by design (the problem's whole point) · **S04** group-by aggregation that
generalizes from "no group" (Part 1) to "one extra grouping key" (Part 2) without restructuring
the aggregation function · **S05** validity gating (non-negative integer `amount`, non-empty
`currency`) applied once and reused unchanged across parts · **S08** deterministic multi-key sort
(`currency` alone, then `(group, currency)`) · **S09** exact output formatting (`SCHEMA` as a
literal section marker; no trailing decorations) · **S18** validation/error paths that skip
rather than crash (missing keys, non-integer amounts, empty values) · **S21** stdlib fluency
(`dict`/`defaultdict`, no custom classes needed) · **S24** domain literacy (loosely-typed webhook
/ ledger-style payloads with evolving schemas, an extremely common real Stripe integration shape).
