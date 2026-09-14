---
nodes: [algorithms.sliding-window, toolbox.sorted, transfer.stripe-oa]
tags: [stripe-oa, q40]
---
# Drill: proximity search over word positions, then a minimal window and document ranking

Sixty minutes, stdin to stdout. Given a text and a query, find where the
query's words occur close together. Part 1 returns every index of the
query's first word for which every other query word occurs strictly after it
and within `k` word-positions. Part 2 replaces that with the shortest
contiguous span of words that contains all query words in any order,
tie-breaking to the earliest start. Part 3 makes both robust to case and
punctuation by tokenizing on maximal runs of letters and digits. Part 4
applies Part 2 across several named documents and ranks them by window
length, dropping any document missing a query word. The interviewer's own
follow-up — worth doing before Part 2 — is to preprocess the text into a
word-to-sorted-positions index so repeated queries don't rescan it.

**Constraints to state and honor**
- Word positions are 0-based; tokens are whitespace-separated in Parts 1–2
  and matched exactly (case and punctuation included).
- Part 1's window condition is `i < p ≤ i + k` — the other word must be
  strictly after the anchor and at most `k` positions later; a one-word
  query returns all its positions.
- Part 2's minimal-window search treats words in any order and needs `None`
  when some query word never occurs at all.
- Part 3's tokenizer is `[a-z0-9]+` on the lowercased text, applied
  identically to the query.
- Part 4 sorts by `(window length, input order)` and silently omits
  documents missing a word — never prints a sentinel for them.

**Grading points**
- Build the `word -> sorted positions` index once and use `bisect` for Part
  1's lookups — say why up front, since the interviewer asked for exactly
  this as a follow-up.
- Part 2 is LC 76's minimum-window-substring pattern moved from characters
  to word tokens — a `have`/`need` counter sliding window, not a fresh scan
  per query.
- The `k`-boundary in Part 1 is asymmetric and easy to get backwards:
  distance exactly `k` counts, `k - 1` does not, and a match before the
  anchor never counts even at distance 0.
- Tie-breaking for the minimal window is strict `<` on length, earliest
  start wins — and "any order" means a word appearing before the anchor can
  still shrink the window.
- Punctuation normalization is applied to the query too, not just the text,
  and happens once at the boundary rather than inline in the search.
- Part 4's silent omission of missing-word documents is a different
  contract from Parts 1–2's explicit `[]`/`None`/`-1` — don't reuse one
  sentinel for both.

**Source**
- `vault/interviews/companies/stripe/problems/q40_query_words_within_k/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q40_query_words_within_k.md`, `vault/interviews/companies/stripe/problems/q40_query_words_within_k/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
