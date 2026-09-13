# q12 Platform Balance + Radar Rules — report

## Summary
Two Stripe primitives glued together: a Connect-style per-merchant balance fed by query-string API
lines, and a Radar rule filter in front of it. Part 1 is parsing hygiene (key order, duplicates,
malformed lines), Part 2 is a split-carefully `==`/`!=` rule, Part 3 is the real thing: a tokenizer +
recursive-descent parser for `ACCEPT/BLOCK if (...)` with quoted constants, boolean attributes, `AND`
tighter than `OR`, parentheses, first-match-wins and missing-field ⇒ false. The 2024 OA followed it
with an essay "how would you improve your code" — the parse → model → evaluate split is the answer.

## Sources & confidence
medium — OA line shapes from 1point3acres (4 threads) + 1024bbs summaries only; the Part 3 grammar is
verbatim from csoahelp 2026-08-05 (VO) and matches docs.stripe.com/radar/rules/reference; the
ALLOW/BLOCK charge variant is verbatim in github kylelong/stripe-interview (Stripe DMCA'd a clone).

## Approach by part
1. `parse_query` (split on `&`, `=` once, last duplicate wins) → `Ledger.apply` requires int `amount`
   and non-empty `merchant`, else the line is ignored. `BAL:` prints `balances.get(m, 0)`.
2. `RULE: field OP value` matched with one regex (`\s*` around the operator). Missing field never
   matches (even `!=`). Numeric compare when both sides are ints, else exact string compare. `<>=<=>=`
   supported for the GitHub variant. A blocked `API:` line leaves the balance untouched.
3. `tokenize` (regex: parens, `=`/`!=`, `:field:`, `"const"`, keywords) → `Parser` builds an AST
   (`or`/`and`/`cmp`/`bool`) → `evaluate(ast, txn)`; compiled rules are cached per rule string so
   10^5 transactions do not re-parse. `should_accept_transaction` returns on the first matching rule,
   `True` when none matches.

## Pitfalls hidden tests target
- `amount==100` vs `amount == 100` (naive `split(" ")` breaks) · `!=` on a missing field must be false
- duplicate keys (last wins), unknown keys, negative amounts, unknown merchant `0`, malformed lines
- rule registered after an API line must not apply retroactively
- Part 3: `a OR b AND c` precedence, swapped operands, constants with spaces, first rule wins even if a
  later rule contradicts, empty rule list → accept, `"TRUE"` truthy but `"1"` not, unbalanced parens
  → `ValueError`
- performance: re-tokenizing every rule per transaction is 15× slower than caching the AST (measured
  3.98 s → 0.28 s)

## Complexity & measured cost
O(lines × rules) evaluation, O(merchants + rules) memory. Measured: 0.28s, 33 MB (100k lines: 40k API,
10k BAL, 50k TXN against 21 rules; budget 2 s / 256 MB). Solution is ~270 lines because it carries three
independent pieces (ledger, simple rules, parser); a candidate would write only the part asked.

## Test inventory
24 tests — part1: 8 · part2: 6 · part3: 10; edge 15 · fmt 1 · io 2 · perf 1.

## Skills exercised
S02 query-string parsing · S03 dict-keyed state · S06 integer cents · S10 ordered commands ·
S18 validation of missing/invalid keys · S19 incremental design · S24 Radar/Connect vocabulary
