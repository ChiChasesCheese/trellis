# q40 Query Words Within k — report

## Summary
Intern phone screen: proximity search over word positions. Part 1 is the source's exact question
(start indices of the first query word such that the other words occur within `k` words after
it); Parts 2–4 are the natural follow-ups (tightest window in any order, punctuation/case
normalization, ranking several documents). The interviewer's own follow-up — preprocess
`word → sorted positions` so repeated queries do not rescan — is the `Document` class.

## Sources & confidence
high — LeetCode discuss 4595354 ("Stripe Intern Interview Question", 2024-01-20) gives the
statement, the `[1, 20]` example (`k = 2`) and the preprocessing follow-up. Single source; the
worked text here is a reconstruction that reproduces `[1, 20]` (the post elides the text).

## Approach by part
1. `Document.positions[word]` sorted; for each position `i` of the first word and each other
   word, `bisect_left(pos, i + 1)` must land on a `p <= i + k` (inclusive end).
2. sliding window over tokens with a `have`/`need` count (LC 76 on words); strict `<` on
   length keeps the earliest window on a tie; `None` if any word is absent.
3. `tokenize(normalize=True)` = `re.findall("[a-z0-9]+", text.lower())`; applied to query too.
4. `min_window` per document with normalization, sort by `(length, input order)`, omit misses.

## Pitfalls hidden tests target
- distance exactly `k` counts; `k = 0`; the other word *before* the start does not count
  (`fox quick` ≠ `quick fox`); duplicate query words
- window ties → earliest; "any order" means `fox quick` is a valid (shorter) window
- `Quick-fox.` → two tokens; exact matching in Parts 1–2 (`Fox,` ≠ `fox`)
- rank: omit documents missing a word (no `-1` rows); ties keep input order

## Complexity & measured cost
Preprocess O(n); Part 1 O(occ(first) · |query| · log n) per query; Part 2 O(n) per query.
Measured: 0.33s, 44 MB (200k-word text, 20 three-word queries, Part 2; Part 1 0.04s;
budget 2 s / 256 MB).

## Test inventory
13 tests — part1: 5 (incl. 1 io) · part2: 4 (incl. 1 perf, 1 brute-force cross-check) · part3: 2 · part4: 2; edge 6.

## Skills exercised
S02 parsing · S08 deterministic tie-break · S13 inclusive/exclusive boundaries · S14 string normalization · S16 sliding window · S19 incremental design
