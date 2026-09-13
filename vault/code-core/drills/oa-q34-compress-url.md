---
nodes: [algorithms.strings, transfer.stripe-oa]
tags: [stripe-oa, q34]
---
# Drill: compress a URL into numeronyms, fold tails, then find collisions

Sixty minutes, stdin to stdout. A URL is split on `/` into major parts, each major part split on
`.` into minor parts; Part 1 replaces every minor part with its numeronym — first letter, count
of letters between, last letter (`internationalization` -> `i18n`) — and rejoins with the same
separators. Part 2 caps each major part at `m` minor parts: parts beyond the cap, dots included,
fold into a single numeronym spanning from the m-th minor part's first letter to the last minor
part's last letter. Part 3 adds a minimum-length threshold below which a part (or a folded tail)
is left uncompressed. Part 4 takes a whole log of URLs and reports which compressed forms are
produced by two or more distinct original URLs, since the compression is lossy.

**Constraints to state and honor**
- Part 1 input is lowercase letters plus `/` and `.` only, with no empty parts (no leading or
  trailing separator, no `..`, no `//`).
- The numeronym formula is exactly `w[0] + str(len(w) - 2) + w[-1]` — short words produce
  strange-but-correct results (`to` -> `t0o`, a single letter -> a negative middle count) unless a
  length threshold says otherwise.
- Folding triggers only when a major part has strictly more than `m` minor parts; a part with
  exactly `m` is left exactly as Part 1 would compress it.
- The folded tail counts every character between its first and last letter, dots included — it is
  not "the numeronym of the joined string minus dots," it's the numeronym of the literal
  dot-joined text.
- Part 4 counts exact duplicate URLs once, reports only compressed forms shared by 2+ distinct
  originals, and sorts by the compressed string.

**Grading points**
- One `numeronym(word, min_len=0)` helper reused everywhere — Part 1 baseline, Part 2's folded
  tail, and Part 3's threshold are all the same function with one added parameter, not three
  separate code paths.
- `m = 1` as the sharpest test of the folding rule: it folds an entire major part including its
  internal dots (`customer.maria` -> `c12a`, not `c6r.m3a`) — get this case right and the general
  rule is right.
- The threshold's boundary is `len == min_len` still compresses, `len < min_len` does not — and
  the same threshold applies to a Part 2 folded tail, not just to ordinary minor parts.
- Part 4 modeled as `compressed -> set(original_urls)`, reporting only entries with 2+ members —
  a plain counter would double-count a URL repeated in the log.
- A single word with no separators, and a URL that is one major part with many minor parts, both
  handled by the same split/join logic without special-casing.
- The whole pipeline runs in time proportional to total character count — no accidental
  quadratic re-scanning of a long path.

**Source**
- `vault/Quick_Check/problems/q34_compress_url/problem.md`, `vault/Quick_Check/problems/q34_compress_url/REPORT.md`, `vault/stripe/q34_compress_url/question.md`, `vault/stripe/q34_compress_url/solution.md`, `vault/Quick_Check/study/10-solutions/q34_compress_url.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
