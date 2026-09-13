# q12 · Platform Balance API strings + Radar rule engine

**Type:** bespoke OA (+ VO follow-up) · **Stage:** HackerRank OA 2024 (75 min: 1 coding + 1 essay "how would you improve your code"); Part 3 grammar is the 2026 VO version · **Last asked:** OA 2024 (1point3acres threads); VO 2026-08-05 (csoahelp)
**Frequency:** 6 independent sources (1point3acres thread-1102706, software-engineer-446019, 442716, 1099687; 1024bbs 10992/5821; csoahelp 2026-08-05; github kylelong/stripe-interview + sahaia1 Python port for the ALLOW/BLOCK charge variant) · **Confidence:** medium (OA summaries only give the line shapes; the VO grammar is verbatim)

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

## Edge cases hidden tests are known to target
- keys in any order; duplicate keys (last wins); unknown keys ignored; negative and zero amounts;
  `BAL:` of an unknown merchant → `0`; malformed lines skipped without crashing
- rule operator with/without spaces (`amount==100` vs `amount == 100` vs `amount ==100`)
- `!=` never matches a missing field; a rule registered *after* an API line does not apply retroactively
- Part 3: constants with spaces; swapped operands; `AND` tighter than `OR` (`a OR b AND c` = `a OR (b AND c)`);
  nested parentheses; first matching rule wins even if a later rule disagrees; no match → accept;
  empty rules list → accept; missing boolean field → false; `"true"` vs `"True"` vs `"1"` (only
  case-insensitive `true` is truthy)
- exact output: bare integers for balances, `ACCEPT`/`BLOCK` upper-case

## Variants seen in the wild
- **Charge-evaluation variant** (github kylelong/stripe-interview `RadarRules.java`, sahaia1 Python port):
  `["CHARGE: card_country=US&currency=USD&amount=150&ip_country=CA", "ALLOW:amount<100",
  "BLOCK:card_country != ip_country AND amount > 100"]` → `0` (blocked) / `1` (allowed); operators
  `> < >= <= == !=`, ≤ 2 conditions joined by `AND`/`OR`, field-vs-field comparisons. The Part 2 evaluator
  already supports the numeric operators; Part 3 covers the boolean structure.
- OA 2024 second question: essay "how would you improve the code of question 1" — the parse → model →
  evaluate split here is the answer.

## What this tests
skills: S02 query-string parsing with malformed input · S03 dict-keyed state · S06 integer cents ·
S10 ordered command stream · S18 validation / missing keys · S19 incremental design (tokenizer +
recursive-descent parser added without touching the ledger) · S24 Radar / Connect vocabulary

## Sources
- 1point3acres thread-1102706「Stripe OA 面经」; interview/software-engineer-446019「Stripe OA 挂经 + 求debug」(tests 5 and 12 commonly fail); 442716; 1099687 (Platform Balance `API:`/`BAL:` lines + Radar `==`/`!=` rule, 75 min + essay)
- 1024bbs 10992「Stripe 吐血面经总结」/ 5821「近期Stripe面经总结」(summaries)
- csoahelp.com 2026-08-05 (VO: `should_accept_transaction(transaction, rules)`, `ACCEPT if (:field: = "const")`, boolean fields + AND/OR, first match wins, default accept, missing field → false)
- https://github.com/kylelong/stripe-interview/blob/master/RadarRules.java (ALLOW/BLOCK charge variant, verbatim task)
- https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/radarrules.py (Python port + expanded statement)
- https://docs.stripe.com/radar/rules/reference (real Radar grammar: first match wins, missing attribute ⇒ false)
