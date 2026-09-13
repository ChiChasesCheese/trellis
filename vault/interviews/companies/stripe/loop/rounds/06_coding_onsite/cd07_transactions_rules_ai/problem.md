# cd07 · Transactions + Rules (AI Programming Exercise) — keyword match → comparisons → AND/OR/NOT

**Type:** onsite "AI Programming Exercise" (2026 新增轮，HackerRank 内嵌 AI 聊天窗口) · **Stage:** ~30 min with AI assistance ("kind of like a lightweight Cursor") / this repo also drills it as a 60 min hand-written round, 3 parts · **Last asked:** 2026-06-09 write-up (rolling, "recently added" as of that date) · **Frequency:** 2 independent mentions (interviewdb.io AI-exercise guide; interviewfox.ai OA/HackerRank guide) plus `en_forums.md` §9's own collation (C11) · **Confidence:** medium — the progression ("keyword/string match → AND/OR boolean logic, multi-stage") and the grading criteria (can you direct/verify/debug the AI, do you write your own tests) are both named explicitly by two independent sources; the exact input protocol, field list, and worked numbers are this repo's reconstruction (no verbatim I/O sample is public).

## Context
Stripe's 2026-added "AI Programming Exercise" round drops candidates into a HackerRank environment
with an embedded AI chat panel and grades **how you direct it**, not whether you can type fast.
The task itself is deliberately ordinary — a rules-based transaction filter, structurally the same
shape as Radar's real rule engine (see `problems/q12_platform_balance_radar_rules` for the
`ACCEPT`/`BLOCK if (:field: = "const")` production version) but smaller: no quoted constants, no
`:field:` markers, no `API:`/`BAL:` balance ledger — just `ALLOW|BLOCK if <condition>` rules
evaluated against a batch of transactions, three parts, each adding one layer of expressiveness.
This directory intentionally does **not** duplicate q12's grammar or its balance-ledger Part 1 —
treat the two as siblings testing the same rule-engine skill at different levels of AI-assisted vs.
hand-written pacing.

## Input (stdin)
First line `PART n` (n ∈ 1..3). Then two sections, in this fixed order, header on its own line;
blank lines ignored everywhere:
```
RULES
ALLOW|BLOCK if <condition>          one rule per line, in registration order
TRANSACTIONS
id,amount,currency,country,card_brand,merchant
```
`amount` is a non-negative integer (cents); `currency`, `country`, `card_brand`, `merchant` are
bare alphanumeric/underscore tokens (no embedded commas, no embedded spaces — this protocol has no
CSV quoting). A transaction row with fewer than 6 columns has its missing trailing columns treated
as empty strings. Up to 10^5 rule lines and 10^5 transaction rows.

## Output
One line per transaction, **in input order**: `id ALLOW (rule k)` or `id BLOCK (rule k)` where `k`
is the **1-indexed line number of the matching rule within the `RULES` block** (counting every
rule line, including ones later skipped as invalid in Part 3 — the numbering is stable regardless
of what else in the file failed to parse). If no rule matches, the line is just `id ALLOW` — no
`(rule k)` suffix; there is no rule to cite. (Part 3 also prints `ERROR line k: <reason>` lines,
emitted once per invalid rule at parse time, all before any transaction output — see Part 3.)

## Rules
### Part 1 — keyword equality
`<condition> := <field> == <value>` only. `<field> ∈ {id, amount, currency, country, card_brand,
merchant}`; `<value>` is a bare token compared as a trimmed string (so `amount == 10000` still
works even though `amount` is numeric — the digits compare equal as strings). Rules are evaluated
**in registration order; the first rule whose condition is true decides**. No match → default
`ALLOW`.

### Part 2 — comparisons and `in`
`<condition>` gains five more operators — `!=`, `>`, `<`, `>=`, `<=` — plus a membership form:
`<field> in [v1, v2, v3]` (spaces after commas and around brackets are optional). Still exactly one
comparison per rule (no boolean combinators yet — that's Part 3). Whitespace around the operator
is optional in every case (`amount>=5000`, `amount >= 5000`, `amount>= 5000` all parse the same).
Comparison semantics (reused by Part 3 too): for `==`/`!=`, if **both** sides parse as integers,
compare numerically (`amount==0100` matches `100`); otherwise compare the trimmed strings. The
ordering operators (`>`, `<`, `>=`, `<=`) are only exercised against `amount` (the one numeric
field) — parse both sides as integers. `in [...]` compares the field's string form against each
literal in the list (`country in [US, CA, MX]`).

### Part 3 — AND / OR / NOT / parentheses
Recursive-descent grammar, **`not` binds tighter than `and`, which binds tighter than `or`**
(keywords `and`/`or`/`not`/`in` case-insensitive; field names, `ALLOW`/`BLOCK`, and values are
case-sensitive):
```
expr        := or_expr
or_expr     := and_expr ("or" and_expr)*
and_expr    := unary ("and" unary)*
unary       := "not" unary | primary
primary     := "(" expr ")" | comparison
comparison  := field OP value | field "in" "[" value ("," value)* "]"   # OP as in Part 2
```
A `field` token is any name in `{id, amount, currency, country, card_brand, merchant}`; any other
bare token in operand position is a literal value (this is how the grammar tells "compare against
the transaction's `country`" apart from "compare against the literal string `country`" without
needing quotes). `not` applies to the single following `unary` (so `not a and b` is `(not a) and
b`, not `not (a and b)`). A rule whose condition fails to parse — bad operator, unbalanced
parens, trailing garbage, a keyword used where an operand was expected, etc. — emits
**`ERROR line k: <reason>`** (k = that rule's 1-indexed line number within `RULES`) and the rule is
**skipped** (never matched against any transaction, and later rules' line numbers are unaffected).
`<reason>` text is implementation-defined; hidden tests check the `ERROR line k:` prefix and the
line number, not the exact wording.

## Worked examples
### Part 1
```
RULES
ALLOW if country == US
BLOCK if amount == 10000
TRANSACTIONS
t1,500,USD,US,visa,acme
t2,10000,USD,CA,visa,acme
t3,700,USD,FR,visa,acme
```
→
```
t1 ALLOW (rule 1)
t2 BLOCK (rule 2)
t3 ALLOW
```

### Part 2
```
RULES
BLOCK if amount > 5000
ALLOW if country in [US, CA]
BLOCK if currency != USD
TRANSACTIONS
t1,6000,USD,US,visa,acme
t2,3000,USD,MX,visa,acme
t3,3000,EUR,FR,visa,acme
t4,3000,USD,CA,visa,acme
```
→
```
t1 BLOCK (rule 1)
t2 ALLOW
t3 BLOCK (rule 3)
t4 ALLOW (rule 2)
```
(`t2`: amount not over 5000, country MX not in the list, currency USD is not `!= USD` — no rule
fires, default ALLOW.)

### Part 3
```
RULES
BLOCK if country == US and amount > 5000
ALLOW if (country == CA or country == MX) and not currency == EUR
BLOCK if amount >
TRANSACTIONS
t1,6000,USD,US,visa,acme
t2,3000,USD,CA,visa,acme
t3,3000,EUR,CA,visa,acme
t4,100,USD,FR,visa,acme
```
→
```
ERROR line 3: expected a field or value
t1 BLOCK (rule 1)
t2 ALLOW (rule 2)
t3 ALLOW
t4 ALLOW
```
(`t3`: rule 1 false (country isn't US); rule 2's `not currency == EUR` is false because currency
*is* `EUR`, so the whole `and` is false; rule 3 was dropped as invalid — no rule matches, default
ALLOW. `t4`: nothing matches — FR isn't CA or MX — default ALLOW.)

```python
part3(["RULES", 'BLOCK if not country == US', "TRANSACTIONS", "t1,0,USD,CA,visa,acme"]) == ["t1 BLOCK (rule 1)"]
part3(["RULES", "ALLOW if a or b and c", "TRANSACTIONS"]) == []   # a/b/c aren't real fields — see edge cases
```

## Edge cases hidden tests are known to target
- default-ALLOW has **no** `(rule k)` suffix; a matched rule always does, even `(rule 1)`
- `(rule k)` numbers count *every* `RULES` line, including ones later reported as `ERROR` (Part 3) —
  a rule after a skipped one keeps its true line number, it does not shift down
- operator whitespace: `amount>=5000`, `amount >=5000`, `amount>= 5000`, `amount >= 5000` all parse
  identically (Part 2+)
- `==`/`!=` numeric-vs-string fallback: `amount == 0100` matches `amount == 100` (both parse as
  ints, compared numerically); `country == us` does **not** match `country == US` (strings, no
  case-folding — field names/values are case-sensitive, only the boolean keywords are not)
- `in [...]` with zero, one, and several items; spaces after commas optional; item not present →
  no match (not an error)
- `not` precedence: `not a and b` is `(not a) and b`; `a or b and c` is `a or (b and c)` (`and`
  tighter than `or`); nested parens `(a and (b or not c))`
- first matching rule wins even when the input transaction *could* also match a later rule — later
  rules are never evaluated once one has already matched
- a rule referencing a field name as a *value* is fine as long as it's on the other side of a
  comparison with a real field (`country == country` always true, both sides resolve to the same
  transaction field) — not exercised as a "gotcha", just confirms field vs. literal resolution is
  per-operand, not per-rule
- malformed rule text in Part 3 that still tokenizes cleanly but has bad structure: unbalanced
  parens, a comparison with no right-hand operand, `and`/`or` with a missing operand, a bare
  keyword (`and`/`or`/`not`/`in`) used where a field/value was expected — each produces exactly one
  `ERROR line k:` line, not a crash
- empty `RULES` block (every transaction defaults to `ALLOW`); empty `TRANSACTIONS` block (no
  output lines, `RULES`-only `ERROR` lines if any); a transaction row with fewer than 6 columns
  (missing trailing fields treated as `""`, comparisons against them just don't match rather than
  crashing)
- up to 10^5 rules × 10^5 transactions must not be quadratic per transaction (compile every rule's
  AST once, reuse across all transactions)

## Variants seen in the wild
- The two sources describing this round agree on the shape ("keyword/string match, upgraded to
  AND/OR boolean logic, multiple progressive stages") but neither publishes a verbatim I/O sample
  or field list — this repo's `RULES`/`TRANSACTIONS` stdin protocol, the six-field transaction
  schema, and the exact grammar productions are a reconstruction built to be testable, modelled on
  this suite's own `problems/q12_platform_balance_radar_rules` (the production-grade sibling of
  this same "rule string → AST → evaluate" skill, which also documents the real Radar grammar at
  https://docs.stripe.com/radar/rules/reference).
- This repo drills the exercise both ways: `loop/mock.py start cd07` gives you the full 60-minute
  hand-written budget (no AI panel available in this harness); the "用 AI 做这题的流程" section
  below is what changes if you *are* allowed a coding assistant, per the sources' grading notes.

## 用 AI 做这题的流程
This round is graded on **how you drive the assistant**, not on typing speed — both sources name
"whether you can use AI effectively without turning your brain off" (interviewdb) and "scores how
you use it on architecture, testing, and optimization" (interviewfox) as the explicit rubric.
Recommended flow (interviewdb's own summary): **AI summarizes the spec → you agree on an
implementation plan together → AI generates code → you write your own tests → you debug and
confirm you understand what got built**, not "paste the prompt, paste the output, submit."

**Five mistakes AI-generated solutions to this exact problem commonly make** — check for every one
before you accept the diff:
1. **Treats `in [US, CA]` as a substring test instead of set membership** — `value in
   raw_condition_text` or `field_value in "US,CA"` instead of splitting the bracket contents and
   comparing each item exactly. Symptom: `country == USA` wrongly satisfies `country in [US]`
   because `"US"` is a substring of `"USA"`.
2. **Gets `and`/`or` precedence backwards or flat** — implements them at the same precedence
   left-to-right (`a or b and c` → `(a or b) and c`, wrong) instead of `and` binding tighter, or
   builds the parser bottom-up so `or` ends up nested *inside* `and` instead of the reverse.
3. **Skips short-circuit evaluation** — evaluates both operands of `and`/`or` unconditionally. This
   is not disqualifying by itself (there's nothing here that fails on a well-formed transaction
   either way — every field exists) as long as the *result* is still correct, but watch for AI
   "fixing" the non-issue with a defensive `try/except` wrapped around every comparison, which
   quietly swallows a real bug (a genuinely missing field, a typo'd operator) instead of surfacing
   it as an `ERROR line k` the way Part 3 actually wants.
4. **Gets the default direction backwards** — defaults an unmatched transaction to `BLOCK` instead
   of `ALLOW`, or prints a placeholder like `(rule None)` / `(rule -1)` instead of omitting the
   suffix entirely. This is the single most common regression when a candidate later asks the AI to
   "add Part 3 support" and it silently rewrites Part 1/2's default-handling in the process.
5. **Either under- or over-builds the tokenizer** — under: `condition.split(" ")` on raw text, which
   breaks the moment spacing isn't exactly one space per token (`amount>=5000` with no spaces at
   all); over: in the same breath, generates a general-purpose expression engine with arithmetic
   operators, quoted-string constants, and a pluggable-function registry that nothing in this spec
   asked for, burning the 30-minute AI budget (or the 60-minute hand-written one) on scope the
   grader never requested. Both ends of this mistake come from not re-reading the grammar in the
   spec before accepting generated code.

## 面试官会怎么追问
1. "这是 AI 轮，评分标准是'你怎么指挥 AI'——如果面试官现在问你'你让 AI 生成的第一版代码有什么问题、
   你怎么发现的'，你会怎么回答?" — 逼你能具体说出一条真实的 review 发现（比如 `in [...]` 被 AI
   写成了子串匹配），而不是空泛地说"我 review 过了"。
2. "为什么 `not` 比 `and` 优先级高、`and` 又比 `or` 优先级高？这个优先级关系在你的递归下降解析器里
   体现在哪一行？" — 期望候选人直接指着 `_or` 调 `_and`、`_and` 调 `_not` 的调用链解释：**优先级
   越高的运算符，对应的解析函数离"叶子"越近**，而不是背一个优先级表却说不出代码里怎么实现的。
3. "如果要加一个新的运算符 `xor`，绑定优先级介于 `and` 和 `or` 之间，你会改哪几个函数？" — 检验
   候选人是否真的理解这个语法糖表结构是可扩展的：只需要在 `_or`/`_and` 之间插入一层新的 `_xor`
   方法，其余分支不用动。
4. "为什么 `ERROR line k` 只在 Part 3 出现，Part 1/2 遇到写错的规则就直接静默跳过？这是题面明确要求
   还是你自己的选择？如果面试官现在说'Part 2 也要报错'，你需要改哪里？" — 检验候选人能不能区分
   "题面写死的行为"和"没写清楚、自己做的合理选择"，并现场说出只需要把 `_evaluate` 里 `if part == 3`
   的判断放宽。
5. "10 万条规则、10 万笔交易，最坏情况下每笔交易都要扫到最后一条规则才 default ALLOW，复杂度是
   多少？有没有办法优化？" — 期望候选人先诚实指出这是 `O(rules × txns)` 最坏情况、当前实现无法避免
   （规则是任意布尔表达式，没有通用的索引结构能跳过不相关规则），再提一个受限场景下的优化思路，比如
   "如果大多数规则只判断单个字段的等值条件，可以按字段建索引、只对该字段值可能命中的规则做全量求值"。
6. "`country == country` 这种写法你选择让它按字段解析、恒真——为什么不是直接报错？换个角度，如果
   一个用户传进来的字段值本身就叫 `country`（比如商户名就是 `country`），你的语法怎么区分"这是字段"
   还是"这是值"？" — 检验候选人是否理解这套语法的核心设计取舍：**字段 vs. 字面量的判定是按 token
   的拼写、不是按值的语义**，这是省掉引号语法（不像 q12 需要 `:field:` 标记）所必须付出的代价。

## What this tests
skills: S02 tokenizing/parsing condition strings · S06 numeric-vs-string comparison fallback ·
S10 ordered rule evaluation with first-match-wins · S18 validation (Part 3's per-rule `ERROR`
reporting without crashing the batch) · S19 incremental grammar (Part n is a strict grammar subset
of Part n+1) · S24 Radar rule-engine vocabulary (shared with q12, at AI-assisted-round scope) ·
S25 directing/reviewing AI-generated code (spec comprehension, own test authorship, catching
over-engineering — this round's actual grading axis, per Sources)

## Sources
- https://www.interviewdb.io/guides/stripe-ai-programming-exercise (2026-06-09: "given a list of
  transactions and a list of rules, where each rule says whether to accept or block a transaction
  followed by an if condition"; grading: "whether you can use AI effectively without turning your
  brain off"; flow: "AI summarizes the README, you agree on an implementation plan, AI generates
  code, you write your own tests, you debug and confirm understanding")
- https://interviewfox.ai/interview-questions/stripe-oa-hackerrank-guide/ (2026: "scores how you
  use it on architecture, testing, and optimization"; ~30 min, HackerRank-embedded AI chat, "kind
  of like a lightweight Cursor")
- `loop/raw/en_forums.md` §9 "2026 新增：AI Programming Exercise 轮" and §6.2 C11 (this repo's own
  collation of the above two sources)
- `problems/q12_platform_balance_radar_rules/problem.md` (this repo's production-grade sibling
  problem; the RULES/comparison-op/boolean-grammar design here is deliberately built as a smaller,
  non-overlapping subset of that one's skill, not a copy of its `API:`/`BAL:`/`:field:` syntax)

## Clarifications (author's own, not sourced)
- Neither source specifies an input/output protocol, a transaction field list, or exact grammar —
  this repo's `RULES`/`TRANSACTIONS` stdin sections, six-field transaction schema, `(rule k)`
  output suffix, and Part 3's `ERROR line k:` reporting are reconstructions built for testability,
  chosen to parallel `problems/q12`'s own house style (parse → model → evaluate, first-match-wins,
  default-accept) rather than invent a fourth convention for the same underlying skill.
- "No suffix on default ALLOW" (vs. e.g. `(default)`) is this repo's choice, made explicit here
  because the source's one-line description does not specify the output format at all.
