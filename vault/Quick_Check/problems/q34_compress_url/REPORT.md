# q34 Compress URL — report

## Summary
Phone-screen string problem: replace every word of a URL with its numeronym (`stripe` → `s4e`) so
that logs stay analyzable but private and small. Part 2 adds a per-segment cap that folds the tail
of a path segment into one numeronym (dots counted). Parts 3–4 (reconstructed follow-ups) add a
minimum-length threshold and a collision report, the natural "is this lossy?" question.

## Sources & confidence
medium-high — one source with a verbatim prompt and driver calls (joeytor/StripeInterview
`Compress.java`, README → Phone Interview). Expected outputs were derived by tracing the Java.

## Approach by part
1. `split('/')` → `split('.')` → `w[0] + str(len(w)-2) + w[-1]`, re-join.
2. if a major part has **> m** minor parts: first `m-1` numeronyms, then `numeronym('.'.join(rest))`
   (the joined tail counts its dots: `write.a.java.program.in.one.day` → `w29y`). `== m` untouched.
3. `numeronym(w, min_len)`: `len(w) < min_len` → unchanged (`==` compresses). Default 0 = no
   threshold, which reproduces the Java for short words (`to` → `t0o`, `a` → `a-1a`).
4. `dict[compressed] -> set[original]`; report `len(set) >= 2`, sorted by compressed string.

## Pitfalls hidden tests target
- folding at `> m` not `>= m`; `m = 1` folds the whole major part (dots counted: `customer.maria` → `c12a`)
- 3-letter word → `x1x`; threshold boundary `==` compresses
- Part 4: exact duplicates counted once; deterministic sort
- no threshold by default: `to` → `t0o` (the assumption "≥ 3 letters" is violated by the source's own m=3 example)

## Complexity & measured cost
O(total characters). Measured: 0.34s, 83 MB (100k URLs, Part 4; budget 2 s / 256 MB).

## Test inventory
17 tests — part1: 5 · part2: 5 (incl. 1 io) · part3: 3 · part4: 4 (incl. 1 perf); edge 7 · fmt 1.

## Skills exercised
S02 parsing · S09 exact formatting · S14 string canonicalization · S19 incremental design · S20 self-testing
