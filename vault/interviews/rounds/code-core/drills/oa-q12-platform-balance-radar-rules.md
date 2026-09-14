---
nodes: [input.grammar, input.structured, transfer.stripe-oa]
tags: [stripe-oa, q12]
---
# Drill: a platform balance ledger behind a hand-written Radar rule language

Sixty minutes, stdin to stdout. Part 1 is a per-merchant balance fed by `API:` lines whose body
is a URL query string (`amount=1000&merchant=121212`), plus `BAL:` to print a balance. Part 2
puts a minimal `field OP value` block-rule filter in front of every `API:` line. Part 3 replaces
that with the real Radar rule grammar — `ACCEPT`/`BLOCK if` with quoted string constants, bare
boolean attributes, `AND` binding tighter than `OR`, and parentheses — evaluated against `TXN:`
lines that must print `ACCEPT` or `BLOCK`.

**Constraints to state and honor**
- First line `PART n`; lines are `API:`/`BAL:`/`RULE:`/`TXN:` with a colon-then-optional-spaces
  prefix; up to 10^5 lines; values are taken literally, no URL-decoding.
- Query-string parsing: keys in any order, a duplicate key means last value wins, unknown keys
  are ignored but still visible to rules; a line missing `amount` or `merchant`, or with a
  non-integer `amount`, is malformed and produces no output and no state change.
- A rule only applies to lines that come after its `RULE:` registration, never retroactively; a
  rule that fails to parse is ignored.
- Part 3: a missing field makes any comparison or boolean attribute `False` (even `!=`); the
  first matching rule wins in registration order; no match means accept.

**Grading points**
- The three-layer separation candidates should name out loud: parse the query string, hold
  ledger/rule state, evaluate — the OA's own follow-up question is "how would you improve this
  code," and that split is the answer.
- Part 2's operator regex tolerates spaces on either side (`amount==100` vs `amount == 100`);
  comparison is numeric when both sides parse as integers, else an exact string compare.
- Part 3 wants a tokenizer plus a small recursive-descent parser (`expr → and_expr → primary`)
  that encodes AND-before-OR by grammar shape, not a precedence table bolted onto a flat scan.
- Compiling each `RULE:` to an AST once at registration, not re-parsing it per transaction — a
  real perf cliff at 10^5 lines (measured roughly 15x slower without it).
- Boolean field truthiness is only case-insensitive `"true"`; `"1"` and `"True"` need care since
  one is truthy and the other isn't obviously the same rule.
- Balances can go negative; an unknown merchant's `BAL:` is `0`.

**Source**
- `vault/interviews/companies/stripe/problems/q12_platform_balance_radar_rules/problem.md`, `vault/interviews/companies/stripe/problems/q12_platform_balance_radar_rules/REPORT.md`, `vault/interviews/companies/stripe/problems/q12_platform_balance_radar_rules/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q12_platform_balance_radar_rules.md`, `vault/interviews/companies/stripe/study/10-solutions/q12_platform_balance_radar_rules.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
