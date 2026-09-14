---
nodes: [rules.money, rules.rounding, rules.tiers, transfer.stripe-oa]
tags: [stripe-oa, q03]
---
# Drill: monthly billing with metered usage, a fixed plan, and mid-month proration

Sixty minutes, stdin to stdout, no libraries beyond the standard one. Each line
of input is one chat session: a user id, input token count, output token
count, and a plan (`payg` or `fixed`). Compute each user's bill for the month
and print it, working in whole cents throughout — never floating point money.

- Part 1: pay-as-you-go pricing — bill each session's tokens in complete
  100-token blocks, input and output blocks priced differently, remainders
  never carried between sessions.
- Part 2: add the fixed plan — a flat monthly fee that includes a token
  allowance; billable tokens (after the same per-session block rounding)
  consume the allowance in a fixed order, and anything left over is billed at
  the pay-as-you-go block rates.
- Part 3: a user who has sessions on both plans in the month pays a prorated
  fixed fee and gets a prorated allowance, both scaled by the ratio of fixed
  sessions to total sessions (session counts, not token counts).

**Constraints to state and honor**
- Up to ~10^5 session lines; token counts can be large (up to 10^9) so all
  arithmetic must stay in integers.
- Per-session block rounding happens before the tokens are applied to any
  allowance — round first, then consume.
- Within one fixed session, input tokens draw down the allowance before
  output tokens do; sessions are consumed in input order.
- Output one line per user sorted by user id in plain string order, format
  `user_id: $x.xx`, and every user appears even at $0.00.

**Grading points**
- All money kept in integer cents from parse through render; a single
  formatting step converts cents to `$x.xx` at the very end.
- Half-up rounding of the prorated fee implemented as integer arithmetic
  (e.g. `(numerator*2 + denominator) // (2*denominator)`), not `round()`,
  which the candidate should know is banker's rounding and wrong here.
- The allowance-consumption order is exercised: input before output within a
  session, sessions in input order, and the overage split correctly when the
  allowance runs out in the middle of a session's tokens.
- Per-session, per-plan block rounding kept separate from cross-session or
  cross-plan pooling — remainders under 100 tokens never accumulate.
- Proration ratio computed from session counts, not token counts, and
  produces a floored allowance and a half-up-rounded fee independently.
- $0.00 users still printed; sort is plain string order, not natural/numeric
  order (e.g. `user10` sorts before `user2`).

**Source**
- `vault/stripe/q03_chat_billing/question.md`
- `vault/stripe/q03_chat_billing/solution.md`
- `vault/Quick_Check/problems/q03_chat_billing/problem.md`
- `vault/Quick_Check/problems/q03_chat_billing/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
