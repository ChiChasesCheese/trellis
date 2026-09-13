---
nodes: [algorithms.settlement, model.idempotency, transfer.stripe-oa]
tags: [stripe-oa, q25]
---
# Drill: match payments to invoices under relaxing rules

Sixty minutes, stdin to stdout, one growing program selected by `PART n`. Given a list of open
invoices (id, due date, amount) and a list of incoming payments (id, amount, free-text memo),
decide which invoices each payment settles. Part 1: a payment settles an invoice only on an
exact memo (`Paying off: <id>`, nothing else) and an exact amount match. Part 2: the memo is
tokenized freely — invoices it names become the *only* candidates with no fallback, or every
invoice if it names none — and the payment still needs an exact amount, applied to the
earliest-due qualifying candidate. Part 3: drop the exact-amount requirement and let one payment
pour across several candidates oldest-due first, reporting `PARTIAL` and `UNAPPLIED` remainders.
Part 4: prepend an audit trail listing every individual application in the order it happened.

**Constraints to state and honor**
- a payment line is split on its first two commas only; everything after is the memo, which may
  itself contain commas
- Part 2's token matching is whole-token: `invoiceAB` in a memo does not mention `invoiceA`
- a payment that names invoices never falls back to unmentioned ones, even when none of the
  named ones qualify
- a second payment aimed at an already-settled invoice changes nothing
- output is always in invoice input order, never due order; due-date ties break by invoice input
  order
- up to 10^5 invoices and 10^5 payments, amounts as integer cents

**Grading points**
- one matching engine reused across parts, where "amount must match exactly" and "pour until
  exhausted" are two settings on the same "pick candidates, then walk them due-first" shape, not
  two separate implementations
- candidate selection (mentioned vs. all) computed once per payment and never silently widened
  afterward if the first choice doesn't pan out
- the boundary triplet tested explicitly: payment exactly equal to the remainder → `PAID`, one
  cent short → `PARTIAL`, one cent over → `UNAPPLIED 1`
- idempotency treated as a first-class rule, not an incidental side effect — replaying a payment
  against a settled invoice must be a true no-op
- zero or negative payment amounts rejected silently, producing no `UNAPPLIED` line
- Part 4's audit trail ordered by when each application happened, which is a different order from
  the final status lines' invoice-input order

**Source**
- `vault/Quick_Check/problems/q25_invoice_reconciliation/problem.md`, `vault/Quick_Check/problems/q25_invoice_reconciliation/REPORT.md`, `vault/stripe/q25_invoice_reconciliation/question.md`, `vault/stripe/q25_invoice_reconciliation/solution.md`, `vault/Quick_Check/study/10-solutions/q25_invoice_reconciliation.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
