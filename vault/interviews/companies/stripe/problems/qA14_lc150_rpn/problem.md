# qA14 · LC 150 Evaluate Reverse Polish Notation — truncate-toward-zero division, trace, and error handling

> ⚠️ **重建题（仅有标题）**：1p3a 镜像里这条条目（2025-12-21 收录）除了题名和一段公开的
> LeetCode 官方题目摘要外，**没有任何候选人面经正文**——没有面试轮次、追问、时间压力、
> 或 Stripe 专属改编的信息。下面 Part 2、Part 3 的 API 形状、输入输出的精确 stdin/stdout
> 框架，以及全部 edge case 清单，**都是本仓库编的**；只有 Part 1 的算法规则（+/-/*/、
> 除法向零截断、两个样例）是抄自 LeetCode 官方公开题面（见 Sources），不是这份镜像本身
> 带来的新信息。**不要把这里的输出格式当成真题格式去背**，练它是为了覆盖下面列出的
> S/A 编号。

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** phone screen / OA helper ·
**Last asked:** 1p3a 镜像收录日 2025-12-21（>6 个月分桶，不代表这就是最近一次被问到）
**Frequency:** 见 Sources 里的 tag 频率数据 · **Confidence:** high（LC 150 本身是公开题面，
算法规则确定）；low（"Stripe 是否真的问过这道题、怎么问的"——1p3a 这条镜像只有标题，
没有任何独立佐证）

## Sources
- LC 150 · *Evaluate Reverse Polish Notation* · Medium · https://leetcode.com/problems/evaluate-reverse-polish-notation/
- 1p3a 镜像（仅标题+官方摘要，无正文）：https://www.1point3acres.com/interview/problems/3a77854f-49c9-41b1-9678-b0a29df247d9
  ；本仓库镜像副本：`catalog/raw/mirror_1p3a_stripe/coding/`（`evaluate_reverse_polish_notation` 条目，2025-12-21）
- `skills_matrix.md` 的 Algorithm 表暂无 LC 150 专属条目（不像 qA10 对应 A12）——本题按
  最贴近的现有 S 编号计（S02/S09/S18/S21，见文末），不新增 A 编号。

## Context
Stripe's internal tooling parses more expression-like structures than you'd expect — fee
formulas, rule-engine conditions, a tiny DSL for computing a merchant's effective rate. RPN
(postfix) is the classic "stack does all the work" warm-up for that family of problems, and the
division-truncation rule is the single most common source of a wrong answer: Python's `//` floors
toward negative infinity, but this problem (like most language runtimes' native integer division)
truncates toward zero, so `-7 // 2` (`-4`) and `truncate(-7 / 2)` (`-3`) disagree exactly when one
operand is negative.

## Input (stdin)
```
PART n
<space-separated tokens>
```
The second line is the RPN expression: zero or more whitespace-separated tokens. A token is
either an **operand** (an optional single leading `-`, then one or more ASCII digits — no `+`
sign, no decimal point, no leading `-` on `"0"` beyond a literal `-0` which is just `0`) or an
**operator**, one of `+ - * /`. An absent second line means zero tokens.

## Output
* Part 1: one line, the integer result.
* Part 2: one line per operator processed, in the order it is processed, `<a> <op> <b> = <result>`
  (the two *original* operand values popped off the stack, not intermediate re-renders), followed
  by a final line `RESULT <value>`.
* Part 3: one line — either the integer result, or an error line `ERROR <code>` (see below);
  never raises, always exactly one output line.

## Rules

### Part 1 — `evaluate_rpn(tokens: list[str]) -> int`
Assume the input is a **valid** RPN expression per the LC constraints: `1 <= len(tokens) <= 10^4`,
every token is a valid operand or operator, the expression always fully reduces to exactly one
value, and division is never by zero. Process tokens left to right with a stack: on an operand,
push its integer value; on an operator, pop `b` (top of stack) then `a` (now top of stack, i.e.
the operand that appeared *before* `b` in the input) and push `a <op> b`. `+ - *` are ordinary
integer arithmetic (unbounded precision, Python `int`). **`/` truncates toward zero**, not `//`'s
floor-toward-negative-infinity: `truncate(a / b) = sign(a/b) * (abs(a) // abs(b))`. At the end the
stack holds exactly one value — that is the answer.

### Part 2 — `evaluate_rpn_trace(tokens: list[str]) -> list[str]`
Same evaluation as Part 1, assume-valid input, but instead of returning only the final number,
return one string per operator application, in the order applied:
```
<a> <op> <b> = <result>
```
using the exact original `a`/`b` integer values (not re-derived from anything downstream) and the
already-truncated `result`. After all tokens are processed, append one final line
`RESULT <value>` with the overall answer — present even when there were zero operators (a
single-operand expression like `["5"]` produces exactly one line, `RESULT 5`, with no operator
lines before it).

### Part 3 — `evaluate_rpn_safe(tokens: list[str]) -> str`
Same arithmetic, but the input is **not** assumed valid, and nothing may raise — every failure
returns a specific `"ERROR <code>"` string instead of the numeric result. Process tokens left to
right; the first applicable failure (in this priority order, checked at the token that triggers
it) wins:
1. `ERROR empty_input` — the token list is empty (before processing anything).
2. `ERROR unknown_token` — a token that is neither a valid operand (per the format above) nor one
   of `+ - * /`.
3. `ERROR insufficient_operands` — an operator is reached with fewer than two values on the
   stack.
4. `ERROR division_by_zero` — the operator is `/` and the popped `b` (the divisor, i.e. the value
   that was on top of the stack) is `0`.
5. `ERROR trailing_operands` — after all tokens are consumed with no earlier error, the stack does
   not hold exactly one value (e.g. `["1", "2"]`: two operands, zero operators, nothing left to
   combine them).

If none of the above fire, return `str(result)` for the single remaining stack value (same
truncation rule as Part 1/2).

## Worked examples
The first two are LeetCode's own published examples for this problem (values unchanged).
```
Part 1
["2", "1", "+", "3", "*"] -> 9      ((2 + 1) * 3)
["4", "13", "5", "/", "+"] -> 6     (4 + truncate(13 / 5) = 4 + 2)
["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"] -> 22   (LC's third example)
```
```
Part 2 (this repo's own trace framing of the first LC example)
stdin:
    PART 2
    2 1 + 3 *
stdout:
    2 + 1 = 3
    3 * 3 = 9
    RESULT 9
```
```
Part 2, zero operators (this repo's own edge case)
stdin:
    PART 2
    5
stdout:
    RESULT 5
```
```
Part 3 (this repo's own error-handling cases)
["1", "0", "/"]      -> "ERROR division_by_zero"
["+"]                -> "ERROR insufficient_operands"
["1", "2"]           -> "ERROR trailing_operands"
["1", "^", "2"]      -> "ERROR unknown_token"
[]                   -> "ERROR empty_input"
["3", "4", "+"]      -> "7"   (still returns the plain numeric string on success)
```

## Edge cases hidden tests are known to target
- **Division truncates toward zero, not floors**: `["-7", "2", "/"]` -> `-3` (not `-4`, which is
  what `//` would give); `["7", "-2", "/"]` -> `-3`; `["-7", "-2", "/"]` -> `3`; a positive result
  with an exact multiple (`["6", "3", "/"]` -> `2`) does not distinguish truncation from flooring,
  so hidden tests specifically need a case where the two rules disagree.
- Multi-digit and negative-literal operands parsed as one token (`"-13"`, not the operator `-`
  followed by `"13"`) — tokens are whitespace-delimited, so `-13` is unambiguous, but the operand
  regex must not also accidentally accept the bare `-` token as a number.
- A single-token expression (`["5"]`, or `["-3"]`) with zero operators — valid in Part 1/2
  (answer is just that operand); in Part 2 it is the "RESULT-only, no operator lines" case above.
- Part 3 priority order: `["/", "0"]` fails as `insufficient_operands` at the very first token
  (the stack is empty when `/` is reached) — it never gets far enough to notice the leftover `"0"`
  would also be a `trailing_operands` problem, because the scan stops at the first error;
  `["1", "0", "/", "9", "9"]` fails as `division_by_zero` at the third token, before the later
  `"9", "9"` pair would ever be reached and flagged as a `trailing_operands` issue — whichever
  failure is encountered *first while scanning left to right* is the one reported, not whichever
  failure a full static analysis of the token list would consider "worst."
- `ERROR insufficient_operands` vs `ERROR trailing_operands`: the former is "an operator wants two
  values and the stack doesn't have them" (checked *during* the scan); the latter is "the scan
  finished cleanly but more than one value is left over" (checked *after* the scan) — an operator
  never triggers `trailing_operands`, and having extra plain numbers never triggers
  `insufficient_operands`.
- Large inputs: `1 <= len(tokens) <= 10^4` per the LC constraint; Part 1/2 must stay `O(n)` (a
  single stack pass, not re-scanning).

## Variants seen in the wild
- LC 150 itself (canonical; the two mirror examples above are its own published examples).
- Full Levenshtein-adjacent "evaluate an infix expression with parens and precedence" (LC 224 /
  227) is the natural next step up but is a different, harder problem — not attempted here.
- "Explain the computation" trace output (Part 2) and "never crash on bad input, return a
  diagnostic code" (Part 3) are standard interview follow-ups for a stack-evaluator warm-up,
  independent of any specific Stripe sighting.

## What this tests
skills: **S02** token-level parsing with an explicit distinguishing regex for "operand" vs.
"operator" tokens (a bare `-` is an operator, `-13` is a negative operand) · **S09** exact,
byte-level output formatting (`RESULT <v>`, `ERROR <code>`, the `<a> <op> <b> = <result>` trace
line) · **S18** validation and error paths that return a diagnostic code instead of raising, with
an explicit, testable priority order across five distinct failure reasons · **S21** stdlib/stack
fluency and getting integer truncation-toward-zero right without reaching for `//` or float
division on values that could lose precision.
