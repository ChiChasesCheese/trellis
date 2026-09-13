# qA03 · LC 1087 Brace Expansion — stack, backtracking, nested braces, count and k-th word

LC 1087 · *Brace Expansion* · Medium · https://leetcode.com/problems/brace-expansion (nested variant: LC 1096 Brace Expansion II, Hard)

## Context
Stripe's screening version reads like a shell: `"/2022/{jan,feb,march}/report"` → three report paths;
`"over{crowd,eager,bold,fond}ness"` → four words; `"read.txt{,.bak}"` → `read.txt`, `read.txt.bak`.
That is glob-style expansion of file names, webhook endpoint templates, or price-ID patterns — and the
tag data plus a verbatim LC Discuss report (Bangalore backend screen, Jun 2024) show the interviewer
then pushes on: multiple groups (cartesian product), malformed input, nested groups, and "how many
without listing them". hackerprep files it as "Bracket Expansion (Stack)".

## The problem (restated)
A string `s` is a template made of literal characters and **brace groups** `{x,y,z}` (comma-separated
options; no nesting in LC 1087). Each group contributes exactly one of its options; every combination
of choices is a word. Return **all distinct words, sorted lexicographically**. LC limits: `1 ≤ len(s) ≤ 50`,
lowercase letters plus `{`, `}`, `,`; input is valid; options within one group are distinct single
letters. The Stripe screening version relaxes options to arbitrary tokens (multi-character, possibly
empty) and asks what to do with malformed input.

## Input (stdin)
```
PART n          # 1..4
<template>      # the string s
k               # Part 4 only, optional: 1-based index of the word wanted
```

## Output
* Parts 1–3: one word per line in lexicographic order (an empty word prints as an empty line).
* Part 4: the count on the first line; if `k` was given, the k-th word on the second line, or `NONE`
  when `k` is out of range.

## Rules
### Part 1 — iterative (stack) expansion  `brace_expansion(s, echo_malformed=False) -> list[str]`
Parse `s` into segments (a literal is a one-option segment; `{…}` is a group of tokens split on `,`,
tokens may be multi-character or empty). Expand iteratively: start with `[""]`, for each segment append
every option to every partial word. Return `sorted(set(words))`.
`echo_malformed=True` (Stripe screening variant): if the template is malformed — no `{`, `{` without `}`,
`}` before `{`, a nested `{` — **or any group has fewer than 2 tokens**, return `[s]` unchanged.

### Part 2 — recursive backtracking  `brace_expansion_recursive(s) -> list[str]`
Same result via DFS over segments (`dfs(i, prefix)`). Must equal Part 1 on every valid input.

### Part 3 — nested braces (LC 1096 grammar)  `brace_expansion_nested(s) -> list[str]`
Braces may nest and a comma inside a group separates *alternatives* which may themselves contain
groups: `{a,b}{c,{d,e}}` → `ac ad ae bc bd be`; `{{a,z},a{b,c},{ab,z}}` → `a ab ac z` (union dedupes).
Concatenation = cartesian product, comma = set union. Return the sorted distinct words. Use one stack
of `(alternatives, current)` frames pushed on `{` and popped on `}`.

### Part 4 — count and k-th  `count_expansions(s) -> int`, `kth_expansion(s, k) -> str | None`
`count_expansions` = product over groups of the number of **distinct** options (literals count 1),
without materializing words. `kth_expansion(s, k)` (1-based) = the k-th word in **choice order**: each
group's distinct options sorted, the leftmost group most significant (mixed radix on `k-1`). Under the
LC 1087 grammar (single-letter options) choice order **is** lexicographic word order, so
`kth_expansion(s, k) == brace_expansion(s)[k-1]`. `None` when `k < 1` or `k > count`.
(With multi-character tokens the two orders can differ — say so in the interview.)

## Worked examples
```
LC ex1   "{a,b}c{d,e}f"  -> ["acdf","acef","bcdf","bcef"]
LC ex2   "abcd"          -> ["abcd"]
Screen   "/2022/{jan,feb,march}/report" -> ["/2022/feb/report","/2022/jan/report","/2022/march/report"]
         "over{crowd,eager,bold,fond}ness" -> overboldness, overcrowdness, overeagerness, overfondness
         "read.txt{,.bak}" -> ["read.txt", "read.txt.bak"]
         echo_malformed=True: "sun{mars}rotation", "minimum{}change", "hello-world", "hello-{-world",
         "hello-}-weird-{-world" -> [input unchanged]
Part 3   "{a,b}{c,{d,e}}" -> ["ac","ad","ae","bc","bd","be"]
         "{{a,z},a{b,c},{ab,z}}" -> ["a","ab","ac","z"]
Part 4   "{a,b}c{d,e}f" -> count 4 ; k=1 "acdf", k=4 "bcef", k=5 None
         "{a,b,c}{a,b,c}{a,b,c}" -> 27 ; k=14 -> "bbb"
```
stdin `PART 1` / `{a,b}c{d,e}f` → `acdf` `acef` `bcdf` `bcef` (one per line).

## 关联知识点

- [[a04-string-expansion-backtracking|A04 栈 / 回溯做字符串展开]]
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s14-string-normalization|S14 字符串归一化 / 规范化]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
