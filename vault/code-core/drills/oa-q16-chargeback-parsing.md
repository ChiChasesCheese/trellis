---
nodes: [input.malformed, rules.money, transfer.stripe-oa]
tags: [stripe-oa, q16]
---
# Drill: parse card-network chargebacks, drop corrupted rows, cancel withdrawn disputes

Sixty minutes, stdin to stdout. Chargeback records arrive one per line — network, transaction
id, amount in minor units, currency, reason, date — the concatenation of one or more
card-network files. Part 1 parses and renders every row as a merchant-facing dispute line,
formatting money per currency (symbol-and-cents, zero-decimal for currencies like JPY, or bare
digits for anything else). Part 2 hardens the parser: a row that fails any of several checks is
corrupted, must be skipped and counted, and the run always ends with a `SKIPPED: n` line. Part 3
adds the sting in the tail: group the surviving rows by `(network, transaction_id)`, and if any
row in a group has reason `withdrawn`, no row from that group is printed at all — original and
withdrawal both vanish.

**Constraints to state and honor**
- First line `PART n`; comma-separated rows with fields trimmed; blank lines ignored and not
  counted; up to 2·10^5 lines.
- A row is corrupted when it doesn't have exactly six fields, `amount` isn't a non-negative
  integer, `date` doesn't parse as `%Y-%m-%d` (but a valid non-zero-padded date like `2024-2-3`
  is accepted and reprinted normalized), `network` isn't one of the four known networks
  (case-insensitive on input), or `transaction_id`/`currency`/`reason` is empty.
- Money formatting: two-decimal currencies print symbol + `x.xx`; zero-decimal currencies (`jpy`,
  `krw`) print the bare integer; any other currency prints `x.xx` with no symbol.
- Withdrawn cancellation is order-independent (withdrawal before or after the original, or a
  lone/double withdrawal, all drop the whole group) and scoped per network — the same
  `transaction_id` on a different network is unaffected; withdrawn rows are not counted toward
  `SKIPPED`, and a row that never made it past Part 2's validity check can't cancel anything.

**Grading points**
- One `parse_row` function returning `None` on any corruption reason, with the count of `None`s
  driving `SKIPPED: n` — validation and rendering never interleave.
- `amount` validated as a non-negative integer specifically (rejecting `"25.00"`, negative, and
  empty) and `date` validated by attempting `strptime` rather than hand-rolled regex, then
  reprinting the parsed date normalized.
- The withdrawn rule implemented as two passes over the valid rows — first collect the
  `(network, id)` pairs with reason `withdrawn`, then filter — rather than trying to detect
  withdrawal order at parse time.
- `SKIPPED: 0` must still print on an all-valid or empty run; Part 1 alone prints nothing extra.
- Output stays in input order throughout; a duplicate non-withdrawn dispute is printed once per
  occurrence, not deduplicated.
- A currency symbol table and the zero-decimal set are the two places all the money-formatting
  edge cases (`5 → $0.05`, `100 → $1.00`, unknown currency → no symbol) actually live.

**Source**
- `vault/Quick_Check/problems/q16_chargeback_parsing/problem.md`, `vault/Quick_Check/problems/q16_chargeback_parsing/REPORT.md`, `vault/stripe/q16_chargeback_parsing/question.md`, `vault/stripe/q16_chargeback_parsing/solution.md`, `vault/Quick_Check/study/10-solutions/q16_chargeback_parsing.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
