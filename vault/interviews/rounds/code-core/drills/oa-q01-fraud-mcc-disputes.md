---
nodes: [model.reversal, rules.exact-ratio, rules.thresholds, transfer.stripe-oa]
tags: [stripe-oa, q01]
---
# Drill: flag fraudulent merchants across a CHARGE/DISPUTE stream

Sixty minutes, five parts unlocked one after another, stdin to stdout. Stripe Radar
watches every merchant account, each carrying an MCC with its own fraud tolerance — a
fixed count of fraudulent charges, or a ratio of fraud once the merchant has enough
volume. Setup lines assign merchants to MCCs, set each MCC's threshold, declare which
result codes mean fraud, and set a minimum-volume gate; they apply before any event no
matter where they sit in the file. Then a stream of CHARGE and DISPUTE events arrives; a
DISPUTE reverses an earlier charge completely, unwinding both of its counters. Part 1
prints the parsed per-merchant threshold. Part 2 prints each account's fraud/total
counts after all charges, disputes ignored. Part 3 adds threshold evaluation, flagging
by count (`>=`) or by ratio (`>=`, gated by the minimum-volume line). Part 4 turns
disputes on as true reversals. Part 5 is the edge-case gauntlet: double disputes,
disputes of unknown ids, disputes of non-fraud charges, and merchants disputed down to
zero.

**Constraints to state and honor**
- A threshold literal with a decimal point (even `1.0`) is a ratio; one without is a
  count — the distinction is lexical, not numeric.
- Up to 10^5 events and 10^4 merchants; only the touched account is re-evaluated after
  each event, never a full rescan.
- Ratio comparisons are integer cross-multiplication, never floats.
- Output is the flagged account ids in plain string order joined by commas, or the
  literal `NONE`.

**Grading points**
- One ledger keyed by charge id, holding the account and the fraud bit, survives all the
  way to Part 4 — a design that only keeps running counters has to be rebuilt the moment
  disputes show up, and a strong candidate says so before writing Part 2.
- `apply_dispute` is the literal mirror of `apply_charge`, same fields opposite sign,
  which is what makes the reversal obviously correct rather than merely tested into
  correctness.
- Exact boundaries: a count threshold hit at exactly the value, a ratio hit at exactly
  the fraction, a total exactly at the minimum-volume gate.
- Disputing a non-fraud charge only lowers the total, which can push a ratio account
  *over* the line — candidates who model "dispute subtracts from both counters
  unconditionally" get this backwards.
- Double dispute of the same id and dispute of an unknown id are both no-ops; a merchant
  disputed down to zero total is never flagged, not a division by zero.
- Accounts with no MERCHANT line, or whose MCC has no threshold, are counted in Part 2
  but never flagged.

**Source**
- `vault/stripe/q01_fraud_mcc_disputes/question.md`, `vault/stripe/q01_fraud_mcc_disputes/solution.md`
- `vault/Quick_Check/problems/q01_fraud_mcc_disputes/problem.md`, `vault/Quick_Check/problems/q01_fraud_mcc_disputes/REPORT.md`
- `vault/Quick_Check/study/10-solutions/q01_fraud_mcc_disputes.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
