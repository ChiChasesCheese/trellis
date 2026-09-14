---
nodes: [algorithms.sliding-window, rules.grouping]
tags: [stripe-oa, qa04, leetcode]
---
# Drill: flag invalid transactions by amount and same-name city conflicts

Forty-five minutes, stdin to stdout. This is LeetCode 1169, Invalid
Transactions: each transaction is name, time, amount and city, and it's
invalid if its amount exceeds 1000 or if another transaction with the same
name but a different city happened within 60 minutes inclusive — in which
case both transactions are invalid. Part 1 returns every invalid transaction
in input order. Part 2 attaches the reasons a transaction was flagged,
naming the specific conflicting transactions. Part 3 turns the same rule
into a streaming detector that processes transactions in arrival order,
evicts old history, and reports each transaction as invalid at most once.

**Constraints to state and honor**
- Transactions are `name,time,amount,city`; up to a few thousand of them,
  given in arbitrary time order for Parts 1–2.
- Amount strictly greater than 1000 is invalid on its own; the city conflict
  needs `|t1 - t2| ≤ 60` and different cities for the same name.
- Output preserves input order and keeps exact duplicate transaction strings
  as separate reported lines.
- Part 3's arrivals are guaranteed non-decreasing in time (a decrease raises
  an error), and history older than the current window can be evicted.
- A dense group (many same-name transactions in one minute) must not
  degrade to a pairwise O(n²) scan.

**Grading points**
- Group by name, sort each group by `(time, input index)`, then slide a
  window counting cities in range rather than comparing every pair — state
  the complexity target before coding it.
- The city-conflict condition is symmetric: both transactions in a
  conflicting pair are invalid, including the earlier one, and the amount
  check is independent of it (OR, not AND).
- A transaction never conflicts with itself or an identical duplicate at the
  same city — same city means no conflict regardless of how many identical
  copies exist.
- Part 2's reason ordering matters: `amount>1000` first when applicable,
  then conflicting transactions ordered by the other transaction's
  `(time, index)`, not by discovery order.
- Part 3's streaming detector must report each transaction invalid at most
  once total even though a later arrival can retroactively implicate an
  earlier one — track what's already been reported, not just what's in the
  window.

**Source**
- `vault/interviews/companies/stripe/problems/qA04_lc1169_invalid_transactions/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/qA04_lc1169_invalid_transactions.md`, `vault/interviews/companies/stripe/problems/qA04_lc1169_invalid_transactions/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
