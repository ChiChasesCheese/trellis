# ps03 · Brace Expansion — glob-style `{a,b,c}` template expansion, robustness, nesting

**Type:** technical phone screen ("Team Screen") · **Stage:** 60 min (45 coding + 15 Q&A), 3 parts · **Last asked:** 2026-08 (InterviewDB "Expansion — Phone", 5 days old at scrape time)
**Frequency:** verbatim LeetCode Discuss screening report (Bangalore backend, 2024-06); interviewdb.io keeps "Expansion" active in 2026; hackerprep.io files it as "Bracket Expansion (Stack)" · **Confidence:** high for Part 1 (three independent worked examples in the source); Part 2/3 rules reconstructed from the source's own follow-up description ("incomplete/mismatched brackets, fewer than 2 tokens, no brackets — return as-is; nested brackets") — see Sources.

## Context
Stripe's screening version of this question reads like a shell: `"/2022/{jan,feb,march}/report"`
expands to three report paths; `"read.txt{,.bak}"` expands to a file and its backup. This is
glob-style expansion of file name templates, webhook endpoint patterns, or price-ID templates —
one comma-separated group at a time. The interviewer then pushes on malformed input and, if time
remains, nested groups and multiple groups in one pattern (a cartesian product).

**This is deliberately not `problems/qA03_lc1087_brace_expansion`** (the LeetCode-tagged
algorithm version of this problem already in this repo): qA03 returns `sorted(set(...))`
(dictionary order, deduplicated) because that is what LC 1087 asks for. This phone-screen version
asks for the opposite contract — **order preserved** (first-listed token first) and **duplicates
kept** — because that is what the sourced report's examples show and what a shell-glob / template
expansion actually does. If you catch yourself reaching for `sorted(set(...))` here, stop: it
silently violates both order and multiplicity requirements below.

## Input (stdin)
First line `PART n` (n ∈ 1..3). Then one **pattern** per line — a template string that mixes
literal characters with brace groups. Each line is independent (its own test case); blank lines
are ignored. Every line is stripped of leading/trailing whitespace before parsing.

## Output
One line per input pattern, **in input order**: the pattern's expansions joined by `,` (no
spaces), in the order defined below. A malformed pattern (Parts 2–3) or a pattern with no group
at all (any part) produces exactly one "expansion" — the original string, unchanged.

## Rules
### Part 1 — single-group expansion  `expand_braces(pattern: str) -> list[str]`
`pattern` contains **at most one** `{tok1,tok2,...}` group (comma-separated tokens; a token may
be empty or multi-character; no nesting). Everything before and after the group is a literal
prefix/suffix, kept verbatim on every output. Result: one string per token, **tokens in the order
written**, `prefix + token + suffix`. A pattern with no group at all is returned as
`[pattern]` (one "expansion": itself). Input is assumed well-formed — Part 1 is not tested on
malformed input; that is Part 2.

### Part 2 — malformed input  `expand_braces_safe(pattern: str) -> list[str]`
Same scope as Part 1 (at most one group, no nesting), but now the input may be malformed:
unmatched braces (`{` with no `}`, or a stray `}`), **a second group** (out of this part's scope —
that capability arrives in Part 3), a **nested** `{` inside the group (same reason), or a group
with **fewer than 2** comma-separated tokens (`{single}`, `{}`). In every one of these cases,
**return the pattern unchanged** — `[pattern]` — do not raise, do not print an error string. A
well-formed single-group pattern still expands exactly as in Part 1.

### Part 3 — nesting and multiple groups  `expand_braces_nested(pattern: str) -> list[str]`
Two new capabilities, both cartesian-product style, **left to right, outer group first**:
* **Multiple top-level groups**: `{a,b}{1,2}` → `a1, a2, b1, b2` (the leftmost group is the outer
  loop, exactly like bash brace expansion: `echo {a,b}{1,2}`).
* **Nested groups**: inside a group, each comma-separated alternative may itself contain groups.
  `{a,{b,c}}d` → alternative `a` (literal) then alternative `{b,c}` (expands to `b`, `c`), in that
  written order, each followed by the outer suffix `d` → `ad, bd, cd`.

Malformed-input handling still applies, generalized to any depth: unmatched braces anywhere, or
**any** group (top-level or nested) with fewer than 2 alternatives, makes the **whole pattern**
malformed → return `[pattern]` unchanged (even if the malformed group is buried three levels
deep). Order is never sorted and duplicate expansions are never removed at any part.

## Worked examples
Part 1 (well-formed, single group):
```
PART 1
/2022/{jan,feb,march}/report
over{crowd,eager,bold,fond}ness
read.txt{,.bak}
{z,a,z}
no braces here
```
→
```
/2022/jan/report,/2022/feb/report,/2022/march/report
overcrowdness,overeagerness,overboldness,overfondness
read.txt,read.txt.bak
z,a,z
no braces here
```
(`{z,a,z}` is neither sorted nor deduped — `z` appears twice, in the order written; contrast with
qA03's `{z,a,z}` under LC 1087 rules, which would give `["a", "z"]`.)

Part 2 (malformed → echoed unchanged; last line still expands normally):
```
PART 2
over{crowd,eager
over}crowd
{onlyone}
{}
a{b,{c,d}}e
{a,b}x{1,2}
read.txt{,.bak}
```
→
```
over{crowd,eager
over}crowd
{onlyone}
{}
a{b,{c,d}}e
{a,b}x{1,2}
read.txt,read.txt.bak
```
(The 5th and 6th lines are malformed **under Part 2's scope** — a nested group and a second
group, respectively — even though both are perfectly well-formed once Part 3 arrives.)

Part 3 (nesting + multiple groups now valid; still malformed → echoed):
```
PART 3
{a,{b,c}}d
{a,b}{1,2}
a{b,{c,d}}e
{a,{single}}
x{a,b}y{1,2}z
over{crowd
```
→
```
ad,bd,cd
a1,a2,b1,b2
abe,ace,ade
{a,{single}}
xay1z,xay2z,xby1z,xby2z
over{crowd
```
(`{a,{single}}` is malformed because its inner alternative `{single}` has only 1 token — the
whole pattern, not just that alternative, is echoed back.)

## Edge cases hidden tests are known to target
- empty token inside a group (`read.txt{,.bak}`, `{,x}`) — the empty string is a valid token
- group at the very start (`{a,b}suffix`) or very end (`prefix{a,b}`) or the whole pattern
  (`{a,b,c}` with no literal at all)
- duplicate tokens are kept and not reordered (`{z,a,z}` → `z,a,z`, not `a,z,z`)
- a pattern with zero braces returns `[pattern]` at every part, not an error
- Part 2: unmatched open, unmatched close, `{}` (0 real tokens), `{single}` (1 token), a second
  top-level group, a nested group — all six echo the pattern unchanged
- Part 3: malformed detection is recursive — a `< 2`-token group nested three levels deep still
  invalidates the whole pattern
- Part 3 cartesian product order: `{a,b}{1,2}` is `a1,a2,b1,b2` (left group outer), not
  `a1,b1,a2,b2`
- very long patterns / many patterns per run (perf: 10,000 lines, one moderate group each)

## Variants seen in the wild
- **Dictionary-order, deduplicated output** (LeetCode 1087 tag data, `problems/qA03_lc1087_brace_expansion`
  in this repo) — a different, sorted+dedup contract; do not conflate the two.
- **"How many words, without listing them"** and **"give me the k-th word"** follow-ups (same LC
  Discuss report family) — implemented as `count_expansions` / `kth_expansion` in qA03 Part 4, not
  reproduced here since this problem set's Part 3 already covers the nesting follow-up.
- Multi-character tokens are explicitly allowed in the Stripe screening version (`{jan,feb,march}`,
  `{crowd,eager,bold,fond}`) — LC 1087 restricts tokens to single lowercase letters.

## What this tests
skills: S02 parsing (segment/brace scanning) · S14 normalisation-free order preservation · S18
input validation without exceptions · S19 incremental design (Part 1 scope deliberately narrowed
so Part 2's malformed-echo rule and Part 3's capability expansion are each a real, testable step)
· S21 recursion / cartesian product

## Sources
- https://leetcode.com/discuss/interview-experience/5341224/Stripe-or-Backend-Engineer-or-Bangalore-or-Jun-2024-or-Reject/ (verbatim: "Part 1 — parse brackets and generate all combinations... e.g. `/2022/{jan,feb,march}/report`... `over{crowd,eager,bold,fond}ness`... `read.txt{,.bak}`"; follow-ups: "handle incomplete/mismatched brackets, fewer than 2 comma-separated values, or no brackets at all (return string as-is)"; "candidate only got through the first follow-up... they usually have 2-3 follow up questions")
- https://www.interviewdb.io/question/stripe ("Expansion — Phone", listed as recently asked, 2026)
- https://hackerprep.io/company/stripe/bracket-expansion (filed as "Bracket Expansion (Stack)"; paywalled, title/tag only)
- `loop/raw/en_forums.md` §3.3 P4 "Bracket / Brace Expansion" (this repo's own collation of the above)

## Clarifications (author's own, not sourced — the raw report gives no output format)
- Output format (comma-joined, one line per pattern) is this repo's convention, chosen to keep
  stdin/stdout deterministic across multiple independent patterns per run; the source only
  describes the returned list, not a serialization.
- Part 2's "second group" and "nested group" cases are treated as malformed (echoed unchanged)
  rather than partially expanded, because Part 1/2's stated scope is "at most one, un-nested
  group" — Part 3 is what explicitly lifts that restriction, matching the source's own "nested
  brackets" follow-up framing.
