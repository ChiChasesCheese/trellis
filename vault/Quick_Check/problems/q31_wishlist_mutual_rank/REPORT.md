# q31 Wishlist / Mutual Rank — report

## Summary
Ordered wishlists in an apartment-swap network; find users who are each other's r-th choice, then
predict which pairings flip when one entry is bumped up a rank. It is a phone-screen favourite
because it is pure index bookkeeping (0-based ranks, out-of-range lookups, symmetric checks) with
a Part 2 that punishes candidates who mutate state or forget the displaced entry.

## Sources & confidence
high for Parts 1–2 (verbatim prompt + examples in joeytor `MutualRank.java`; adonais0 2021 phone
write-up; 1point3acres ×4 "mutualrank / wishlist" high-frequency phone lists; InterviewDB
"Wishlist — Phone"). Parts 3–4 (rank-sum scoring / best match, swap cycles) are reconstructed
from the title-only follow-ups and marked as such in problem.md. No conflicting rules between
sources; adonais0's `changed_antipairings` is the same function under another name.

## Approach by part
1. `pos[u][v]` rank index built once; `has_mutual_pair_for_rank(u, r)` = `entry(u, r) = v` and
   `entry(v, r) = u`; `has_mutual_first_choice` delegates with r = 0.
2. `changed_pairings(u, r)`: `up = list[u][r]`, `down = list[u][r-1]`; each is affected iff its
   mutual status *before* (checked at its current rank) differs from *after* (rank ∓ 1) — an XOR,
   computed without touching the lists. Output order: `up` then `down`.
3. Mutual wish at any ranks; score = sum of the two ranks; `PAIRS` sorted by (score, u, v) with
   u < v; `BEST u` minimises (score, own rank, name).
4. `CYCLES k`: DFS from each start over successors with name > start (canonical rotation, no
   duplicates), close the cycle when `start ∈ list[last]`.

## Pitfalls hidden tests target
- partner's list shorter than the queried rank (`RANK b 2`) → false, never IndexError
- `BUMP u 0` / rank ≥ len → nothing; both moved entries can be affected; state must not change
- unknown users (queried or listed but never defined) act as empty lists; self-entries ignored
- `PAIRS` each pair once (u < v) and ties broken by names; cycles printed once, sorted

## Complexity & measured cost
Parts 1–2 O(1) per query after O(total list length) preprocessing; Part 3 O(L); Part 4 O(L·d^(k-2)).
Measured: 0.23s, 71 MB (10k users × 10 entries, 100k queries + PAIRS + CYCLES 3).

## Test inventory
20 tests — part1: 6 · part2: 5 · part3: 4 · part4: 5 (incl. 1 io, 1 perf); edge 9 · fmt 1.

## Skills exercised
S02 parsing · S03 records keyed by id · S08 deterministic ordering · S13 index/off-by-one
discipline · S18 validation · S19 incremental design · S20 self-testing
