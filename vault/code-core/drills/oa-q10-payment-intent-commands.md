---
nodes: [model.state-machine, model.idempotency, transfer.stripe-oa]
tags: [stripe-oa, q10]
---
# Drill: replay PaymentIntent commands through a lifecycle state machine

Sixty minutes, stdin to stdout. A log of PaymentIntent API commands arrives one per line —
INIT, CREATE, ATTEMPT, SUCCEED, then UPDATE, then FAIL and REFUND, then everything timestamped
with a refund window — and you replay it against an in-memory ledger of merchants and payments.
Every command that doesn't apply (unknown id, wrong state, bad arity, a non-integer token) is
silently ignored, never printed and never crashed on. Part 1 create/attempt/succeed only. Part 2
adds UPDATE, which only takes while a payment is still awaiting action. Part 3 adds FAIL,
reopening a payment for another attempt, and REFUND, reversing a completed payment exactly once.
Part 4 prefixes every line with a timestamp, lets INIT carry an optional refund_limit window,
and — in the version tested here — has CREATE complete and credit immediately, no SUCCEED
required.

**Constraints to state and honor**
- Optional `PART n` first line (default 3); up to 2·10^5 lines; amounts are integer cents.
- Output one line per merchant that was ever `INIT`ed: `merchant balance`, sorted by plain
  string order, zero balances included.
- Payment states `REQUIRES_ACTION → PROCESSING → COMPLETED`; balance moves only on `SUCCEED`
  (or immediately on `CREATE` in Part 4).
- A refund debits exactly the amount that was credited, once; Part 4's window test is
  `t_refund − t_create ≤ refund_limit`, inclusive.

**Grading points**
- A transition table `{(command, state): new_state}` rather than nested if/elif — a combination
  not in the table is a no-op, which is the whole spec in one data structure.
- Arity/type checking happens once, before dispatch, so unknown words and bad ints never reach
  the state logic.
- Idempotency built in explicitly: second `INIT` doesn't reset, second `REFUND` is ignored,
  duplicate `CREATE` ids are rejected.
- `UPDATE` is blocked once `ATTEMPT`ed but reopens after `FAIL` — and `SUCCEED` credits whatever
  amount is current at that moment, not the original.
- The refund window boundary is inclusive; `refund_limit 0` means never, absent means always,
  and a refused refund can be retried later.
- Balances may go negative, and string-sorted merchant ids (`m10` before `m2`) is part of the
  output contract, not incidental.

**Source**
- `vault/Quick_Check/problems/q10_payment_intent_commands/problem.md`, `vault/Quick_Check/problems/q10_payment_intent_commands/REPORT.md`, `vault/stripe/q10_payment_intent_commands/question.md`, `vault/stripe/q10_payment_intent_commands/solution.md`, `vault/Quick_Check/study/10-solutions/q10_payment_intent_commands.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
