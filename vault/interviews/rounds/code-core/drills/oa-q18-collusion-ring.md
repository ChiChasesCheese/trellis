---
nodes: [toolbox.union-find, transfer.stripe-oa]
tags: [stripe-oa, q18]
---
# Drill: find fraud rings from shared identifiers

Sixty minutes, three parts (a fourth, weighted-link phone-screen variant exists but is
out of scope here). Each record is `customer:device_id[:credit_card_id]` — any number of
identifier fields, compared only at matching positions, so a device value never links to
a card value and an empty field links nothing. Two customers are directly linked if they
share an identifier value at the same position; links are transitive. Part 1 lists every
customer directly linked to a target. Part 2 computes the size of the target's full
connected component (including the target itself) and decides `BLOCK` when that size
meets or exceeds a given threshold. Part 3 adds a `risk_factor` to each record; a
customer's risk is its most recent record's value, and a ring's risk is the mean of its
members' risk after dropping members with risk exactly 0, reported per ring in the order
each ring's first member appeared.

**Constraints to state and honor**
- Up to 10^5 records; identifiers at different field positions never link customers even
  if the string values happen to match.
- The target is excluded from its own direct-links list, and a pair linked through two
  different shared identifiers is listed only once.
- Ring size counts the target itself; a customer with no shared identifiers has ring size
  1, and an unknown target has ring size 0 and an empty direct-links list.
- A ring whose members all have risk 0 scores 0, not a division by zero.

**Grading points**
- The graph is bipartite — customers on one side, `(position, value)` identifier keys on
  the other — and every customer sharing one key is unioned in O(k), not connected
  pairwise in O(k^2); this is the single design decision the whole problem turns on.
- Encoding the field position into the union-find key is what keeps a device and a card
  from merging just because their string values coincide.
- Part 1 (one hop) and Parts 2/3 (full connected component) reuse the identical grouping
  structure — a candidate should say Part 1 is a one-hop query on the same bipartite
  graph, not a different algorithm.
- The block threshold `K` is non-strict (`size >= K`), and a long chain of five or more
  customers is still one ring, not a set of overlapping pairs.
- Risk-zero members are removed *before* averaging, not after, and the per-customer risk
  used is specifically the last chronological record for that customer.
- Deterministic output throughout: direct links sorted, ring members sorted within a
  line, rings ordered by first appearance, risk printed to two decimals.

**Source**
- `vault/interviews/companies/stripe/problems/q18_collusion_ring/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q18_collusion_ring.md`
- `vault/interviews/companies/stripe/problems/q18_collusion_ring/problem.md`, `vault/interviews/companies/stripe/problems/q18_collusion_ring/REPORT.md`
- `vault/interviews/companies/stripe/study/10-solutions/q18_collusion_ring.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
