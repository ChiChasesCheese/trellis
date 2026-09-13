# cd05 Business Account Data Verification — report

## Summary
A configurable rule engine over a nested `account` JSON tree: `requires` (must be non-empty),
`when` (all-match gating), `one_of` (at-least-one group), and `owners[].first_name` array
wildcards. Stripe's real onboarding flow works exactly this way — form fields aren't hardcoded,
they're driven by a rules table so compliance can add/change requirements without a deploy. The
whole difficulty is in path resolution semantics (missing vs empty vs wrong type), not algorithms.

## Sources & confidence
high for the rule schema (source gives near-verbatim JSON schema detail: `when`/`requires`/
`one_of`, path syntax, the "non-empty" definition, output format, all four numeric constraints).
2 independent mentions: `1point3acres interview/problems/ad817329-...` (full spec) and
`interview/thread/1155516` (VO write-up naming the same task, no technical detail). Worked
examples and a few undocumented behaviors (wildcard-base-missing fallback, `one_of` + wildcard
interaction) are this repo's own reconstruction — flagged explicitly in problem.md's
Clarifications section, since the source text never reproduces its own worked example verbatim.

## Approach by part
1. Part 1: `_expand()` walks a `.`-split path against the account dict; a plain `requires` list
   with no `[]` never produces more than one (path, value) pair per rule entry. Collect all
   missing tokens across rules into a `set` (dedup), `sorted()` on output.
2. Part 2: same `_expand()` now also handles `owners[]`-style wildcard segments — iterate the
   array, recurse per element with the index baked into the resolved path string
   (`owners[2].first_name`); a missing/non-list base falls back to the *unexpanded* literal path
   as a single token instead of silently doing nothing. `_when_matches()` is a separate,
   non-wildcard, single-value resolver (`equals` / `present`) since `when` conditions never need
   array fan-out in this problem's scope. `one_of` reuses the same single-value resolver: first
   path found non-empty short-circuits to "satisfied", else emit `one_of(f1|f2|...)` in
   declaration order (not sorted internally — only the whole token participates in the final
   sort).

## Pitfalls hidden tests target
- `equals` is type-sensitive (`"true"` string != `True` bool) — a naive `str(value) == v` would
  pass this incorrectly.
- `present: false` matching "path does not exist" (not "value is falsy") — easy to conflate with
  the "non-empty" definition used elsewhere.
- Empty wildcard array (`"owners": []`) is vacuously satisfied — a naive implementation might
  treat "no owners" as itself a violation.
- Wildcard base missing entirely (`owners` key absent) must NOT silently produce zero output (that
  would hide a real gap); it falls back to the literal unexpanded path.
- Dedup across rules requiring the *same* field — a naive list-append implementation double-prints.
- Sorting must be a single explicit `sorted()` over ALL tokens together (plain requires paths and
  `one_of(...)` strings interleaved), not two separately-sorted groups concatenated — the worked
  Part 2 example is specifically constructed so `one_of(...)` sorts *before* `owners[1]...`
  because `'n' < 'w'`, which would silently break under a "requires first, then one_of" ordering.
- `when` is AND over the whole condition list — one failing condition skips the entire rule, even
  if an earlier condition in the same list matched.

## Complexity & measured cost
O(total resolved path expansions), which is bounded by `rules × requires_per_rule × avg array
length` — linear in the number of JSON leaves actually visited, never more than the `account`
node-count cap (10^4) times the rule count cap (200) in the worst pathological case, and far less
in practice since most rules touch a handful of leaves. Perf test: 3000-owner account, 200 rules,
one of them fanning out over all 3000 owners — well under the 2 s / 256 MB budget (typically
< 0.1 s, a few MB, on CPython 3.12).

## Test inventory
21 tests — part1: 8 (incl. 1 io) · part2: 13 (incl. 1 io, 1 perf); edge: 8 · fmt: 2 · io: 2 ·
perf: 1.

## Skills exercised
S02 parsing (JSON, not CSV) · S03 tree path resolution · S04 grouping/dedup · S08 deterministic
sort (mixed-format tokens) · S09 exact formatting (`one_of(...)`, indexed paths) · S18 validation
rule-engine design · S19 incremental design (Part 1 → 2 adds `when`/`one_of`/wildcards)

## Review（2026-09-02）
逐条对照 `loop/tasks/review_checklist.md` 复核，结论：solution.py 在 review 前已经完全正确——21
个测试全绿（含全部 worked examples 手工逐字核对：Part 1 缺失列表、`VERIFIED` 分支、Part 2 的
`one_of(...)`/通配下标输出都精确匹配 problem.md），`IMPL=starter` 下 21 个测试全部按预期失败，
`starter.py`/`starter_template.py` 内容一致。**没有发现 F 级 bug**——路径解析、`when` 的 AND 短路、
`one_of` 的短路满足、通配数组的 vacuous-true 与缺失回退、排序去重全部与 problem.md 逐条一致。

改动（均为 S 级打磨，不改变任何输出行为）：
- `solution.py`：给 `_split`/`_when_matches`/`_missing_for_requires`/`_missing_for_one_of`/
  `part1`/`part2` 补了一句话 docstring（此前只有 `_is_nonempty`/`_expand`/`_resolve_one` 有），
  满足 checklist "docstring 一句话说清做什么"。
- `test_cd05.py`：`test_perf_large_account_and_ruleset` 里 `rng = random.Random(0)` 被创建但从未
  使用（`knocked_out` 原来是固定的 `range(0, 3000, 7)` 步长模式，flake8 F841 报未用变量）——改成
  `rng.sample(range(3000), 429)`（429 是原步长模式的元素个数，保持断言 `len(lines) ==
  len(knocked_out)` 不变），既修了 lint 又让这条 perf 用例真正符合 CONVENTIONS "perf 用
  `random.Random(0)`" 的要求，而不是名义上创建了 rng 却不用。
- `black --fix` 在 `solution.py`/`starter.py`/`starter_template.py`/`test_cd05.py` 四个文件的
  module docstring 后各加了一个空行（新版 black 风格），纯格式改动。

回归：`rtk proxy python3 -m pytest loop/rounds/06_coding_onsite/cd05_business_account_verification
--tb=short` 21 passed；`IMPL=starter` 同目录 21 failed；`loop/lint.sh
loop/rounds/06_coding_onsite/cd05_business_account_verification` 通过（black 无需改动，flake8 无
输出）。

遗留：无。这题的三处"本仓库补全"细节（数组整体缺失回退、`one_of` 不支持通配、`present` 的精确
语义）在 problem.md 的 Clarifications 里已经写清楚，solution.py 与之完全对齐，不需要进一步调整。
