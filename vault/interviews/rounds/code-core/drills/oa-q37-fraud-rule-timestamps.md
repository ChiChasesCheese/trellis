---
nodes: [chrono.intervals, model.event-stream, transfer.stripe-oa]
tags: [stripe-oa, q37]
---
# Drill: replay authorizations against a history of fraud rules

Sixty minutes, stdin to stdout, one accumulating program — `RULE` and `AUTH`
lines interleave freely, with no `PART` header separating the parts. Each
`RULE` line adds a version of a named fraud rule with an effective-from time
and a condition on merchant or amount; each `AUTH` line is an authorization
request with a timestamp, merchant and amount. For every `AUTH`, decide
APPROVE or REJECT using whichever rule version was actually in force at that
timestamp, then print every decision sorted by `(timestamp, id)`. Part 1 is a
single rule with only an effective-from time. Part 2 adds several
independently-named rules and multiple versions per name, where only the
version in force decides. Part 3 adds an effective-to time so a version can
also expire. Part 4 removes the assumption that `RULE` and `AUTH` lines
arrive in file order.

**Constraints to state and honor**
- `RULE` lines carry 4 fields (Parts 1–2) or 5 (Part 3, adding
  `effective_to`); `AUTH` lines are id, timestamp, merchant, amount.
- A condition is `<field><op><value>` on merchant or amount, or the literal
  `none` (rule switched off from that version on).
- Same-name `RULE` lines are versions of one rule, not independent rules;
  different names are independent, and any in-force match rejects.
- Output is sorted by `(timestamp, id)` with `id` compared as a plain string,
  not numerically.
- File order of `RULE` vs `AUTH` lines is irrelevant — version selection is
  always by effective time, never by line position.

**Grading points**
- Parse everything first, then sort rule versions per name by
  `effective_from` and requests by `(timestamp, id)` — nothing should depend
  on the order lines appear in the file.
- Version selection is "largest `effective_from ≤ t`", found the same way as
  q36's TTL lookup — say the two problems share a shape.
- `effective_to` is exclusive, and expiry of the in-force version does not
  revive an older one — no fallback, consistent with q36's Part 3 rule.
- `amount` comparisons are numeric, not string; `!=`/`<=` and the `none`
  condition are real branches to test, not corner cases to skip.
- The non-retroactivity rule — a request before `effective_from` is APPROVE
  even if it matches — is the line most likely to get inverted under time
  pressure; check it first against the worked examples.

**Source**
- `vault/stripe/q37_fraud_rule_timestamps/question.md`, `vault/stripe/q37_fraud_rule_timestamps/solution.md`, `vault/Quick_Check/problems/q37_fraud_rule_timestamps/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
