# q18 · Six Degrees of Collusion — fraud rings from shared identifiers

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 3 questions building on each other, 20 hidden tests) · **Last asked:** 2026-07-09 (LeetCode post); 2026-06-24 (1point3acres 题库)
**Frequency:** 5 independent sources (LeetCode 8385570 verbatim, 1point3acres 题库 "Six Degrees of Collusion", csoahelp 2026-07-22 VO, linkjob 2025-12-07 phone screen "User Record Linking", InterviewDB "Collusion — OA") · **Confidence:** high for Parts 1–3 (verbatim examples), medium for Part 4 (phone-screen variant)

## Context
Stripe Radar looks for *collusion rings*: sets of customer accounts that share devices, cards
or contact details. Two accounts that share any identifier are directly linked; links are
transitive (A shares a device with B, B shares a card with C → A, B, C are one ring). Given
transaction records, you find who is directly linked to a suspect, measure the suspect's ring,
score each ring's risk, and decide whether to block.

## Input (stdin)
First line `PART n` (1–4). Records follow, one per line, blank lines ignored. Fields are
`:`-separated and trimmed. A customer may appear on many records. Up to 10^5 records.

* Parts 1–2: `customer:device_id[:credit_card_id]` — any number of identifier fields ≥ 1
  (`A:d1`, `A:d1:123`). Every non-customer field is an identifier; fields at the **same
  position** are compared (a device never links to a card). Empty fields link nothing.
* Part 3: `customer:device_id:credit_card_id:risk_factor` (`risk_factor` integer 0–100).
* Part 4: `user_id,name,email,company` (comma-separated, §24 record-linking variant).

Second line (after `PART n`): Part 1 `<target>`; Part 2 `<target> <K>`; Part 4 `<target> <threshold>`.

## Output
* Part 1: directly linked customers, **sorted, one per line**, `NONE` if none.
* Part 2: `<ring size> BLOCK` or `<ring size> ALLOW`.
* Part 3: one line per ring, `<members sorted, comma-joined> <risk>` (risk two decimals).
* Part 4: users linked to the target with confidence ≥ threshold, sorted, `NONE` if none.

## Rules
### Part 1 — direct links
`direct_links(records, target)` → sorted list of customers (≠ target, deduped) that share at
least one identifier value with the target **at the same field position**. Unknown target → `[]`.

### Part 2 — fraud ring size & block decision
`groups(records)` → the connected components of the link graph (union-find / BFS): customers
sharing an identifier are in the same group, transitively. `ring_size(records, target)` = size of
the target's component **including the target** (a customer with no links has ring size 1;
unknown target → 0). `largest_ring(records)` = max component size (0 for no records).
`should_block(records, target, k)` = `ring_size ≥ k` (non-strict).

### Part 3 — ring risk scoring
Each record now carries a `risk_factor`. A customer's risk = the risk on its **last** record
(records are chronological). Ring risk = **mean risk of the members after removing members
with risk 0** (they are treated as verified / not part of the scoring); a ring whose members all
have risk 0 scores `0`. `ring_risks(records)` returns one score per ring in order of the ring's
**first-appearing customer**.

### Part 4 — weighted link confidence (record-linking variant, phone screen)
Records `user_id,name,email,company`. Two users are linked with confidence
`Σ weight(field)` over the fields where both values are non-empty and equal
case-insensitively; default weights `name 0.2, email 0.5, company 0.3`, threshold `0.5`.
`weighted_links(records, target, weights=..., threshold=0.5)` → sorted user ids with
confidence ≥ threshold (non-strict; compare in integer thousandths so 0.2 + 0.3 ≥ 0.5 holds).

## Worked examples
Example 1 (LeetCode Q1 — groups):
```
PART 2                       records: A:d1  B:d2  C:d3  D:d2  B:d3
B 3                          -> groups {A}, {B,C,D}  -> "3 BLOCK"    (ring of B = 3 ≥ K=3)
```
Example 2 (LeetCode Q2 — largest ring; device OR card links):
```
records: A:d1:123  B:d2:456  C:d3:123  D:d2:789  E:d2:999
-> groups {A,C} (card 123), {B,D,E} (device d2) -> largest_ring = 3
PART 1 / target A -> C          PART 2 / "A 3" -> "2 ALLOW"
```
Example 3 (LeetCode Q3 — ring risk, zero-risk members dropped):
```
PART 3
A:d1:123:90  B:d2:456:50  C:d3:123:0  D:d2:789:100  E:d2:999:30
-> ring_risks = [90, 60]        stdout:   A,C 90.00
                                          B,D,E 60.00
```
Example 4 (Part 4 — linkjob weights):
```
PART 4
u1 0.5
u1,alice smith,alice@x.com,acme
u2,alice smith,other@x.com,acme      (name .2 + company .3 = .5  -> linked)
u3,bob,alice@x.com,zzz               (email .5                 -> linked)
u4,alice smith,,                     (name .2                  -> not linked)
-> u2
   u3
```

## Edge cases hidden tests are known to target
- target excluded from its own direct-link list; a customer with several records links through
  all of them; the same pair linked by two identifiers is listed once
- self-only customer: `direct_links` → `[]`, `ring_size` → 1; unknown target → `[]` / 0
- identifiers at different positions never link (`A:x:y` and `B:y:x`); empty field links nothing
- ring size counts the target itself; `K` boundary: size == K blocks, K+1 allows
- long chains (A–B–C–D–E) are one ring — BFS/union-find, not one-hop
- risk: members with 0 are removed **before** averaging; all-zero ring → 0; risk is the last
  record's value; output in first-appearance order of rings, members sorted
- Part 4 threshold non-strict and float-safe (`0.2 + 0.3` must count as `0.5`); matching is
  case-insensitive and ignores empty fields
- ring-risk rounding: mean printed with two decimals (`(50+100+30)/3 = 60.00`, `(1+2)/2 = 1.50`)

## Variants seen in the wild
- LeetCode Q2's record `E:d2:123` (as posted) would merge every group; the poster's expected
  answer (3) needs it to be a distinct card — the example above uses `999`.
- csoahelp VO (2026-07-22): merchants with `email/phone/website/bank`, P1 shared attribute,
  P2 weighted score ≥ threshold, P3 direct + 1-hop indirect (`weighted_links(..., hops=2)`).
- 1point3acres 1154050: daily data updates, track cluster changes over time (incremental
  union-find — `groups` is idempotent over the accumulated record list, so re-running on the
  appended list is the intended solution).
- 1point3acres OJ titles: "Direct Links" (P1) / "Fraud Ring Size" (P2) / "Risk Scoring" (P3).

## What this tests
skills: S02 parsing · S03 records keyed by id · S04 grouping · S05 threshold semantics · S08
deterministic order · S18 validation · S19 incremental design · A16 union-find / components

## Sources
- https://leetcode.com/discuss/post/8385570/ (Stripe HackerRank OA, 2026-07-09 — verbatim Q1–Q3 examples)
- 1point3acres 题库 `company/stripe/six-degrees-of-collusion-oa` (OA · 60 min · Medium · last asked 2026-06-24; variants "Risk Scoring / Fraud Ring Size / Direct Links")
- csoahelp 2026-07-22 VO 「从商户属性匹配到间接关系查询」
- linkjob 2025-12-07 phone screen "User Record Linking" (weights name 0.2 / email 0.5 / company 0.3, threshold 0.5)
- InterviewDB "Collusion — OA", "Linked User — Phone", "Matching Contacts — Phone"
- 1point3acres 1154050 (cluster tracking with daily updates, union-find)

## Clarifications (from adversarial review, 2026-08-26)
- Risk means are printed with Python `.2f` (round-half-even: 1.125 → `1.12`). If a hidden test expects half-up, switch to `Decimal.quantize(ROUND_HALF_UP)`; the source examples do not hit a .xx5 case.
