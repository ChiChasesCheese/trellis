# qA10 · LC 161 One Edit Distance — single pass, adjacent swap, name the edit, within-k via banded DP

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** phone screen warm-up / OA helper (the q05 Part 4 "corrupted card" logic) · **Last asked:** tag snapshot 2026-07-12 (>6 months bucket)
**Frequency:** tag freq 61.2 (liquidslr All, 2025-06), 67.1 (liquidslr >6mo), 62.5 all / 62.5 >6mo (snehasishroy 2026-07) · 3 tag mirrors · **Confidence:** high (tag data), medium (no dated candidate write-up names it; q05 Part 4 uses the same rule)

LC 161 · *One Edit Distance* · Medium · https://leetcode.com/problems/one-edit-distance

## The problem (restated)
Two strings `s` and `t` are *one edit apart* when you can turn `s` into `t` with **exactly one** of:
insert one character, delete one character, or replace one character. Return whether `s` and `t` are
one edit apart. Identical strings are **not** (zero edits ≠ one edit). Characters are ASCII letters and
digits. LC limits: `0 ≤ len(s), len(t) ≤ 10^4`.

## Context
Stripe's OA "corrupted card number" part (q05 Part 4) asks which valid card numbers are one error away
from what the customer typed — a changed digit *or two adjacent digits swapped*. Radar's typo
detection, Atlas company-name near-duplicates (q06) and idempotency-key fuzzing all need the same
primitive: is this string one keystroke away from that one, and which keystroke? LC 161 is the
primitive; the follow-ups add the adjacent swap (Damerau), return the edit itself, and generalise to
"within k edits" with a DP that must not be O(n·m) at n = 10^4.

## Input (stdin)
```
PART n                 # 1..4
K k                    # Part 4 only, non-negative integer
s                      # line 3 (may be empty)
t                      # line 4 (may be empty)
```
`s` and `t` are the two lines after the header (after `K k` in Part 4), with the line ending removed;
an absent line is the empty string. They contain no spaces.

## Output
* Parts 1, 2, 4: one line `true` or `false`.
* Part 3: one line `kind index [char]`: `insert i c` (insert `c` before position `i` of `s`),
  `delete i` (delete `s[i]`), `replace i c` (set `s[i] = c`), `swap i` (swap `s[i]` and `s[i+1]`), or
  `none` when the strings are not one edit apart (swap counted as one edit).

## Rules
### Part 1 — LC signature  `is_one_edit_distance(s, t) -> bool`
Let `s` be the shorter (swap if needed). If `len(t) − len(s) > 1` → false. Walk both from the left to
the first index `i` where they differ; if there is none, the strings are one edit apart **iff the lengths
differ by exactly one** (identical → false). Otherwise: equal lengths → the rest after `i` must match
(`s[i+1:] == t[i+1:]`); lengths differ by one → `s[i:] == t[i+1:]` (the longer one has an extra
character at `i`). Single pass, O(n) time, O(1) extra space (slices are allowed but stop after the
first mismatch).

### Part 2 — adjacent swap counts as one edit  `is_one_edit_or_swap(s, t) -> bool`
Part 1, **or** `len(s) == len(t)` and the strings differ at exactly two positions `i` and `i+1` with
`s[i] == t[i+1]` and `s[i+1] == t[i]` (a transposition of two *different* characters — swapping equal
characters changes nothing and is not an edit). This is the q05 Part 4 rule ("one digit changed or two
adjacent digits swapped"). Optimal string alignment distance = 1.

### Part 3 — name the edit  `find_edit(s, t) -> Edit | None`
`Edit(kind, index, char)` (NamedTuple; `char` is `""` for `delete` and `swap`). The edit that turns `s`
into `t`; `None` if none (identical strings → `None`). Determinism: `index` is the **first** index where
`s` and `t` differ (`len(s)` when `s` is a proper prefix of `t`, so `"aa" → "aaa"` is `insert 2 a`, not
`insert 0 a`). Kinds never collide: `swap` changes two positions, `replace` one, and `insert`/`delete`
change the length.

### Part 4 — within k edits  `within_k_edits(s, t, k) -> bool`
Levenshtein distance (insert/delete/replace, no swap) `≤ k`. Requirements: `abs(len(s) − len(t)) > k`
→ false immediately; `k = 0` → equality; the DP must be **banded** — only cells with `|i − j| ≤ k`
are computed (O(k·n) time, O(k) memory), so `n = 10^4, k = 50` runs in well under a second where
the full O(n·m) table would not. Note `within_k_edits(s, t, 1)` is `s == t or is_one_edit_distance(s, t)`.

## Worked examples
```
LC ex1  s="ab"  t="acb"  -> true    (insert c)
LC ex2  s=""    t=""     -> false   (zero edits)
        s="a"   t=""     -> true    (delete)
        s="cab" t="ad"   -> false
Part 1  "abc"/"abx" -> true ; "abc"/"axx" -> false ; "abc"/"abcde" -> false (length diff 2)
        "abc"/"abc" -> false ; "abc"/"abcd" -> true ; "abc"/"xabc" -> true
Part 2  "ab"/"ba" -> true (swap) ; "abcd"/"abdc" -> true ; "aa"/"aa" -> false (swap of equal chars is
        no edit) ; "abc"/"bca" -> false (that is two swaps) ; "ab"/"acb" -> true (Part 1 still applies)
Part 3  "ab"/"acb"  -> Edit("insert", 1, "c")     "acb"/"ab" -> Edit("delete", 1, "")
        "abc"/"axc" -> Edit("replace", 1, "x")    "abc"/"bac" -> Edit("swap", 0, "")
        "aa"/"aaa"  -> Edit("insert", 2, "a")     "abc"/"abc" -> None    "abc"/"bca" -> None
Part 4  "kitten"/"sitting" k=3 -> true ; k=2 -> false   (distance 3)
        "abc"/"abc" k=0 -> true ; "abc"/"abd" k=0 -> false
        "flaw"/"lawn" k=2 -> true (delete f, insert n) ; k=1 -> false
        s="a"*10000 t="a"*9999+"b" k=1 -> true
```
stdin for Part 3:
```
PART 3
ab
acb
```
→ `insert 1 c`
stdin for Part 4 (`PART 4` / `K 2` / `kitten` / `sitting`) → `false`

## Edge cases hidden tests are known to target
- identical strings → false (the most common wrong answer), including two empty strings
- one empty, the other of length 1 → true; length 2 → false
- difference in the last character; extra character at the very beginning or very end
- the "first mismatch" must be found by scanning, not by assuming the extra character is at the end
- Part 2: a transposition of two equal characters is not an edit; `"ab"/"ba"` is not a replace
- Part 3: insertion index is the first mismatch (`"aa"/"aaa"` → 2)
- Part 4: length difference alone decides when it exceeds k; band edges at `|i − j| == k`; `k = 0`

## Variants seen in the wild
- q05 Part 4: enumerate all strings one edit/swap away and keep the valid card numbers.
- LC 72 Edit Distance (full Levenshtein) and LC 583 — the un-banded DP.
- "Is `t` a typo of `s`?" in fraud/Radar screens: Damerau distance ≤ 1 with case folding (q06 style).

## Why Stripe asks it
A five-minute string question that still separates careful candidates (identical strings, both empty,
extra char at either end) from sloppy ones, and it is literally the helper the OA's corrupted-card part
needs. The k-edit follow-up checks whether the candidate knows the banded DP rather than reaching for
the O(n·m) table on 10^4-character inputs.

## Stripe-flavored follow-ups
1. Adjacent transposition as one edit (card-number typos, q05 Part 4) — Part 2.
2. Return the edit (to explain "did you mean …") — Part 3.
3. Within k edits with a banded DP; then Damerau within k (add the transposition transition).

## What this tests
skills: A12 one-edit distance · S13 off-by-one discipline · S14 string canonicalisation · S15 masked-input combinatorics · S21 stdlib fluency

## Sources
- https://leetcode.com/problems/one-edit-distance
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 61.2)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (freq 67.1)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (freq 62.5 all / 62.5 >6mo)
- catalog/raw/github_repos.md §30 (tag table, freq 61.2)
- problems/q05_card_validation_luhn (Part 4 — the same one-edit-or-swap rule on card numbers)
