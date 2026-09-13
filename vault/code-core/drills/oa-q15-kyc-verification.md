---
nodes: [input.malformed, input.normalization, transfer.stripe-oa]
tags: [stripe-oa, q15]
---
# Drill: verify merchant onboarding data against five accumulating KYC rules

Sixty minutes, stdin to stdout. Six-column CSV rows describe a business awaiting Stripe KYC
verification — name, profile name, full and short statement descriptors, website, product
description — and each row must pass a growing list of checks: all fields present after
trimming; the full descriptor's length inside an inclusive range; the descriptor not a generic
value compared case-insensitively with inner whitespace collapsed; a short descriptor whose
length and first word line up with the full one, and the full descriptor containing the
business's own name; and a well-formed http(s) URL. Print `VERIFIED: <name>` or `NOT VERIFIED:
<name>` per row in input order, and with a `REASONS` flag, the failing codes in one fixed order.

**Constraints to state and honor**
- Optional `PART n` (1–5, default 5) optionally followed by `REASONS` on the first line; rows
  parsed with the `csv` module so quoted commas survive; a header row (first cell
  `business_name`, case-insensitive) and blank lines are skipped; missing trailing columns count
  as empty, extras are ignored; every value is trimmed before any check; up to 10^5 rows.
- Every rule up to the selected part is evaluated on every row, so one row can carry several
  reason codes, always in the fixed order `EMPTY_FIELD, DESCRIPTOR_LENGTH,
  DESCRIPTOR_BLACKLISTED, SHORT_DESCRIPTOR, NAME_MISMATCH, INVALID_URL`.
- Full descriptor length must be 5–31 characters inclusive after trimming; the blacklist
  comparison is case-insensitive with internal whitespace collapsed to single spaces.
- A URL must start with `http://` or `https://` (scheme case-insensitive) and its host (up to the
  next `/`, `?` or `#`) must contain a dot, no whitespace, and not start or end with a dot.

**Grading points**
- One predicate per rule, each returning a bool, collected into the reason-code list in a fixed
  declaration order — that order is the output contract, not an implementation detail to sort
  afterward.
- Normalization (trim, case-fold, whitespace-collapse) happens once at the check boundary, but
  the printed name is the original trimmed value, not the normalized one.
- `PART n` must actually gate which rules run, not just which are printed — a blacklisted
  descriptor is `VERIFIED` under `PART 2`.
- Boundary discipline on both the 5–31 descriptor length and the 2–10 short-descriptor length,
  tested one below, at, and one above each edge.
- Missing/short rows (fewer than six columns) degrade to empty fields rather than raising, and an
  empty `business_name` still prints a well-formed (if odd-looking) `NOT VERIFIED: ` line.
- Quoted CSV fields containing commas must be parsed with the `csv` module, not `split(",")`, and
  must round-trip into the output line unchanged.

**Source**
- `vault/Quick_Check/problems/q15_kyc_verification/problem.md`, `vault/Quick_Check/problems/q15_kyc_verification/REPORT.md`, `vault/stripe/q15_kyc_verification/question.md`, `vault/stripe/q15_kyc_verification/solution.md`, `vault/Quick_Check/study/10-solutions/q15_kyc_verification.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
