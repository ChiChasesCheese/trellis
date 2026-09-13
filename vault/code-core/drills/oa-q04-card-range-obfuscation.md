---
nodes: [chrono.intervals, output.formatting, transfer.stripe-oa]
tags: [stripe-oa, q04]
---
# Drill: fill and merge brand intervals across a card BIN

Sixty minutes, stdin to stdout, no libraries beyond the standard one. Given a
6-digit BIN and a list of `[start, end] -> brand` intervals (10-digit offsets
within the BIN, inclusive endpoints), extend the intervals so the entire BIN
range is covered with no gaps, then merge what can be merged, and print the
canonical, fully-covered table as full 16-digit zero-padded card numbers. One
program accumulates rules; a `PART n` line selects how far to apply them.

- Part 1: extend only the two outer intervals — the one with the smallest
  start moves its start to the BIN's low end, the one with the largest end
  moves its end to the BIN's high end.
- Part 2: also close any interior gap by extending the interval that owns the
  gap's lower edge, up to one less than the next interval's start.
- Part 3: handle intervals nested inside another correctly — the interval
  extended to close a gap is the one holding the running-maximum end seen so
  far, never the contained interval that happens to print just before the gap.
- Part 4: merge consecutive intervals that touch or overlap and share the
  exact same brand string.

**Constraints to state and honor**
- Offsets are 10-digit and inclusive; the full BIN range spans
  `BIN*10^10` through `BIN*10^10 + 9999999999`, about 10^16 — must stay in
  integers, since that magnitude exceeds exact float spacing.
- Touching intervals (`end + 1 == next.start`) are not a gap and are never
  extended or merged across different brands.
- Up to ~10^5 intervals, possibly unsorted, possibly with exact duplicates.
- Output sorted by `(start, end, brand)` on the final, extended values, each
  number zero-padded to 16 digits; `N = 0` prints nothing.

**Grading points**
- The gap-filling rule is inclusive: the gap closes at `next.start - 1`, never
  at `next.start` — this off-by-one is the whole difficulty of the problem.
- The interval chosen to close a gap is tracked as a running "owner holding
  the maximum end seen so far," not the interval immediately preceding the
  gap in sorted order — this is what correctly handles a nested/contained
  interval in Part 3.
- Overlapping intervals are left untrimmed (only extended, never shrunk); a
  contained interval keeps its original bounds and simply sorts after its
  covering interval in the output.
- Brand comparison is exact string equality (`VISA` != `Visa`), reproduced
  verbatim in the output.
- Merging in Part 4 is a single left-to-right pass tracking a "current"
  interval, re-extended whenever the next interval touches/overlaps and
  matches brand exactly.
- Leading-zero offsets parse correctly and the output is zero-padded to a
  fixed 16 digits regardless of BIN or offset magnitude; duplicates stay as
  separate rows through Part 3 and only collapse in Part 4.

**Source**
- `vault/stripe/q04_card_range_obfuscation/question.md`
- `vault/stripe/q04_card_range_obfuscation/solution.md`
- `vault/Quick_Check/problems/q04_card_range_obfuscation/problem.md`
- `vault/Quick_Check/problems/q04_card_range_obfuscation/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
