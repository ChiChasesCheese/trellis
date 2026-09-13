---
nodes: [output.ordering, input.malformed, transfer.stripe-oa]
tags: [stripe-oa, q31]
---
# Drill: mutual-rank pairings over ordered wishlists

Sixty minutes, stdin to stdout. Each user names an ordered wishlist of other users' apartments —
best choice first. Part 1 answers whether two users are each other's r-th choice for a given rank
(a first-choice check is just rank 0). Part 2 is the core of the drill: for a proposed bump that
would move one wishlist entry up one rank and its neighbor down, report which users' mutual-pair
status would flip, without ever performing the swap. Part 3 generalizes to mutual wishes at any
rank, scored by the sum of the two ranks, with queries for every mutual pair and for one user's
best mutual wish. Part 4 finds simple swap cycles of length 2 to 5, where each user in the chain
wants the next user's apartment.

**Constraints to state and honor**
- Wishlist lines are `user: w1 w2 w3 ...`, space-separated, best first; a user may declare an
  empty list, and a name that appears only inside someone else's wishlist behaves as an empty
  list of its own.
- Any rank query beyond a user's own or the partner's list length, or against an unknown user,
  answers `false` / `NONE` — it must never raise an index error.
- `BUMP u 0` (nothing above to swap with) and `BUMP u r` with `r` at or past the list length both
  answer `NONE`; the swap itself is never applied to the underlying data.
- `PAIRS` reports each mutual-wish pair once with the smaller name first; `CYCLES k` reports each
  cycle once, rotated to start at its smallest name, with no duplicate rotations.

**Grading points**
- A precomputed `pos[u][v] -> rank` reverse-lookup per user, so every mutual check is an O(1)
  lookup instead of a re-scan of the partner's list.
- `BUMP`'s affected-or-not test expressed as an XOR of before/after mutual status for each of the
  two moved entries, not as "swap, check, swap back" — say out loud why comparing states beats
  mutating and restoring.
- Output order for `BUMP` is the entry moving up, then the one displaced down — both may appear,
  either may be absent, and the answer is `NONE` only when neither is affected.
- `PAIRS` and `BEST` tie-break fully specified: `PAIRS` by (score, u, v); `BEST u` by (score, the
  querying user's own rank of v, then name) — ties are not left to whatever the sort happens to do.
- A user listing themselves inside their own wishlist is ignored for pairing purposes.
- Cycle detection at length k as a bounded DFS from each candidate start, canonicalized to avoid
  printing the same cycle under multiple rotations; `CYCLES 2` must equal `PAIRS` without scores.

**Source**
- `vault/Quick_Check/problems/q31_wishlist_mutual_rank/problem.md`, `vault/Quick_Check/problems/q31_wishlist_mutual_rank/REPORT.md`, `vault/stripe/q31_wishlist_mutual_rank/question.md`, `vault/stripe/q31_wishlist_mutual_rank/solution.md`, `vault/Quick_Check/study/10-solutions/q31_wishlist_mutual_rank.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
