# q19 · Accept-Language — resolve a request's language preferences against supported tags

**Type:** bespoke phone screen (4 parts, also reported as OA) · **Stage:** phone screen / tech screen (45–60 min, "use tests to demonstrate correctness") · **Last asked:** 2025-10-22 (1point3acres); 2025-09 (programhelp OA write-up); LeetCode 2024-02-17
**Frequency:** 7 independent sources (joeytor/StripeInterview verbatim statement, LeetCode 4742657, adonais0 blog 2021, Glassdoor QTN_4469893, programhelp 2025, 1point3acres 题库, Blind 2022) · **Confidence:** high (Parts 1–3 verbatim; Part 4 q-values medium-high)

## Context
Stripe's Dashboard and hosted pages are localised. A browser sends
`Accept-Language: en-US, fr-CA, fr-FR` — a comma-separated list of language tags in descending
order of preference. The server supports only some languages and must return the list of
supported tags that satisfy the request, most preferred first.

## Input (stdin)
Line 1: the header value (may be empty). Line 2: comma-separated supported tags, in the
server's preference order. Rules accumulate — one program handles every part (no `PART n`).
Tags are `language[-REGION]`, compared **case-insensitively**; whitespace around tags and `;`
parameters is ignored. Up to 10^4 header entries × 10^3 supported tags.

## Output
Matching tags, **one per line, spelled as in the supported list**, most preferred first;
`NONE` if nothing matches.

API: `parse_accept_language(header: str, supported: list[str]) -> list[str]`.

## Rules
### Part 1 — exact tags
Return the supported tags that appear in the header, in **header order**. A tag mentioned
twice is emitted once (first position wins).

### Part 2 — language-only tags
A tag without a region (`en`) means "any variant of English": it expands to **every supported
tag whose language part is `en`, in supported-list order** (`en-US`, `en-GB`, and a bare
`en` if the server lists one). Tags already emitted are not repeated (`"fr-FR, fr"` →
`fr-FR, fr-CA`, not `fr-FR, fr-CA, fr-FR`). Unsupported languages expand to nothing.

### Part 3 — wildcard
`*` means "all other languages": every supported tag **not covered by any explicit entry of
the header** (exact or language-only), in supported-list order. A second `*` adds nothing.

### Part 4 — quality values
Entries may carry `;q=<0..1>` (default `1.0`; other parameters such as `;level=1` are
ignored; an unparsable q counts as `1.0`). For every supported tag the **most specific**
matching entry decides its q — exact tag > language-only tag > `*`, ties by header position
(so `fr-CA;q=0, fr;q=0.5` gives fr-CA q=0, not 0.5). Output is ordered by **q descending,
ties by header position of the deciding entry, then supported order**. `q=0` means "not
acceptable": the tag is dropped, and `*` / a language-only tag never re-adds it.
(Variant: sink q=0 tags to the end instead — see Variants.)

## Worked examples
Part 1 (verbatim):
```
parse_accept_language("en-US, fr-CA, fr-FR", ["fr-FR", "en-US"])  -> ["en-US", "fr-FR"]
parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"])         -> ["fr-FR"]
parse_accept_language("en-US", ["en-US", "fr-CA"])                -> ["en-US"]
```
Part 2 (verbatim):
```
parse_accept_language("en", ["en-US", "fr-CA", "fr-FR"])        -> ["en-US"]
parse_accept_language("fr", ["en-US", "fr-CA", "fr-FR"])        -> ["fr-CA", "fr-FR"]
parse_accept_language("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"]) -> ["fr-FR", "fr-CA"]
```
Part 3 (verbatim):
```
parse_accept_language("en-US, *", ["en-US", "fr-CA", "fr-FR"])     -> ["en-US", "fr-CA", "fr-FR"]
parse_accept_language("fr-FR, fr, *", ["en-US", "fr-CA", "fr-FR"]) -> ["fr-FR", "fr-CA", "en-US"]
```
Part 4:
```
parse_accept_language("en-US,en;q=0.8,fr;q=0.9,de;q=0.7", ["en-US","en-GB","fr","de"])
    -> ["en-US", "fr", "en-GB", "de"]                      (programhelp: en-US 1.0, fr .9, en .8, de .7)
parse_accept_language("fr-FR;q=1, fr-CA;q=0, *;q=0.5", ["fr-FR","fr-CA","fr-BG","en-US"])
    -> ["fr-FR", "fr-BG", "en-US"]                          (fr-CA claimed by q=0, so * skips it)
    -> ["fr-FR", "fr-BG", "en-US", "fr-CA"]  with zero_q="last"   (programhelp's expected output)
```
stdin form of the first Part 1 example: `en-US, fr-CA, fr-FR` ⏎ `fr-FR,en-US` → `en-US` ⏎ `fr-FR`.

## Edge cases hidden tests are known to target
- empty header, header of only whitespace/commas, empty supported list → `[]` / `NONE`
- case: header `EN-us` matches supported `en-US` and is printed as `en-US`; supported list may
  itself be mixed-case (`en-us`) — output uses the supported spelling
- whitespace: `" en-US ,fr ; q=0.5 "`
- duplicates in the header and in the supported list → emitted once
- `fr-FR, fr` must not repeat `fr-FR`; `fr, fr-FR` → `fr-CA, fr-FR` (fr-FR already emitted by `fr`)
- `*` alone → the whole supported list in supported order; `en, *` → English first, then the rest
- q ties keep header order; q values like `0.80` vs `0.8` are equal; `q=1.0` is the default
- `q=0` excludes (primary) and still blocks `*` from re-adding the tag
- language-only tag that is itself in the supported list (`en` in `["en", "en-US"]`) → both

## Variants seen in the wild
- **q=0 sinks to the end** (programhelp): `parse_accept_language(header, supported, zero_q="last")`
  appends q=0 matches after everything else (header order among them). Primary is exclusion
  (RFC 7231 §5.3.5 "not acceptable").
- Return a set instead of an ordered list (adonais0 2021 write-up) — ordering was still asked as
  a follow-up.
- 1point3acres `http-language-preference`: "exact match → prefix match → …" phrasing, same 4 parts.

## What this tests
skills: S02 parsing · S08 deterministic order (q desc, header position) · S14 normalisation
(case, whitespace) · S18 validation (bad q) · S19 incremental design · S20 self-testing

## Sources
- https://github.com/joeytor/StripeInterview (`src/main/java/HttpHeaderParser.java`, README → Phone Interview; verbatim Parts 1–3)
- https://leetcode.com/discuss/interview-experience/4742657/ (2024-02-17, verbatim Part 1)
- https://adonais0.github.io/20210603/interview-stripe/ (phone, 2021-06)
- https://programhelp.net/en/vo/stripe-interview-process-explained-2025-edition/ (q-values, wildcard examples)
- Glassdoor QTN_4469893 "Parsing the HTTP Accept-Language header" (Infra Eng)
- 1point3acres 题库 `http-language-preference` (phone screen, last asked 2025-10-22, 4 Part)
- Blind Apr 2022 "parsing some list of http headers"; InterviewDB "Header Parsing — Phone"
