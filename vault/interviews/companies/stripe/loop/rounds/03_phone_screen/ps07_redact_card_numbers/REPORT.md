# ps07 Redact card numbers from logs — report

## Summary
"Blur card numbers in logs" is interviewing.io's one-line phrasing of a real Stripe requirement:
log sinks must never persist a raw PAN. The problem is Luhn/network validation (q05) wearing a
different hat -- the interesting engineering is not the checksum, it's (a) finding card-shaped
spans inside arbitrary free text without a backtracking-prone regex, (b) masking in a way that
preserves the surrounding text and the number's own punctuation exactly, and (c) using the
Luhn+brand check as a false-positive filter rather than as the end goal. The four parts walk a
naive "any digit-shaped run" heuristic to a validated, streaming-safe redactor -- a shape Stripe
phone screens reuse constantly (see q03, q05, ps05: naive pass -> add a rule that fixes a
specific wrong answer -> generalize -> scale).

## Sources & confidence
medium -- interviewing.io lists "How would you blur credit card numbers from logs?" as a coding-
round sample question with no published transcript (`loop/raw/en_forums.md` section 6.2, C8);
staffengprep independently lists a "Valid Credit Card Number (Redaction)" prompt with the same
masking core (section 3.3, P13) but a different part-boundary convention (validate-then-mask,
not mask-then-filter). Every rule in this problem.md beyond "find and blur card numbers in
free-text logs" is this report's reconstruction -- see Open points in problem.md.

## Approach by part
1. **Bare digit runs**: one linear scan (`_scan_candidates`) finds maximal digit-only runs;
   length filter `[13, 19]`; mask all but the last 4 digits. No brand/Luhn check yet, so it
   over-redacts (worked example 1c, a 13-digit unix-ms timestamp).
2. **Separators**: the same scanner grows a candidate through a single `' '`/`'-'` between two
   digit groups (never two in a row, never leading/trailing). Masking replaces digit characters
   only, keeping every separator untouched, and counts the *last 4 digits*, not the last 4
   characters -- this matters for AMEX's 4-6-5 grouping (`3782-822463-10005` ->
   `****-******-*0005`, the last group is 5 characters but only its last 4 are digits kept).
   The naive space-joining also makes over-grouping worse, not better (a grouped phone number
   totalling 13 digits gets swept in, worked example 2c) -- Part 3 is the actual fix.
3. **Luhn + brand filter**: reuses q05's Luhn walk, but a wider brand table (adds Discover
   `6011`/`65` and Mastercard's `2221`-`2720` range, both absent from q05's three-network table)
   because this problem's job is "catch every real PAN network", not "the three networks q05
   already drilled". A candidate is redacted iff `brand_of(digits) is not None and luhn_ok(digits)`
   -- everything else (wrong prefix, wrong length, right shape but bad checksum) passes through
   byte-identical.
4. **Streaming**: identical detection logic, engineered to be a single pass per line with no
   quadratic string rebuilding (list-append + one final `"".join`, never `str += `) and no regex
   with nested quantifiers, so total cost is O(sum of line lengths). Appends `REDACTED n`.

## Pitfalls hidden tests target
- masking is format-preserving: separators, punctuation and everything outside a candidate span
  survive untouched; only digit characters inside a redacted span change
- last-4 is measured in *digits*, not characters, once separators are in play
- boundary lengths: 13/19 in, 12/20 out, and a >19-digit run is never partially masked (it isn't
  "the first 19 digits of a longer number", the whole thing is left alone)
- blank log lines must round-trip as blank lines, not be dropped -- this is log text, not a
  delimited record format like the other problems in this repo
- a doubled separator or a leading/trailing separator breaks the chain at that point, it does not
  get silently absorbed into a longer candidate
- known Luhn-valid look-alikes that must NOT be redacted even at Part 3/4: order/invoice numbers,
  Unix-ms timestamps (13 digits -- collides with the *minimum* PAN length), grouped international
  phone numbers (13+ digits when concatenated)
- the two networks q05 explicitly does not support (Discover; Mastercard's `2221`-`2720` range)
  must be recognized and redacted here -- `2223003122003222` is `UNKNOWN_NETWORK` in q05 but a
  real, redactable Mastercard in this problem
- `REDACTED n` counts spans actually masked post-filter, not raw Part 1/2-style candidates

## Complexity & measured cost
O(total input length): one pass per line to find spans (`_scan_candidates`), one pass to build
the masked output (`_mask_span` + list join), both bounded by the line's length; no re-scanning,
no `str +=` in a loop. Measured: 100,000 log lines (mix of real-PAN lines every 500th line,
timestamp look-alikes every 137th line, plain text otherwise), Part 4 end-to-end (stdin -> stdout)
in well under 2 s, comfortably under the 256 MB budget -- see `test_perf_100k_lines`.

## Test inventory
27 tests -- part1: 9 . part2: 6 . part3: 6 . part4: 6 (incl. 4 io, 1 perf); edge 12 . fmt 1 . io 4
. perf 1.

## Skills exercised
S02 parsing free text (not delimited records) . S09 exact, format-preserving output . S14 Luhn
digit walking reused for a new purpose . S18 false-positive/validation discipline . S19
incremental design (Part 1 subset of Part 2 subset of Part 3/4) . S21 stdlib fluency, no
backtracking regex

## Interview talk track: what to say while writing
1. **Reading the prompt**: say out loud that this is not q05 -- q05 asks "is this string a valid
   card number", this problem asks "does this log line contain one hidden inside free text, and
   if so how do I blur it". Nail down two contract questions before coding: does the mask keep
   the original separators, and how are non-card look-alikes (order numbers, timestamps, phone
   numbers) supposed to be handled? Getting these wrong derails Part 2/3.
2. **Writing Part 1**: build the "find 13-19 digit runs" scanner first and say explicitly "I'm
   deliberately not checking Luhn yet -- this will over-redact, and that's fine because Part 3 is
   where I fix it; splitting detection from validation keeps each layer single-responsibility."
   Surfacing the known flaw before being asked is worth more than looking flawless.
3. **Writing Part 2**: call out that "last 4" means digits, not characters -- the trap is AMEX's
   4-6-5 grouping where the final group is 5 characters. Also flag the tradeoff explicitly: "I'm
   not requiring a canonical group shape like 4-4-4-4, so this over-groups things like phone
   numbers; Part 3's Luhn+brand filter is what narrows it back down."
4. **Writing Part 3**: reuse the Luhn walk from Part 1 (mention "this is the same algorithm as a
   card-validation problem, just applied to a redaction pipeline instead") and lead with "prefix
   + length must match a real network before Luhn even runs" -- then prove it live with the
   timestamp and phone-number counterexamples.
5. **Writing Part 4**: narrate the complexity choice -- single pass with list-append + one final
   join, not per-line regex substitution or string `+=`, so total cost is O(input length). If
   asked about a chunked/streaming transport that could split a card number across two reads,
   admit the current API assumes reassembled lines and sketch (don't fully implement) a
   stateful scanner carrying an unresolved digit suffix between `process(chunk)` calls.
6. **Wrapping up**: walk through the worked examples by hand once more (especially the 2c/3a
   pair -- over-redact then fix), then offer to run the redactor read-only against a sample of
   real logs and diff before/after line lengths as a pre-deploy sanity check -- ties the solution
   back to the PCI-DSS motivation from the prompt.

## Open points
- The interviewing.io source is a single sentence with no published I/O contract, part count, or
  worked examples. This problem.md's Rules/Worked examples are a defensible reconstruction built
  from q05's already-verified Luhn/network code, the repo's recurring "naive -> filtered ->
  scaled" phone-screen template, and real PCI-DSS partial-PAN display conventions. If a verbatim
  transcript surfaces, reconcile part boundaries and the exact masking format against it.

## Review（2026-09-02）
复核通过，本轮未改动 `solution.py`/`starter.py`/`starter_template.py`/`test_ps07.py`（代码已在此前
review 中定型）。
- 快速核对：problem.md 的关键 worked examples（1a/4a 单卡+多卡打码、2c 电话号码过度分组、3a 时间戳/
  电话/订单号被 Part 3 放过、3b 五个品牌样例含 Mastercard `2221-2720`/Discover 新前缀及 Luhn 失败样例）
  已用 `solution.py` 逐字重跑核对 stdin → stdout，全部与文档一致。
- 回归：`rtk proxy python3 -m pytest loop/rounds/03_phone_screen/ps07_redact_card_numbers --tb=short`
  29 passed；`IMPL=starter` 同目录 20 failed / 9 passed（starter 的桩函数默认原样透传输入而非返回空，
  故"不该被打码的行"这类用例恰好也通过，符合设计，不构成空洞测试）。
- Lint：`loop/lint.sh loop/rounds/03_phone_screen/ps07_redact_card_numbers` 直接通过，无需 `--fix`
  （black 110 列 + flake8 F 类 0）。
- `starter.py`/`starter_template.py` 内容仍完全一致，公共 API 与 `solution.py` 一致。
- 遗留：无。problem.md 的 Open points（interviewing.io 源为单句无逐字 transcript）已如实标注，不影响
  代码正确性。
- 文章：`loop/study/30-articles/ps07_redact_card_numbers.md`（157 行）。
