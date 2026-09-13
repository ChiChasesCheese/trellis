# q15 KYC Business Verification — report

## Summary
Progressive CSV validation of merchant onboarding rows: completeness, statement-descriptor
length, generic-descriptor blacklist, then (reconstructed) short-descriptor/name consistency
and website checks. It mirrors Stripe's KYC / statement-descriptor requirements and is asked
as a "five incremental steps" OA or a 45-minute team screen. The traps are CSV quoting,
trimming before every check, inclusive boundaries, whole-string case-insensitive blacklist,
and reporting every failing rule in a fixed order.

## Sources & confidence
high for Parts 1–3 — 1point3acres 题库 ×2 (last asked 2026-06-30), 1point3acres team-screen
summaries, Glassdoor QTN_8763050, InterviewDB, darkinterview all agree on fields, `5–31`, and
the five blacklisted descriptors. Parts 4–5 are **reconstructed** (sources only say "five/six
steps"; rules follow Stripe's public descriptor/website requirements) and are marked so in
problem.md. Reason codes are a repo extension (`reasons=True`); the sourced output is plain
`VERIFIED: name` / `NOT VERIFIED: name`.

## Approach by part
`parse_rows` uses `csv.reader` (quoted commas / doubled quotes), skips blanks and a header row,
trims and pads to six columns. `check_row(fields, part)` evaluates rules 1..part independently
and returns codes in `CODES` order; `verify` renders lines.
1. any empty (post-trim) field → `EMPTY_FIELD`
2. `5 ≤ len(full) ≤ 31` inclusive → `DESCRIPTOR_LENGTH`
3. `" ".join(full.split()).upper() in BLACKLIST` (whole string) → `DESCRIPTOR_BLACKLISTED`
4. short `2–10` chars and same first word as full → `SHORT_DESCRIPTOR`; full contains business
   or profile name case-insensitively → `NAME_MISMATCH`
5. `http(s)://` + host (before `/?#`) containing a dot, no leading/trailing dot, no whitespace → `INVALID_URL`

## Pitfalls hidden tests target
- whitespace-only fields; trimming before length check (`"   ACME   "` is 4 chars)
- boundaries 4/5/31/32 and 1/2/10/11; `SHOP ACME` is not blacklisted, `shop` is
- quoted business names with commas must round-trip into the output line
- rows with < 6 columns; header row; `PART n` gating (blacklisted row is VERIFIED under PART 2)
- multiple codes at once, fixed order, each once; empty name prints `NOT VERIFIED: `

## Complexity & measured cost
O(total characters). Measured: 0.27s, 103 MB (100k rows with reasons; budget 2 s / 256 MB).

## Test inventory
17 tests — part1: 4 · part2: 3 · part3: 3 (incl. 1 io) · part4: 2 · part5: 5 (incl. 1 io, 1 perf);
edge 10 · fmt 1.

## Skills exercised
S02 CSV parsing · S05 inclusive thresholds · S09 exact output · S14 normalisation · S18 validation · S19 incremental rules · S21 stdlib csv · S24 KYC/descriptor domain
