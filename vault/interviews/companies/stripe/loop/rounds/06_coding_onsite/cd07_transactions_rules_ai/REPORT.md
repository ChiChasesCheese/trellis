# cd07 Transactions + rules (AI Programming Exercise) — report

## Summary
A three-stage rule engine (`ALLOW|BLOCK if <condition>`) over a batch of transactions: keyword
equality, then comparison operators + `in [...]`, then a full `and`/`or`/`not`/parens
recursive-descent grammar with per-rule error reporting. It is the AI-assisted-round sibling of
`problems/q12_platform_balance_radar_rules`'s Radar grammar, deliberately smaller (no quoted
constants, no `:field:` markers, no balance ledger) since the real round budgets ~30 min with an
AI assistant instead of 75 min hand-written.

## Sources & confidence
Medium. Two independent sources (interviewdb.io's AI-programming-exercise guide, 2026-06-09;
interviewfox.ai's HackerRank OA guide, 2026) agree on the round's existence, format (HackerRank +
embedded AI chat, ~30 min), grading axis ("can you direct/verify/debug AI, do you write your own
tests"), and the problem's shape ("transactions + rules, ALLOW/BLOCK if condition, keyword match
progressing to AND/OR boolean logic"). Neither publishes a verbatim I/O sample, field list, or
exact grammar — the `RULES`/`TRANSACTIONS` stdin protocol, six-field transaction schema, `(rule
k)` output suffix, and Part 3's `ERROR line k:` reporting are this repo's reconstruction, built to
parallel `problems/q12`'s own parse→model→evaluate house style rather than invent a fourth
convention for the same skill.

## Approach by part
1. `RULE_RE` splits `ALLOW|BLOCK if <condition>` per line; Part 1's grammar restricts `<condition>`
   to a single `field == value` comparison via the `part` argument threaded through the parser.
2. Same tokenizer/parser, `part=2` unlocks `!=`, `>`, `<`, `>=`, `<=`, and `field in [v1, v2, ...]`.
   `_compare` reuses q12's own numeric-vs-string fallback rule (both sides int-parseable → compare
   numerically; else compare trimmed strings) so `amount == 0100` matches `amount == 100`.
3. `part=3` unlocks the boolean grammar (`_or` → `_and` → `_not` → `_primary`), giving `not` >
   `and` > `or` precedence for free from the recursion structure itself, and parenthesized
   sub-expressions via `_primary`'s `LP` branch. A rule that fails to tokenize or parse raises
   `RuleError`, caught per-rule so one bad line doesn't take down the batch; only Part 3 surfaces
   it as `ERROR line k: <reason>` (Parts 1/2 silently skip, since the spec's error-handling
   requirement is scoped to Part 3 only).
   Field-vs-literal resolution (`_resolve`) is per-operand, not per-rule: a bare token that names a
   known transaction column (`id`, `amount`, `currency`, `country`, `card_brand`, `merchant`) is
   looked up in the transaction; anything else is a literal string. This is what lets the grammar
   skip quoting entirely (unlike q12's `:field:`/`"const"` markers) while still supporting
   field-vs-field comparisons (`country == country`) without special-casing them.

## Pitfalls hidden tests target
- `(rule k)` line numbers must count every `RULES` line, including later-`ERROR`'d ones — a rule
  after a skipped one does not renumber down
- default (no match) has **no** `(rule k)` suffix at all, distinct from a matched rule at any k
- operator whitespace tolerance (`amount>=5000` vs `amount >= 5000`) — a naive `line.split(" ")`
  parser (the AI-generated failure mode called out in the problem's own "common mistakes" section)
  breaks on the no-space form
- `and` binding tighter than `or`, and `not` binding to only the immediately following unary/primary
  rather than an entire `and`/`or` chain — both are exercised with test cases chosen to disagree
  with the wrong-precedence reading, not just to happen to produce the same answer either way
- `in [...]` as true set membership vs. accidental substring matching (`USA` must not satisfy
  `country in [US]`)
- malformed Part 3 rules (unbalanced parens, missing operand, keyword-as-operand, bad action
  keyword) each produce exactly one `ERROR line k:` and are skipped, not fatal to the run
- 2,000 compiled rules × 20,000 transactions must not re-parse rule text per transaction (rules are
  compiled to an AST once, reused across the whole batch)

## Complexity & measured cost
O(rules) to compile once + O(transactions × matched-rule-position) to evaluate (each transaction
stops at its first matching rule). 2,000 rules / 20,000 transactions (Part 3, worst case: many
rules never match so most transactions scan deep): ~0.3 s, well under the 5 s / 256 MB budget.

## Test inventory
23 tests — part1: 6 (incl. 1 io) · part2: 5 · part3: 12 (incl. 1 io, 1 perf). edge: 14 · fmt: 1 ·
io: 3 · perf: 1.

## Skills exercised
S02 tokenizing/parsing condition strings · S06 numeric-vs-string comparison fallback · S10 ordered
rule evaluation with first-match-wins · S18 validation (per-rule `ERROR` reporting without crashing
the batch) · S19 incremental grammar (each part a strict subset of the next) · S24 Radar rule-engine
vocabulary (shared with q12, at AI-assisted-round scope) · S25 directing/reviewing AI-generated code
## 电面话术：边写边说什么
1. **读题时**：先大声确认协议边界——"`RULES` 和 `TRANSACTIONS` 两个 section 靠一行独立的 header
   区分，行数不定长；一行交易少于 6 列时，缺的列我当空字符串处理，不报错"——把隐含契约说出来。
2. **写 Part 1 前**：一句话说明分层——"我打算把条件文本的解析和对交易求值分开，这样后面加运算符、
   加布尔逻辑都只是扩展解析这一层，求值和主循环不用大改"。
3. **写 Part 2 时**：主动点出数值/字符串双轨比较——"`==`/`!=` 我先看两边是不是都能转成整数，能就按
   数字比，不能就按去空格后的字符串比，这样 `amount == 0100` 才能匹配 `amount == 100`"。
4. **写 Part 3 前**：先口头画出优先级——"`not` 最紧，然后 `and`，最后 `or`，我用递归下降实现，
   `or_expr` 调 `and_expr`、`and_expr` 调 `unary`，优先级天然由函数调用顺序保证，不用额外维护
   优先级表"。
5. **写错误处理时**：说明设计选择而不是默认行为——"题面只要求 Part 3 报 `ERROR line k`，Part 1/2
   我选择静默跳过写错的规则；如果你们希望 Part 1/2 也报错，我现在就能把这个判断放宽一行"。
6. **收尾**：主动提一句关于 AI 轮的自我审查——"如果是用 AI 生成的版本，我会重点检查三处：`in [...]`
   是不是被写成了子串匹配、`and`/`or` 优先级有没有被拍平、默认方向是不是写反成了 BLOCK"——呼应
   problem.md 里"AI 生成代码常见的五个坑"，证明这不是背答案而是真的理解每个坑背后的原因。
7. **被追问复杂度时**：「规则先编译成 AST 一次，之后对每笔交易只做树遍历，不重新解析文本；最坏情况
   是每笔交易都要扫到最后一条规则，`O(rules × transactions)`，如果规则以单字段等值判断为主，可以
   按字段建索引进一步剪枝。」
## Review（2026-09-02）
- **发现（F）**：REPORT.md 缺少 CONVENTIONS/checklist 要求的"电面话术/边写边说"节——已补上。检查
  未发现半成品痕迹（无遗留 TODO/调试 print/未完成分支），LEDGER 里"代理撞 limit 前已完成"这条记录
  与实际代码状态一致：`solution.py`/tests/starter 三件套完整、lint 干净、23 个测试全绿。
- **发现（S）**：`test_in_list_empty_single_and_several_items` 的名字承诺测了"empty"（零元素）的
  `in []` 情况，但原测试体只覆盖了 3 元素和单元素两种，没有真正测零元素——已补一条 `country in []`
  永不匹配的断言。problem.md 缺少本仓库其它题目都有的"面试官会怎么追问"节——已补 6 条，覆盖 AI 轮
  评分标准、优先级实现位置、语法扩展性、错误处理的题面 vs. 自选边界、最坏复杂度、字段/字面量判定
  依据这几个方向。
- **未改动**：`solution.py` 本身未发现 F 级问题——tokenizer/parser/evaluator 三层分离清晰，
  worked examples 逐字核对全部通过，lint（black -l 110 + flake8 F 类）一次性通过，无需 `--fix`。
- **遗留**：无。`_compare` 对 `==`/`!=` 的数值兜底目前对 Part 1/2/3 统一生效，problem.md 的 Part 1
  措辞（"值按去空格字符串比较"）与 Part 2 措辞（"两边都能转成整数就按数字比"）在字面上略有张力，
  但两种解释在所有 worked examples 和当前测试上给出相同结果，本次未改动此行为，仅在这里记录供后续
  如需收紧 Part 1 语义时参考。
