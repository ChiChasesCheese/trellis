# q15 · KYC Business Verification — progressive CSV validation of merchant onboarding data

**Type:** bespoke OA / tech screen ("five incremental steps") · **Stage:** HackerRank OA or 45-min team screen · **Last asked:** 2026-06-30 (1point3acres 题库); Glassdoor "6 step KYC Verification coding Q"; InterviewDB "Data Validation — Phone" (Aug 2026)
**Frequency:** 6 independent sources (1point3acres 题库 ×2 entries, 1point3acres 1154573/1155516 team-screen summaries, Glassdoor QTN_8763050, Exponent, InterviewDB, darkinterview) · **Confidence:** high for Parts 1–3 (three sources agree on the rules), Parts 4–5 reconstructed (titles only; rules modelled on Stripe's statement-descriptor and website requirements)

## Context
Before a business can accept payments, Stripe verifies its onboarding data (KYC — "know your
customer"). A record is only `VERIFIED` when every check passes: fields present, statement
descriptors (what appears on the cardholder's bank statement) well-formed and not generic,
and a real website. The checks arrive as incremental parts; each part adds a rule.

## Input (stdin)
Optional first line `PART n` (1–5, default 5 = all rules) optionally followed by the token
`REASONS`. Then CSV rows, parsed with the `csv` module (**quoted fields may contain commas**),
columns in this fixed order:
```
business_name,business_profile_name,full_statement_descriptor,short_statement_descriptor,url,product_description
```
A header row (first cell equal to `business_name`, case-insensitive) is skipped. Blank lines
are skipped. Missing trailing columns count as empty; extra columns are ignored. Every value is
trimmed before checking. Up to 10^5 rows.

## Output
One line per row, in input order:
`VERIFIED: <business_name>` or `NOT VERIFIED: <business_name>` (name as given, trimmed).
With `REASONS`, failing rows print the reason codes in the fixed order below:
`NOT VERIFIED: Acme (EMPTY_FIELD, DESCRIPTOR_LENGTH)`.

API: `verify(rows: list[str], part: int = 5, reasons: bool = False) -> list[str]`;
`check_row(fields: list[str], part: int = 5) -> list[str]` returns the reason codes (empty = verified).

## Rules (cumulative — Part n applies rules 1..n; every rule is evaluated, so a row can have several codes)
### Part 1 — completeness → `EMPTY_FIELD`
All six fields must be present and non-empty after trimming.

### Part 2 — full descriptor length → `DESCRIPTOR_LENGTH`
`len(full_statement_descriptor)` must be **5–31 inclusive** (Stripe's real limit is 22, the OA
uses 5–31). Length is counted after trimming, in characters. An empty descriptor fails both
rule 1 and rule 2.

### Part 3 — generic descriptors → `DESCRIPTOR_BLACKLISTED`
The full descriptor must not equal (case-insensitive, trimmed, inner whitespace collapsed) any
of: `ONLINE STORE`, `ECOMMERCE`, `RETAIL`, `SHOP`, `GENERAL MERCHANDISE`.
`"online store"`, `" Shop "`, `"General   Merchandise"` are blacklisted; `"SHOP ACME"` is not.

### Part 4 — short descriptor & name consistency (reconstructed) → `SHORT_DESCRIPTOR`, `NAME_MISMATCH`
* `SHORT_DESCRIPTOR`: the short descriptor must be **2–10 characters** and its **first word**
  (whitespace-delimited, case-insensitive) must equal the first word of the full descriptor.
* `NAME_MISMATCH`: the full descriptor must contain the business name **or** the business
  profile name (case-insensitive substring; empty names never match).

### Part 5 — website (reconstructed) → `INVALID_URL`
`url` must start with `http://` or `https://` (scheme case-insensitive) and its host (up to
the next `/`, `?` or `#`) must contain a dot, contain no whitespace, and not start or end
with a dot. `https://acme.com`, `HTTP://shop.acme.io/path?x=1` pass; `acme.com`,
`ftp://acme.com`, `https://localhost`, `https://.com`, `https://acme com` fail.

Reason-code order: `EMPTY_FIELD, DESCRIPTOR_LENGTH, DESCRIPTOR_BLACKLISTED, SHORT_DESCRIPTOR, NAME_MISMATCH, INVALID_URL`.

## Worked examples
Example 1 (Parts 1–3, the sourced rules):
```
PART 3
business_name,business_profile_name,full_statement_descriptor,short_statement_descriptor,url,product_description
Acme Inc,Acme,ACME INC STORE,ACME,https://acme.com,Widgets      -> VERIFIED: Acme Inc
Bolt,Bolt Shop,,BOLT,https://bolt.io,Chargers                    -> NOT VERIFIED: Bolt      (empty full descriptor)
Cafe Rio,Cafe Rio,CAFE,CAFE,https://caferio.com,Coffee           -> NOT VERIFIED: Cafe Rio  (length 4 < 5)
Dot LLC,Dot,online store,DOT,https://dot.co,Things               -> NOT VERIFIED: Dot LLC   (blacklisted, case-insensitive)
"Ed, Inc","Ed",ED INC PAYMENTS,ED INC,https://ed.com,"Books, toys" -> VERIFIED: Ed, Inc     (quoted commas)
```
Example 2 (all five parts with reasons):
```
PART 5 REASONS
Acme Inc,Acme,ACME INC STORE,ACME,https://acme.com,Widgets    -> VERIFIED: Acme Inc
Zed,Zed,ZED STORE,STORE,zed.com,Stuff                         -> NOT VERIFIED: Zed (SHORT_DESCRIPTOR, INVALID_URL)
Foo,Bar,BAZ SERVICES,BAZ,https://baz.io,Svc                   -> NOT VERIFIED: Foo (NAME_MISMATCH)
,,SHOP,S,https://x,                                           -> NOT VERIFIED:  (EMPTY_FIELD, DESCRIPTOR_LENGTH, DESCRIPTOR_BLACKLISTED, SHORT_DESCRIPTOR, NAME_MISMATCH, INVALID_URL)
```
(Row 2: `STORE` ≠ first word `ZED`; row 4: every rule fails — note the empty name after `NOT VERIFIED: `.)

Example 3 (Part 1 only — later rules are not applied):
```
PART 1
Dot LLC,Dot,online store,DOT,https://dot.co,Things   -> VERIFIED: Dot LLC
Dot LLC,Dot,online store,DOT,,Things                 -> NOT VERIFIED: Dot LLC
```

## Edge cases hidden tests are known to target
- whitespace-only field is empty (`"  "`); values are trimmed before every check
- descriptor length boundaries: 4 / 5 / 31 / 32 characters; length counted after trimming
- blacklist is case-insensitive and whole-string (`SHOP ACME` passes, `shop` fails,
  `General  Merchandise` with doubled space fails)
- quoted CSV fields with commas and quotes (`"Ed, Inc"`, `"Say ""hi"""`); a header row
- rows with fewer than 6 columns → missing fields are empty → `EMPTY_FIELD`
- several rules failing at once print all codes in the fixed order, once each
- `PART n` limits the rules: a blacklisted descriptor is `VERIFIED` under `PART 2`
- short descriptor boundaries 1 / 2 / 10 / 11 characters; first-word comparison is
  case-insensitive (`acme` vs `ACME INC`)
- URL: scheme case-insensitive; `https://` with empty host fails; host with port
  (`https://acme.com:8443`) passes; trailing path/query ignored

## Variants seen in the wild
- **Six steps** (Glassdoor): an extra "cross-column" step; Exponent mentions detecting
  **circular dependencies** between fields — not reproduced here (no rule text available).
- Output only the verified names / only the failed names (team-screen summaries) — trivial
  filter on the returned lines.
- Reason codes are this repo's extension (the sources print only `VERIFIED`/`NOT VERIFIED`);
  keep `reasons=False` for the sourced format.

## What this tests
skills: S02 CSV parsing (quoted commas) · S05 inclusive thresholds · S09 exact output ·
S14 normalisation (case, whitespace) · S18 validation & error paths · S19 incremental rules ·
S21 stdlib `csv` · S24 domain (statement descriptors, KYC)

## Sources
- 1point3acres 题库 `kyc-business-verification` (OA / Tech screen · Medium · last asked 2026-06-30 · "five incremental steps")
- 1point3acres 题库 `problems/c2c4e3e9-…` 「KYC Conundrum」 (3 parts visible)
- 1point3acres 1154573 / 1155516 team-screen summaries ("Data Verification", "KYC CSV 30+ 行 6 列")
- Glassdoor QTN_8763050 "6 step KYC Verification coding Q"
- Exponent "CSV parsing & validation… circular dependencies"; InterviewDB "Data Validation — Phone"; darkinterview "Data Verification"
