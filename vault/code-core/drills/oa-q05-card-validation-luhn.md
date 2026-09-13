---
nodes: [algorithms.strings, algorithms.backtracking, transfer.stripe-oa]
tags: [stripe-oa, q05]
---
# Drill: validate, unmask, and repair card numbers

Sixty minutes, stdin to stdout, no libraries beyond the standard one. Card
numbers are validated by two independent facts: their shape (length + prefix)
determines a network, and a Luhn checksum determines whether the digits are
internally consistent. Build this up across four parts, then apply it to two
real-world twists on damaged input.

- Part 1: given a 16-digit number starting with `4`, print `VISA` if the Luhn
  checksum passes, else `INVALID_CHECKSUM`.
- Part 2: given any 15- or 16-digit number, determine the network from length
  and prefix (VISA, MASTERCARD, AMEX); print `UNKNOWN_NETWORK` if no network
  matches (shape is checked before the checksum), else the network name or
  `INVALID_CHECKSUM`.
- Part 3: given a card with 1-5 digits redacted as `*`, count how many
  completions are valid, per network, and print each non-zero count.
- Part 4: given a card with exactly one error (one digit changed, or one pair
  of adjacent digits swapped), enumerate and print every valid original.

**Constraints to state and honor**
- Luhn: from the rightmost digit moving left, double every second digit,
  subtract 9 if the doubled value exceeds 9, and require the total digit sum
  to be divisible by 10.
- Network shape is checked strictly before the checksum — a Luhn-valid number
  of the wrong length/prefix is `UNKNOWN_NETWORK`, never a network name.
- Part 3 masks can hide prefix digits too, so a network can be ruled in or out
  purely by length; up to 5 stars must not be handled by anything that scales
  exponentially and times out.
- Part 4 must deduplicate candidates a digit-change and a swap can both
  produce, must never accept the observed number itself, and swapping two
  equal adjacent digits is not a valid "error."
- Output for Part 3 is one line per network with non-zero count, alphabetical
  by network name; Part 4 output is ascending numeric order, deduplicated.

**Grading points**
- `network_of` (shape) and `luhn_ok` (checksum) built as small independent
  functions shared unchanged across all four parts.
- The order-of-checks trap made explicit: shape first, checksum second —
  candidate should be able to name a Luhn-valid, wrong-shape number as the
  test case that catches getting this backwards.
- Part 3 solved without a brute-force blowup on the maximum mask count — a
  digit-by-digit or mod-10 DP approach, or a candidate who at least reasons
  about the 10^k bound explicitly rather than assuming it's fine.
- Part 4's two candidate generators (single-digit change, adjacent swap) kept
  separate but merged into one deduplicated candidate set before filtering.
- Numeric vs alphabetic/string ordering used correctly in each part (Part 3's
  network names are alphabetical strings; Part 4's card numbers are sorted by
  numeric value, same length so string order happens to coincide, but the
  candidate should say why).
- Recognizes that the original of a corrupted card can belong to a different
  network than the observed (masked or corrupted) prefix suggested.

**Source**
- `vault/stripe/q05_card_validation_luhn/question.md`
- `vault/stripe/q05_card_validation_luhn/solution.md`
- `vault/Quick_Check/problems/q05_card_validation_luhn/problem.md`
- `vault/Quick_Check/problems/q05_card_validation_luhn/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
