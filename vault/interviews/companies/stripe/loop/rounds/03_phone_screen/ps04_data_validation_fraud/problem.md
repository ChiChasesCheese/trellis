# ps04 · Transaction Data Validation / Fraud Report — range + blocklist + behavior match + priority report

**Type:** technical phone screen ("Team Screen") · **Stage:** 60 min (45 coding + 15 Q&A), 4 parts · **Last asked:** 2025-11-30 (programhelp, cross-posted to LeetCode Discuss)
**Frequency:** LeetCode Discuss report (programhelp write-up, 2025-11-30); interviewdb.io lists "Data Validation" (2 weeks old) and "Fraud Reports" (1 month old) as separately-tracked, still-active listings as of 2026-07 · **Confidence:** high for the four-part shape and each part's one-line rule summary (all four are named explicitly in the source); the exact input protocol, priority order beyond "up to two codes", and worked numbers are this repo's reconstruction — see Sources.

## Context
Stripe Radar screens transactions in stages: is the record even complete, does it violate a hard
business rule (amount range, blocked payment method), does it look like the user's own history,
and — if several things are wrong at once — which two matter most to print. This is deliberately
**not** `problems/q15_kyc_verification` (KYC: onboarding CSV, statement-descriptor rules, quoted
commas, reconstructed circular-dependency checks). ps04 is post-onboarding **fraud triage**: a
numeric range check, a blocklist, and a 3-attribute match against a per-user behavioral profile —
no CSV quoting, no descriptor rules.

## Input (stdin)
First line `PART n` (n ∈ 1..4). Then four sections, in this fixed order, headers on their own
line; blank lines are ignored everywhere. All four sections are always present (their content may
be irrelevant to an earlier part — parse them anyway; this keeps the protocol identical across
parts, only the *evaluated* rules change).
```
RULES
min_amount,max_amount                                    decimal dollars, inclusive bounds
BLOCKLIST
method1,method2,...                                      may be an empty line (no blocked methods)
PROFILES
user_id,countries,hour_min,hour_max,amount_min,amount_max
                                                           countries is ';'-joined (e.g. US;CA);
                                                           hour_min/hour_max integers 0-23 inclusive;
                                                           amount_min/amount_max decimal dollars
TRANSACTIONS
txn_id,user_id,amount,currency,payment_method,country,timestamp
                                                           header row always present, always skipped;
                                                           timestamp is ISO-8601 'YYYY-MM-DDTHH:MM:SS'
```
Fields are split on `,` (no quoting — none of these fields contain embedded commas); every value
is trimmed. A transaction row with fewer than 7 columns has its missing trailing columns treated
as empty strings; extra columns are ignored. Up to 10^5 transaction rows.

## Output
API: `partN(lines: list[str]) -> list[str]`, one output line per transaction, **in input order**.
Parts 1–3: `txn_id: CODE1,CODE2,... ` or `txn_id: OK`. Part 4: a column-aligned report (see below).

## Rules (cumulative — Part n evaluates categories 1..n; every active category is checked
independently, so a row can trigger several codes)
### Part 1 — completeness → `MISSING_FIELD`
Any of the 7 fields (`txn_id,user_id,amount,currency,payment_method,country,timestamp`) empty
after trimming (including a missing trailing column) → `MISSING_FIELD`.

### Part 2 — range + blocklist → `AMOUNT_OUT_OF_RANGE`, `BLOCKED_METHOD`
`amount` must parse as a number **and** lie in `[min_amount, max_amount]` **inclusive**, from the
`RULES` section (a missing/empty amount is not additionally flagged here — `MISSING_FIELD`
already covers it). `payment_method` (case-insensitive, trimmed) must not be in `BLOCKLIST`.
Violating either fires the matching code; both can fire on the same row.

### Part 3 — behavioral match → `SUSPICIOUS`
Compare the transaction against its user's `PROFILES` row on **3 attributes**: `country` in the
profile's country set; the timestamp's hour-of-day in `[hour_min, hour_max]`; `amount` in
`[amount_min, amount_max]` (the *profile's* range — independent of Part 2's global `RULES`
range). Count how many of the 3 attributes match. **Fewer than 2 matches (i.e. 0 or 1 — "at least
50%" rounds to "at least 2 of 3") → `SUSPICIOUS`.** A user with **no profile row** is never
flagged suspicious (nothing to compare against — this rule is simply skipped for that user).

### Part 4 — priority report
Same rule set as Part 3, but the output is a report: at most the **top 2** codes by priority
(dropping the rest), formatted as one aligned block. Priority, highest first:
`MISSING_FIELD > BLOCKED_METHOD > AMOUNT_OUT_OF_RANGE > SUSPICIOUS`. Each line is
`txn_id` **left-justified to the width of the longest `txn_id` in this run**, then exactly **two
spaces**, then the (≤2) codes joined by `,`, or `OK` if none fired.

## Worked examples
Shared setup for every example below:
```
RULES
10.00,5000.00
BLOCKLIST
prepaid_card,gift_card
PROFILES
u1,US;CA,8,20,10.00,500.00
u2,GB,0,23,5.00,10000.00
TRANSACTIONS
txn_id,user_id,amount,currency,payment_method,country,timestamp
t1,u1,150.00,USD,credit_card,US,2026-08-01T14:30:00
t2,u1,150.00,USD,prepaid_card,US,2026-08-01T14:30:00
t3,u1,6000.00,USD,credit_card,US,2026-08-01T14:30:00
t4,u1,150.00,USD,credit_card,,2026-08-01T14:30:00
t5,u1,150.00,,credit_card,FR,2026-08-01T03:00:00
t6,u3,150.00,USD,credit_card,US,2026-08-01T14:30:00
t7,u1,9000.00,USD,gift_card,DE,2026-08-01T02:00:00
,u1,150.00,USD,credit_card,US,2026-08-01T14:30:00
```
`PART 1` →
```
t1: OK
t2: OK
t3: OK
t4: MISSING_FIELD          (country empty)
t5: MISSING_FIELD          (currency empty)
t6: OK
t7: OK
: MISSING_FIELD            (txn_id itself empty -- displayed as the empty string)
```
`PART 2` (adds range + blocklist) →
```
t1: OK
t2: BLOCKED_METHOD                       (prepaid_card is blocked)
t3: AMOUNT_OUT_OF_RANGE                  (6000.00 > 5000.00)
t4: MISSING_FIELD
t5: MISSING_FIELD
t6: OK
t7: BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE   (gift_card blocked AND 9000.00 > 5000.00)
: MISSING_FIELD
```
`PART 3` (adds behavior match; u1's profile: country in {US,CA}, hour 8-20, amount 10.00-500.00) →
```
t1: OK                                                  (country US, hour 14, amount 150 -- 3/3 match)
t2: BLOCKED_METHOD                                      (same 3/3 match, so not suspicious)
t3: AMOUNT_OUT_OF_RANGE                                 (country+hour match, amount 6000 doesn't -- 2/3, still OK)
t4: MISSING_FIELD                                       (country '' doesn't match, hour+amount do -- 2/3, still OK)
t5: MISSING_FIELD,SUSPICIOUS                            (country FR no, hour 3 no, amount 150 yes -- 1/3 < 2)
t6: OK                                                  (u3 has no profile -- SUSPICIOUS never evaluated)
t7: BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE,SUSPICIOUS       (country DE no, hour 2 no, amount 9000 no -- 0/3)
: MISSING_FIELD
```
`PART 4` (top-2 by priority, column-aligned; longest txn_id here is `t1`..`t7`, width 2) →
```
t1  OK
t2  BLOCKED_METHOD
t3  AMOUNT_OUT_OF_RANGE
t4  MISSING_FIELD
t5  MISSING_FIELD,SUSPICIOUS
t6  OK
t7  BLOCKED_METHOD,AMOUNT_OUT_OF_RANGE
    MISSING_FIELD
```
(`t7`'s 3rd code, `SUSPICIOUS`, is dropped by the top-2 rule. The empty-`txn_id` row's id column is
2 blank spaces — the padding width — followed by the mandatory 2-space separator, so 4 spaces
before `MISSING_FIELD`.)

## Edge cases hidden tests are known to target
- a value that is only whitespace is empty after trimming (`"  "` → `MISSING_FIELD`)
- amount exactly at `min_amount` / `max_amount` (inclusive boundary, both ends) → not out of range
- a fewer-than-7-column row (missing trailing columns) → those columns are empty → `MISSING_FIELD`
- `BLOCKLIST` comparison is case-insensitive (`Prepaid_Card` blocked if `prepaid_card` is listed);
  an empty `BLOCKLIST` line blocks nothing
- exactly 2 of 3 behavioral attributes matching is **not** suspicious (the ">= 2" boundary, not "> 2")
- exactly 1 of 3 matching **is** suspicious; 0 of 3 is suspicious
- a user with no `PROFILES` row is never `SUSPICIOUS`, regardless of how anomalous the transaction
  looks — there is nothing to compare against
- a row with 3+ triggered codes: Parts 1–3 print all of them (priority order); Part 4 keeps only
  the top 2 and drops the rest, never re-ordered
- an all-passing row prints `OK`, not an empty code list or an empty string
- `PART n` truly gates evaluation: a `BLOCKED_METHOD`/`AMOUNT_OUT_OF_RANGE`/`SUSPICIOUS` violation
  is invisible (row prints `OK`) under `PART 1`
- txn_id itself empty (still triggers `MISSING_FIELD`; displayed as the empty string, and as pure
  padding in Part 4's aligned column — see worked example)
- Part 4 column width is recomputed per run from the widest `txn_id` actually present, not a fixed
  constant
- amount that fails to parse as a number (non-numeric, non-empty) is out of documented scope and
  is not exercised by hidden tests (the field is either empty, or a valid decimal)
- up to 10^5 transaction rows, up to 10^5 profiles — must not be quadratic (dict lookups, not scans)

## Variants seen in the wild
- The source's Part 2 says "amounts must be within a business-defined range" and "payment methods
  not on a blocked list" without specifying whether both live in one rule block or two; this
  version keeps them in separate `RULES` / `BLOCKLIST` sections for parseability.
- "At least 50% of the behavioral attributes match" (source's own wording) is implemented here as
  literally `>= 2` of 3, i.e. round-up-to-majority, not a fractional threshold — with exactly 3
  attributes there is no ambiguity (2/3 = 66.7% >= 50%, 1/3 = 33.3% < 50%), but this repo makes
  the integer threshold explicit rather than re-deriving it from a percentage every call.
- The source does not specify the number of output codes kept in Part 4 beyond "up to two" and
  does not name a tie-break priority; this repo fixes both
  (`MISSING_FIELD > BLOCKED_METHOD > AMOUNT_OUT_OF_RANGE > SUSPICIOUS`) since a phone-screen
  rubric needs one.

## What this tests
skills: S02 parsing (sectioned stdin) · S05 inclusive range checks · S06 `Decimal` money, never
float · S08 deterministic ordering (input order preserved throughout) · S09 exact formatting
(column alignment) · S18 validation & prioritized error paths · S19 incremental rules (Part n
evaluates categories 1..n) · S24 domain (Radar-style fraud triage, distinct from q15's KYC domain)

## Sources
- https://leetcode.com/discuss/post/7384225/stripe-phone-screen-4-part-interview-exp-dhoy/ (programhelp write-up, 2025-11-30: "Part 1: read a CSV of 6 fields [sic — this repo uses 7, see Clarifications], validate all fields are non-empty. Part 2: amount must be within a business-defined range, payment method must not be on a blocked list, else mark suspicious. Part 3: compare against historical behavior (spending countries, time range, amount range) — at least 50% of the behavioral attributes must match, else SUSPICIOUS. Part 4: output an error report with up to two error codes per transaction, prioritized, maintaining column alignment for readability.")
- https://www.interviewdb.io/question/stripe ("Data Validation" — 2 weeks old; "Fraud Reports" — 1 month old, as scraped 2026-07)
- `loop/raw/en_forums.md` §3.3 P6 "交易风控四段题（Data Validation / Fraud Reports）" (this repo's own collation of the above)

## Clarifications (author's own, not sourced)
- The source says "6 fields" for the completeness check but the domain description (amount,
  currency, payment method, country, timestamp for behavior matching) needs 7 named columns
  (`txn_id,user_id,amount,currency,payment_method,country,timestamp`) to make Parts 2–4 well
  defined; this repo uses 7 and treats "6" as the source's own paraphrase (it is a secondhand
  write-up, not a verbatim problem statement).
- "Marked suspicious" for Part 2 in the source's paraphrase is superseded by the more specific
  `AMOUNT_OUT_OF_RANGE` / `BLOCKED_METHOD` codes once Part 4's "error codes, prioritized" language
  makes clear multiple distinct codes exist by Part 4 — `SUSPICIOUS` is reserved for Part 3's
  behavioral-match failure specifically, per the source's own Part 3 wording.
- Exact section names (`RULES`/`BLOCKLIST`/`PROFILES`/`TRANSACTIONS`), the profile schema, and the
  priority order are this repo's reconstruction (no verbatim I/O sample is available), modelled on
  this suite's own `problems/q02_merchant_fraud_score` sectioned-stdin convention.
