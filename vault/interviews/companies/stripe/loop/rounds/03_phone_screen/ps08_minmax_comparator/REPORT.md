# ps08 Min/Max with comparator — report

## Summary
A four-part progression from "get the min" to "get the min or max by any field" to "get the
extreme under an arbitrary caller-supplied ordering" to "what if more than one record is tied".
It is a compact tour of a real API-design decision Stripe engineers make constantly: when does a
single `key`/`mode` parameter stop being enough, and you need a full comparator instead? Part 3's
worked example is built specifically to make that concrete — the canonical comparator picks a
*different* winner than Part 1's simpler rule on the exact same tie, because it can express a
composite (amount, then created_at) ordering that a single field cannot.

## Sources & confidence
medium — rampatra's 2020-01 Dublin phone-screen writeup (`loop/raw/en_forums.md` section 3.3, P14)
verifies the four-part shape verbatim ("Part 1: take the min value record; Part 2: return min or
max based on a parameter; Part 3: use a comparator; Part 4: handle ties") but does not include a
record schema or sample I/O. This report's record shape (`id, amount, created_at, country`), all
worked numbers, and the exact tie-break rules are a reconstruction chosen to be Stripe-flavored
and to make Part 3 genuinely diverge from Part 1 on a hand-checkable example -- see Open points.

## Approach by part
1. `min_by_amount`: one linear scan, replace `best` only on strict improvement -- this both finds
   the minimum and gives "first on tie" for free without a separate tie-break pass.
2. `extreme(records, key, mode)`: same scan shape, generalized via a small `_key_extractor(key)`
   dispatch (amount -> Decimal compare, created_at -> datetime compare, country -> string
   compare) and a `mode` switch; unknown key/mode raise `ValueError` rather than silently
   returning a wrong answer.
3. `extreme_with(records, comparator)`: the same linear-scan shape again, but the comparison
   itself is delegated to the caller's `comparator(a, b) -> int`. Deliberately a scan, not
   `min(records, key=functools.cmp_to_key(comparator))` -- discussed in the interview talk track
   below. `main()`'s `PART 3` uses a canonical `by_amount_then_created_at` comparator specifically
   because it needs two fields with independent tie-break order, which Part 2's interface cannot
   express.
4. `extreme_all(records, key, mode)`: two passes over the same `(key, mode)` interface as Part 2
   -- first find the extreme value, then collect every record whose extracted value equals it,
   sorted by `id`. This is the one place the tie-break *contract* changes on purpose (return
   every tied record instead of the first) and that change is called out explicitly rather than
   left implicit.

## Pitfalls hidden tests target
- empty input -> `NONE` on every part, never an exception or an empty print
- `Decimal` amount comparison, never `float` (negative amounts/refunds included)
- `created_at` parses both `Z` and an explicit numeric offset and compares them as the same
  instant
- Part 4's `id` sort is plain string order (`"B" < "a"`, `"user10" < "user2"`), not
  case-insensitive or numeric-aware -- same rule as q03's user-id sort, deliberately reused
- duplicate `id`s are not deduplicated -- if both members of a duplicate pair are tied for the
  extreme, both appear in Part 4's output
- Part 3's comparator argument order and sign convention matches C/`qsort`/`cmp_to_key`
  (`negative` = a before b); a comparator that only inspects one non-`amount` field must still
  work, since `extreme_with` makes no assumption about which fields the comparator uses
- Part 1/2/3 vs Part 4 tie-break divergence: Parts 1-3 always resolve to exactly one id (first in
  input order); Part 4 is the only part that returns more than one line, and only when tied
- Part 3's canonical `by_amount_then_created_at` picks a different winner than Part 1's
  `min_by_amount` on the same tied pair -- both are individually correct under their own stated
  rule, and a test locks in that divergence rather than treating it as a bug
- unknown `key`/`mode` strings raise `ValueError`

## Complexity & measured cost
Parts 1-3: `O(n)` -- a single linear scan, no sort. Part 4: `O(n)` to find the extreme value plus
`O(k log k)` to sort the `k` tied ids (`k <= n`), never a full `O(n log n)` sort of all records
when only the extreme (or the tied set) is needed. Measured: 100,000 records with a narrow
amount range (many ties by construction), Part 4 end-to-end (stdin -> stdout) well under 2 s,
comfortably under the 256 MB budget -- see `test_perf_100k_records`.

## Test inventory
33 tests -- part1: 9 . part2: 8 . part3: 7 . part4: 9 (incl. 6 io, 1 perf); edge 11 . fmt 1 .
io 6 . perf 1.

## Skills exercised
S03 modeling records as a small typed structure (NamedTuple), not raw CSV lines . S08
deterministic ordering with an explicit tie-break that changes on purpose in Part 4 . S12
timestamp parsing/comparison (Z vs explicit offset) . S19 incremental design (Part 4 wraps Part
2's interface; Part 3 stands apart as the more general mechanism) . S21 stdlib fluency (Decimal,
datetime.fromisoformat, functools.cmp_to_key discussed but not used, in favor of a linear scan)

## Interview talk track: what to say while writing
1. **Reading the prompt**: confirm the tie-break rule for each part before coding -- "first in
   input order" for Parts 1-3, versus "return everyone" for Part 4 -- and say explicitly that
   these are two different contracts, not an inconsistency to paper over.
2. **Writing Part 1**: note out loud that a single `if val < best_val: best = val` scan gives you
   both the minimum and the "first on tie" rule simultaneously, with no separate tie-break pass
   needed -- cheap to say, and it preempts "how do you handle ties" before it's asked.
3. **Writing Part 2**: mention the `ValueError` on an unknown key/mode as a deliberate choice --
   "I'd rather fail loudly on a typo'd key than silently compare nothing and return a wrong
   answer."
4. **Writing Part 3**: this is the part to slow down on. Say why a hand-rolled linear scan is
   used instead of `min(records, key=functools.cmp_to_key(comparator))`: both are effectively
   `O(n)` here, but the scan keeps the tie-break rule in one visible `if` condition and avoids
   wrapping every record in a `cmp_to_key` object; if you needed the full sorted order for
   something else, `cmp_to_key` would be the right call, but for a single extreme it's doing more
   work than the problem needs. Then walk through the r2/r3 tie by hand to prove the comparator
   picks a genuinely different (and correct) answer than Part 1.
5. **Writing Part 4**: point out this is the only part where the contract itself changes -- "I'm
   not retrofitting ties into Parts 1-3's single-winner functions; Part 4 is a new function with
   a new return type, and I built it directly on Part 2's key/mode extraction so the two stay in
   sync."
6. **Wrapping up**: run the worked examples by hand, then proactively raise the natural follow-up
   -- "if you wanted ties under a comparator instead of just key/mode, I'd swap the equality check
   in extreme_all for `comparator(record, best) == 0`, sketch that instead of writing it" -- this
   is exactly the kind of unprompted edge-surfacing interviewers reward.

## Open points
- Only the four-part shape and its one-line-per-part description are verified from the source;
  the record schema, field names, and every worked number in this problem.md are a reconstruction
  chosen to be internally consistent and hand-checkable. If a transcript with real sample I/O
  surfaces, reconcile the schema and numbers against it.

## Review（2026-09-02）
- 逐条对照 `loop/tasks/review_checklist.md` 复核：problem.md 四个 Part 的全部 worked examples（Part 1
  单值、Part 2 四组 key/mode、Part 3 比较器、Part 4 两组并列、空输入 `NONE`）已用 `solution.py` 逐字
  重跑核对（stdin → stdout），全部与文档一致，未发现规则歧义。
- `solution.py` 逻辑复核：`min_by_amount`/`extreme`/`extreme_with` 三者都是同一个"严格更优才替换"的
  单趟扫描骨架，平局天然保留输入序中先出现的记录，无需额外 tie-break 分支；`extreme_with` 未对
  comparator 做任何字段假设（`test_extreme_with_custom_comparator_ignores_amount` 覆盖）；`extreme_all`
  两趟扫描复用 `_key_extractor`，不复用单赢家函数（返回类型不同，独立实现是对的）；未知 `key`/`mode`
  均正确抛 `ValueError`；`created_at` 的 `Z`/显式偏移量归一化正确比较为同一时刻；未发现功能性 bug
  （F 项 0 处需修）。`starter.py`/`starter_template.py` 内容仍完全一致，公共 API 与 `solution.py` 一致。
- 修复：`loop/lint.sh --fix` 对 `solution.py`/`starter.py`/`starter_template.py` 做了纯格式化（模块
  docstring 后补一行空行，本地 black 版本差异导致），无语义变化；`loop/lint.sh` 复检通过（black 110 列
  + flake8 F 类 0，flake8 单独核实无任何警告）。
- 回归：`rtk proxy python3 -m pytest loop/rounds/03_phone_screen/ps08_minmax_comparator --tb=short`
  33 passed；`IMPL=starter` 同目录 26 failed / 7 passed（余下 7 处全部是"空输入 → None/NONE"的平凡
  用例，starter 桩代码的默认返回值恰好满足，不构成空洞测试）。
- 遗留：无功能性遗留项。问题面来源置信度为 medium（仅四段的一句话描述可验证，具体字段名/schema/worked
  numbers 为本仓库重构），problem.md 的 Open points 已如实标注，不需要在代码侧处理。
- 文章：`loop/study/30-articles/ps08_minmax_comparator.md`（152 行）。
