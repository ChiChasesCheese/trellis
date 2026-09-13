# q31 · Wishlist / Mutual Rank — apartment-swap pairings

**Type:** phone screen (2021–2023) · **Stage:** phone interview (joeytor README; adonais0 2021 phone;
1point3acres "mutualrank / wishlist" high-frequency phone list) · **Last asked:** 2023-11 (1point3acres
thread-1028744) · **Frequency:** 7 independent sources (joeytor Java header, adonais0 blog, 1point3acres
×4 threads, InterviewDB "Wishlist — Phone") · **Confidence:** high (Parts 1–2 verbatim), Parts 3–4 reconstructed

## Context
Imagine an Airbnb-like vacation rental service where users in different cities exchange apartments
for a week. Each user compiles an **ordered wishlist** of other users' apartments — the first entry is
their first choice. You are writing the part of the matching algorithm that finds users who would
like to swap with each other: two users are a *mutually ranked pair at rank r* when each is the
other's (r+1)-th choice.

## Input (stdin)
First line `PART n`. Then, in any order:
- wishlist lines `user: w1 w2 w3 ...` (a colon after the user name; entries space-separated, best
  first; a user may have an empty list `user:`); every line containing `:` is a wishlist;
- query lines (no colon), answered in input order (commands per part below).
Names are case-sensitive tokens without spaces. Blank lines are ignored. Up to 10^4 users, total
wishlist length up to 10^5, up to 10^5 queries.

## Output
One line per query, in query order. Booleans print as `true` / `false`. Lists print the names
separated by single spaces, or `NONE` when empty.

## Rules
### Part 1 — mutual first choice and mutual pair for rank (verbatim)
`FIRST u` → `has_mutual_first_choice(u)`: `true` iff `u`'s first choice `v` exists and `v`'s first choice
is `u`. `RANK u r` → `has_mutual_pair_for_rank(u, r)`: `true` iff `u`'s entry at 0-based rank `r` is
some `v` **and** `v`'s entry at the same rank `r` is `u`. `FIRST u` ≡ `RANK u 0`. Unknown user, rank
≥ list length, or negative rank → `false`.

### Part 2 — changed pairings when an entry is bumped up (verbatim)
The most common operation is **incrementing the rank of one wishlist entry**: entry at rank `r` of
user `u` swaps with the entry at rank `r−1`. `BUMP u r` → `changed_pairings(u, r)`: the users whose
pairing with `u` **would gain or lose** mutually-ranked status if the swap took place (the swap is
*not* applied). Let `y = list[u][r]` (moves up to `r−1`) and `z = list[u][r−1]` (moves down to `r`):
`y` is affected iff (`list[y][r] == u`) ≠ (`list[y][r−1] == u`); `z` is affected iff
(`list[z][r−1] == u`) ≠ (`list[z][r] == u`). Output `y` then `z` (only those affected); `NONE` if none.
`r = 0`, `r` ≥ list length or unknown user → `NONE` (nothing to swap).

### Part 3 — mutual wishes at any rank, scored by rank sum (reconstructed)
`u` and `v` are a *mutual wish* when `v ∈ list[u]` and `u ∈ list[v]` (ranks may differ). Its
**score** is `rank_u(v) + rank_v(u)` (lower is better; 0 = mutual first choices).
`PAIRS` → every mutual-wish pair, one per line `u v score`, with `u < v` (string order), sorted by
score, then `u`, then `v`; `NONE` if there are none.
`BEST u` → `v score` for `u`'s lowest-scoring mutual wish; ties → the smaller `rank_u(v)`, then the
smaller name; `NONE` if `u` has no mutual wish.

### Part 4 — swap cycles (reconstructed)
`CYCLES k` → all simple cycles `u1 → u2 → … → uk → u1` of length `k` (2 ≤ k ≤ 5) where each user
wants the next user's apartment (`u_{i+1} ∈ list[u_i]`, `u1 ∈ list[uk]`). Each cycle is printed once,
rotated so that it starts at its smallest name, as `u1 u2 … uk`; lines sorted in string order; `NONE`
if none. `k = 2` is exactly the set of mutual-wish pairs.

## Worked examples
Data (verbatim from the source) used by all examples:
```
a: c d
b: d a c
c: a b
d: c a b
```
```
PART 1                          Output
FIRST a                         true      (a and c are each other's first choice)
FIRST b                         false     (b's first choice d does not rank b first)
RANK a 0                        true
RANK a 1                        true      (a and d are mutually each other's second choice)
RANK b 2                        false     (b's third choice is c; c has no third choice)

PART 2                          Output
BUMP d 1                        a         (a moves to d's first choice: a and d stop being a mutual pair)
BUMP b 2                        c         (c becomes b's second choice: b and c become mutual second choices)
BUMP b 1                        NONE

PART 3                          Output
PAIRS                           a c 0
                                a d 2
                                b d 2
                                b c 3
BEST d                          a 2       (a d and b d both score 2; d ranks a (1) above b (2))
BEST b                          d 2

PART 4                          Output
CYCLES 3                        a c b     (a wants c's, c wants b's, b wants a's)
                                a d b
                                a d c
                                b d c
CYCLES 2                        a c
                                a d
                                b c
                                b d
```

## Edge cases hidden tests are known to target
- rank beyond a user's list length (`RANK b 2` when the partner has only 2 entries) → `false`, no IndexError
- unknown user in any query → `false` / `NONE`
- `BUMP u 0` (nothing above) and `BUMP u r` with `r ≥ len` → `NONE`
- a user listing themselves is ignored for pairing purposes; empty wishlist `u:` is valid
- users who appear only inside others' wishlists (never define a list) behave as having an empty list
- both affected users returned by `BUMP` (the entry moving up first, then the displaced one)
- `PAIRS` prints each pair once with `u < v`; score ties ordered by names
- `CYCLES` must not print rotations/duplicates of the same cycle; `CYCLES 2` equals `PAIRS` without scores

## Variants seen in the wild
- adonais0 (2021 phone) names Part 2 `changed_antipairings(username, rank)` — same semantics.
- 1point3acres reports the input as a dict `{'a': ['c','d'], ...}` handed to the function rather than stdin.
- Best-match / cycle parts (3–4) are our reconstruction of the "wishlist" follow-ups reported only by title.

## What this tests
skills: S02 parsing · S03 records keyed by id · S08 deterministic ordering · S13 index / off-by-one
discipline · S18 validation of missing keys and ranks · S19 incremental design · S20 self-testing

## Sources
- https://github.com/joeytor/StripeInterview (`src/main/java/MutualRank.java`, README → Phone Interview; verbatim Parts 1–2 + examples)
- https://adonais0.github.io/20210603/interview-stripe/ ("Wishlist", phone, 2021; `changed_antipairings`)
- https://www.1point3acres.com/bbs/thread-851458-1-1.html (条纹电面: "mutualRank / wishlist / airbnb-like rental service")
- https://www.1point3acres.com/bbs/thread-804154-1-1.html (2021-10 条纹店面: "Wishlist" with mutual-rank variants)
- https://www.1point3acres.com/bbs/thread-873287-1-1.html (2022-03 电面 prep list "mutual rank … wishlist")
- https://www.1point3acres.com/bbs/thread-1028744-1-1.html (2023-11 店面高频题整理: mutual rank)
