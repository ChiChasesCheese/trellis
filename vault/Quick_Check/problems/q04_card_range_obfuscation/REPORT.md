# q04 Card Range Obfuscation — report

## Summary
Extend the brand intervals published for one 6-digit BIN so the whole 10-digit offset range
`0000000000..9999999999` is covered, then merge same-brand neighbours and print 16-digit
zero-padded rows in canonical order. It is Stripe's card-metadata table hardened against
BIN-gap probing, reduced to inclusive-interval arithmetic. Four accumulating parts: outer ends
→ interior gaps → nested intervals → same-brand merge. The difficulty is which interval owns a
gap (the running-maximum end, not the previous row) and the inclusive `next.start − 1` edge.

## Sources & confidence
high — 7 independent mentions: csoahelp 2024-11-04 (4 parts, per-part test counts 4/4/2/3,
samples 1–2), programhelp 2025-08-07, linkjob 2025-09-16, extrabrain 2026-02-10, scribd "Card
Range Obfuscation Methodology", 1024bbs 10992, 1point3acres thread-1085478.
- https://extrabrain.app/interview-questions/stripe-hackerrank-online-assessment-extrabrain/
- https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/
- https://programhelp.net/en/oa/stripe-hackerrank-online-assessment-questions-guide/

## Approach by part
Parse into mutable `[start, end, brand]` with full numbers `LO + offset` (`LO = BIN·10^10`; a
token ≥ 10^10 is already a full number). One program; `PART n` selects how far to go.
1. `extend_outer`: `min(start)` → `LO`, `max(end)` → `HI` (tie on end → smaller start).
2. `fill_gaps`: walk in sorted order with an `owner` = interval holding the running maximum
   end; when `iv.start > owner.end + 1` set `owner.end = iv.start − 1` (inclusive; touching is
   not a gap). Overlaps are left untrimmed.
3. Same walk — `owner` only changes on a strict `iv.end > owner.end`, so a contained interval
   never becomes the owner and the covering one (smaller start on ties) is the one extended.
4. `merge_same_brand`: single pass over the sorted list; merge when brand strings are equal and
   `iv.start <= cur.end + 1`. Render sorted by `(start, end, brand)` on the final values, `%016d`.

## Pitfalls hidden tests target
- gap filler ends at `next.start − 1`; `end + 1 == next.start` is touching, never extended or
  merged across brands
- Part 3: extending the row printed just before the gap (the contained one) instead of the
  interval owning the max end; a contained interval prints after its cover
- leading-zero offsets (`0000000000`), zero-padded 16-digit output, `N = 0` → nothing,
  `N = 1` → whole range; duplicates kept in Parts 1–3 and merged in Part 4
- brand compared exactly (`VISA` ≠ `Visa`); unsorted input; integer math only (10^16 exceeds
  exact float spacing)

## Complexity & measured cost
O(n log n) for the sort, O(n) memory. 100k random shuffled intervals: ~0.30 s, ~69 MB RSS
(budget 2 s / 256 MB).
Measured: 0.295s, 69 MB

## Test inventory
24 tests — part1: 8 · part2: 4 · part3: 4 · part4: 8; edge 13 · fmt 1 · perf 1 · io 2.
`IMPL=starter`: 23 fail / 1 pass (`N = 0` prints nothing is satisfied by the empty stub).

## Skills exercised
S01 full-spec reading · S02 parsing · S08 deterministic sort · S09 zero-padded formatting ·
S13 inclusive interval logic · S19 incremental design · S20 self-testing (touching vs gap)
