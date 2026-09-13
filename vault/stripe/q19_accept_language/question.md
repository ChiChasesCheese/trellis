# q19 · Accept-Language — resolve a request's language preferences against supported tags

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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s14-string-normalization|S14 字符串归一化 / 规范化]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s20-self-test-discipline|S20 自测纪律]]
