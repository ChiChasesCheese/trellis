# q12 · Platform Balance API strings + Radar rule engine

## Context
A Stripe Connect *platform* keeps a running balance per connected merchant. Money movements arrive as
API request strings whose body is a URL query string (`amount=1000&merchant=121212`, amounts in integer
cents). Stripe Radar sits in front of that API: a rule is `ACTION if CONDITION` and the first matching
rule decides whether the request is accepted. Part 1 is the ledger, Part 2 bolts a minimal `==`/`!=` rule
filter in front of it, Part 3 is the real Radar-style rule language with quoted constants, boolean
attributes, `AND`/`OR` and parentheses (https://docs.stripe.com/radar/rules/reference).

## Input (stdin)
First line `PART n`. Then one command per line; blank lines ignored; the prefix is followed by `:` and
optional spaces.
- `API: k1=v1&k2=v2…` — a balance update. Keys in any order. `amount` is an integer (may be negative),
  `merchant` is an opaque string. Unknown keys are ignored (but stay visible to rules). Duplicate key →
  **last value wins**. A line is **malformed** (ignored, no output) if `amount` or `merchant` is missing, or
  `amount` is not an integer, or the prefix is unknown.
- `BAL: merchant=121212` — print that merchant's current balance as a plain integer (`0` if never seen).
- `RULE: <rule>` (Parts 2–3) — register a rule; rules apply to every later `API:`/`TXN:` line in order of
  registration. A rule that fails to parse is ignored.
- `TXN: k1=v1&…` (Part 3) — evaluate a transaction against the rules; print `ACCEPT` or `BLOCK`.
Values are taken literally (no URL-decoding; spaces inside values are allowed). Up to 10^5 lines.

## Output
One line per `BAL:` (integer cents, e.g. `750`, `-250`, `0`) and per `TXN:` (`ACCEPT` / `BLOCK`), in input
order. `API:` and `RULE:` print nothing.

## Rules
### Part 1 — platform balance
`API:` adds `amount` to `balances[merchant]` (starting at 0; balances may go negative). `BAL:` prints it.

### Part 2 — simple block rules
`RULE: field OP value` with `OP ∈ {==, !=}` and **optional spaces on either side of the operator**
(`amount==100`, `amount ==100`, `merchant != 121212`). Every Part 2 rule is a **block** rule: an `API:` line
whose query matches **any** registered rule is rejected (balance untouched, nothing printed).
Comparison: if both sides parse as integers compare numerically (`amount==0100` matches `100`), otherwise
compare the trimmed strings. A field missing from the query never matches (`!=` included — Radar
semantics). Rules only affect `API:` lines that come after them. (Cheap extension, tested: `<`, `>`, `<=`,
`>=` also work, numerically only — the GitHub charge-evaluation variant uses them.)

### Part 3 — Radar rule language
```python
def should_accept_transaction(transaction: dict[str, str], rules: list[str]) -> bool
```
Grammar (keywords case-insensitive, field names and constants case-sensitive):
```
rule       := ("ACCEPT" | "BLOCK") "if" expr
expr       := and_expr ("OR" and_expr)*          # AND binds tighter than OR
and_expr   := primary ("AND" primary)*
primary    := "(" expr ")" | operand ("=" | "!=") operand | field
operand    := field | '"' constant '"'           # constants may contain spaces; operands swappable
field      := ":" name ":"                       # name = [A-Za-z0-9_]+
```
- A bare `field` is a **boolean attribute**: true iff `transaction[name].lower() == "true"`.
- `=` / `!=` compare the two operand strings exactly (`"US" = :card_country:` is the same as
  `:card_country: = "US"`; field-vs-field also allowed).
- **Missing field ⇒ that comparison / boolean is `False`** (even for `!=`), like Radar.
- Rules are evaluated **in order; the first rule whose condition is true decides** (`ACCEPT` → `True`,
  `BLOCK` → `False`). **No rule matches ⇒ accept** (`True`). Empty rule list ⇒ `True`.
- A syntactically invalid rule raises `ValueError` from `should_accept_transaction`; the stdin driver
  (`part3`) skips such `RULE:` lines.
In the stdin protocol `TXN:` prints `ACCEPT`/`BLOCK`; `API:`/`BAL:` still work as in Part 1 (unfiltered).

## Worked examples
```
PART 1
API: amount=1000&merchant=121212
API: merchant=121212&amount=-250
BAL: merchant=121212          -> 750
BAL: merchant=999             -> 0
API: amount=abc&merchant=1        (malformed, ignored)
API: amount=5&amount=7&merchant=1&foo=bar
BAL: merchant=1               -> 7
```
```
PART 2
RULE: amount==100
RULE: merchant != 121212
API: amount=100&merchant=121212   (blocked: amount==100)
API: amount=50&merchant=777       (blocked: merchant != 121212)
API: amount=50&merchant=121212    (accepted)
BAL: merchant=121212          -> 50
BAL: merchant=777             -> 0
```
```
PART 3
RULE: BLOCK if (:card_country: = "US" AND :large_amount:)
RULE: ACCEPT if ("United States" = :country_name:)
RULE: BLOCK if (:currency: != "usd")
TXN: card_country=US&large_amount=true&country_name=United States      -> BLOCK   (rule 1)
TXN: card_country=US&large_amount=false&country_name=United States&currency=eur -> ACCEPT (rule 2 before rule 3)
TXN: card_country=CA&currency=eur                                       -> BLOCK   (rule 3)
TXN: card_country=CA                                                    -> ACCEPT  (currency missing ⇒ rule 3 false; no match)
```
```python
should_accept_transaction({"a": "1"}, ['BLOCK if (:a: = "1" OR :b: = "2")'])           -> False
should_accept_transaction({"a": "1", "b": "x"}, ['BLOCK if (:a: = "1" AND :b: = "2")']) -> True
should_accept_transaction({}, [])                                                        -> True
```

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s24-payments-domain-vocab|S24 领域词汇（支付）]]
