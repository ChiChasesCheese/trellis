# qA10 LC 161 One Edit Distance — report

## Summary
"Are these strings one keystroke apart?" — the primitive behind the OA's corrupted-card part (q05
Part 4), Atlas near-duplicate names and Radar typo checks. Part 1 is the LC single pass; follow-ups
add the adjacent transposition, return the edit itself, and generalise to Levenshtein ≤ k with a
banded DP that stays O(k·n) at n = 10^4.

## Sources & confidence
tag freq 61.2 / 67.1 (liquidslr 2025-06 All / >6mo), 62.5 / 62.5 (snehasishroy 2026-07); not in the
shreeratn 2025-05 snapshot → high on tag data; no dated write-up names it (medium). Parts 2–4 are
Stripe-flavoured designs; Part 2's rule is verbatim the q05 Part 4 rule.

## Approach by part
1. `_first_mismatch` scans to the first differing index `i`; equal lengths → `i < len` and tails after
   `i` equal; lengths differ by one → `short[i:] == long[i+1:]`; identical → false. O(n), O(1).
2. `find_edit(s, t) is not None` — Part 3 with the transposition case included.
3. Same scan; equal lengths: tails equal → `replace`; else `s[i]==t[i+1] and s[i+1]==t[i]` and tails
   after `i+2` equal → `swap`; length +1 → `insert` at `i`; −1 → `delete` at `i`. Kinds cannot collide.
4. Banded Levenshtein: row `i` stores `j ∈ [i−k, i+k]` in a list of width `2k+1`; `prev[j−1]` is
   `prev[d]`, `prev[j]` is `prev[d+1]`, `cur[j−1]` is `cur[d−1]`; early exit when `min(row) > k`; final
   cell at `d = m − (n − k)`. O(k·n) time, O(k) memory. Cross-checked against the full table on 3000
   random pairs.

## Pitfalls hidden tests target
- identical strings (including two empties) → false; `"" / "a"` → true; `"" / "ab"` → false
- assuming the extra character is at the end (`"abc"/"acbd"` is false)
- `"ab"/"ba"` is false in Part 1 (two replaces), true in Part 2; swap of equal chars is not an edit
- Part 3 insertion index = first mismatch (`"aa"→"aaa"` is `insert 2`), delete of a trailing char
- Part 4: `|len diff| > k` short-circuit, `k = 0` equality, band edges at `|i−j| == k`
- stdin: empty string lines must survive parsing (blank lines are *data* here, not noise)

## Complexity & measured cost
Parts 1–3 O(n) time, O(1) extra (tail slices only after the first mismatch). Part 4 O(k·n) time, O(k)
memory. Measured: 0.34 s for the perf test (50 × Parts 1–3 on 10^4 chars + banded DP at n = 10^4,
k = 50 without early exit + one script run); script run alone 0.14 s, ~16 MB. Budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 6 (incl. 1 io, 1 perf) · part2: 3 · part3: 3 · part4: 3; edge 5.

## Skills exercised
A12 one-edit distance · S13 off-by-one discipline · S14 string canonicalisation · S15 masked-input combinatorics · S21 stdlib fluency
