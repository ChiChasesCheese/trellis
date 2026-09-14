---
nodes: [algorithms.backtracking, input.grammar]
tags: [stripe-oa, qa03, leetcode]
---
# Drill: brace expansion, from a stack parser to nesting, counting and indexing

Forty-five minutes, stdin to stdout. This is LeetCode 1087, Brace Expansion:
given a shell-style template of literal text and comma-separated brace
groups, expand it into every combination, sorted and deduplicated. Part 1
parses the template into segments and expands iteratively with a stack-like
scan, plus a malformed-input mode that echoes the template unchanged instead
of crashing. Part 2 gets the same result by recursive backtracking and must
agree with Part 1 everywhere. Part 3 moves to LeetCode 1096's nested
grammar, where braces can contain braces and concatenation and union
interact like a cartesian product and a set union. Part 4 counts the number
of expansions and finds the k-th one without ever materializing the list,
which for some templates is astronomically large.

**Constraints to state and honor**
- A template is literal characters plus `{opt,opt,...}` groups; options may
  be multi-character or empty, and a group can appear anywhere including the
  edges.
- Part 1's malformed-input mode returns the template unchanged when there's
  no group, an unmatched or nested brace, or any group with fewer than two
  options.
- Part 3's grammar allows nesting: concatenation is a cartesian product,
  comma inside braces is a set union, and nested unions must still dedupe.
- Part 4 must not enumerate to count or index — the count is a product over
  groups of distinct-option counts, and indexing is a mixed-radix decode.
- Output for Parts 1–3 is globally sorted, distinct words — sorting within a
  group is not the same as sorting the final output.

**Grading points**
- Parsing is a single-pass scanner that classifies each segment (literal vs.
  group) up front, so the expansion step is a clean cartesian product over a
  list of option-lists — state the parse/expand separation before coding
  either.
- Malformed detection must be checked, not assumed away: a nested `{`, a
  stray `}` before any `{`, and a group with one option are three distinct
  cases to test, not one.
- Global sort-and-dedupe happens once at the end (`sorted(set(...))`), never
  per group — an unsorted or duplicate-option group is a good adversarial
  test.
- Part 3's stack of `(alternatives, current)` frames should be described
  before coding it, since nesting is the one place where
  concatenation-as-product and comma-as-union have to compose correctly.
- Part 4's count and k-th must run in O(len(s)) regardless of how large the
  expansion is, and the interview should surface that choice-order equals
  lexicographic order only because options here are single letters — say
  when that stops being true.

**Source**
- `vault/interviews/companies/stripe/problems/qA03_lc1087_brace_expansion/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/qA03_lc1087_brace_expansion.md`, `vault/interviews/companies/stripe/problems/qA03_lc1087_brace_expansion/problem.md`

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
