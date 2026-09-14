---
nodes: [algorithms.settlement, transfer.stripe-oa]
tags: [stripe-oa, q35]
---
# Drill: spend loyalty points oldest-first across multiple payers

Sixty minutes, live coding, stdin to stdout, state accumulating across the whole
session. `ADD,payer,points,timestamp` records a signed point transaction for a payer
(timestamps can arrive out of order); `SPEND,points` deducts from the oldest positive
points across all payers first, regardless of who funded them; `BALANCE` reports every
payer ever added, in first-add order, including zero balances. A negative transaction is
a correction that, before any spend, cancels that specific payer's own oldest remaining
positive points — never the user's balance in general — and an `ADD` that would push its
payer negative is rejected outright.

**Constraints to state and honor**
- Points transactions must be sorted by timestamp for the FIFO walk, with same-timestamp
  ties broken by insertion order — input order is not timestamp order.
- Each transaction entry tracks its own remaining balance so consecutive `SPEND` calls
  continue from where the previous one stopped, rather than re-deriving state each time.
- A `SPEND` that exceeds the total available balance changes nothing and prints `ERROR`;
  `SPEND,0` prints an empty line rather than nothing at all.
- Payer names may contain spaces; parse accordingly.

**Grading points**
- Modeling each payer's contribution as a sequence of individually-trackable entries
  (not a single running balance) is what makes both FIFO spending and per-payer
  correction possible — a candidate who collapses to one balance per payer has to
  backtrack once negative transactions appear.
- The negative-transaction rule stated precisely: it nets against its *own* payer's
  oldest remaining positive entries first, independent of whether those entries were
  added before or after the correction in timestamp order — processing negatives before
  running the spend FIFO is what keeps every payer non-negative throughout.
- `SPEND` output is aggregated per payer (even when several of that payer's entries are
  touched by one spend) and ordered by first consumption, not by payer name.
- Exact-balance spend succeeds; one point more fails atomically, leaving state
  untouched — this is the boundary hidden tests are built around.
- Zero-balance payers still appear in `BALANCE`, in the order they were first added, not
  sorted alphabetically or by balance.
- Sorting entries by `(timestamp, insertion order)` explicitly, since adds are not
  guaranteed to arrive in timestamp order.

**Source**
- `vault/stripe/q35_user_points_fifo/question.md`, `vault/stripe/q35_user_points_fifo/solution.md`
- `vault/Quick_Check/problems/q35_user_points_fifo/problem.md`, `vault/Quick_Check/problems/q35_user_points_fifo/REPORT.md`
- `vault/Quick_Check/study/10-solutions/q35_user_points_fifo.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
