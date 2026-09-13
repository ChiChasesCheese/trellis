# qA03 LC 1087 Brace Expansion — report

## Summary
Shell-style `{a,b}` template expansion. Tag freq 82–89, a verbatim Stripe screening report (LC
Discuss, Jun 2024) with the exact examples and the "echo malformed input" follow-up, InterviewDB
"Expansion — Phone" (Aug 2026), hackerprep "Bracket Expansion (Stack)". Parsing with a stack, a
cartesian product, a sort — then validation, nesting, and counting/indexing without materializing.

## Sources & confidence
high — LC Discuss 5341224 (verbatim), liquidslr (82.0 / 88.8), shreeratn (51.5), snehasishroy
(87.5), InterviewDB, hackerprep, 3 prep repos (Hazeera65, premjm-67, TWINSRIRAM brace_followup).

## Approach by part
1. `parse_segments` → `Segment(options, is_group)` via a one-level scanner that returns `None` on
   nested `{`, stray `}`, or unclosed `{`. Iterative product, `sorted(set(...))`. `echo_malformed`
   returns `[s]` on malformed / no group / a group with < 2 tokens (screening rule).
2. Same segments, DFS with prefix; tested equal to Part 1 on 300 random templates.
3. LC 1096 stack of `(alternatives, current)` frames: `{` push, `,` close alternative, `}` union
   then product with the enclosing `current`.
4. `count` = product of distinct options per group; `kth` = mixed-radix decode of `k-1` with the
   leftmost group most significant — equals `brace_expansion(s)[k-1]` under single-letter options.

## Pitfalls hidden tests target
- sorting per group instead of globally (`{ab,a}{c,bc}`); forgetting to dedupe
- empty token `{,.bak}`; group at position 0 / end; adjacent groups
- malformed cases: reversed braces, unclosed, `{}` (one empty token), `{x}` (one token)
- nested union must dedupe (`{{a,z},a{b,c},{ab,z}}` → 4 words, not 5)
- count/k-th must not enumerate (10^20-word template test)

## Complexity & measured cost
Parts 1–3: O(total output size); Part 4: O(len(s)). Measured: 0.10s (60 expansions at LC max
2187 words + two 10^5-word stress expansions + script run); script run at LC max ≈ 0.03 s, ~10 MB.

## Test inventory
16 tests — part1: 8 (incl. 1 io, 1 perf) · part2: 2 · part3: 3 · part4: 3; edge 7 · fmt 1.

## Skills exercised
A04 stack/backtracking expansion · S02 parsing · S08 deterministic ordering · S14 string handling · S18 validation
