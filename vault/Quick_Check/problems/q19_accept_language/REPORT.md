# q19 Accept-Language — report

## Summary
Resolve an `Accept-Language` header against the server's supported tags: exact tags, then
language-only tags (`fr` → all `fr-*`), then the `*` wildcard, then `;q=` weights. A classic
Stripe phone screen (verbatim statement in a public repo) that also shows up as an OA. The
grading is all about ordering and deduplication: header order vs supported order, no repeats
when `fr-FR, fr` overlap, wildcard = "everything not already covered", q ties by position.

## Sources & confidence
high — joeytor/StripeInterview verbatim statement with examples for Parts 1–3, LeetCode
4742657 (Part 1 verbatim), adonais0 blog, Glassdoor, 1point3acres 题库 (last asked 2025-10-22),
programhelp (q-value examples), Blind. Conflict resolved: programhelp's example sinks q=0 tags
to the end; RFC 7231 (and the user brief) treat q=0 as "not acceptable". Primary = exclude,
variant `zero_q="last"` reproduces programhelp's expected outputs and is tested.

## Approach by part
One function, one model: parse entries `(tag, q, position)` (lowercase, trimmed, `;q=` with
default 1.0, bad q → 1.0). For every supported tag pick the **most specific** matching entry
(exact 2 > language-only 1 > `*` 0; ties by header position) — that entry's q and position
label the tag. Sort by `(-q, position, supported index)`; drop q=0 (or append last).
1. exact tags → position order; 2. language-only expansion in supported order; 3. `*` covers
tags with no explicit entry; 4. q-sorting. Output uses the supported list's spelling.

## Pitfalls hidden tests target
- `fr-FR, fr` repeating fr-FR; `fr, fr-FR` ordering (fr-CA first — both q=1, `fr` is earlier)
- `*` re-adding a tag explicitly listed later (`*, en-US` → French first, en-US last)
- `fr-CA;q=0, fr;q=0.5`: the exact q=0 entry must win over the language expansion
- case-insensitive matching but output in supported spelling; duplicated supported entries
- default q = 1.0 beats `q=0.9`; `0.50 == 0.5`; `;level=1` parameter ignored; `Q=` uppercase

## Complexity & measured cost
O(S · E) tag/entry matching (S supported, E entries) + O(S log S).
Measured: 0.23s, 19 MB (10k entries × 1k supported; budget 2 s / 256 MB).

## Test inventory
20 tests — part1: 6 (incl. 1 io) · part2: 3 · part3: 4 (incl. 1 io) · part4: 7 (incl. 1 perf, 1 variant);
edge 10 · fmt 1.

## Skills exercised
S02 parsing · S08 deterministic order · S14 normalisation · S18 validation · S19 incremental · S20 self-testing
