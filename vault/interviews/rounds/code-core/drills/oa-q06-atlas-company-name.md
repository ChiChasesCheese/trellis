---
nodes: [input.normalization, model.idempotency, transfer.stripe-oa]
tags: [stripe-oa, q06]
---
# Drill: check, register, and reclaim company names by canonical form

Sixty minutes, stdin to stdout, no libraries beyond the standard one. A
Delaware-style "name availability" check: two names are the same if they
normalize to the same canonical form, where normalization is a fixed,
order-sensitive pipeline (case-fold; turn `&`/`,` into spaces; split on
whitespace; strip trailing entity suffixes like `inc`/`llc`/`corp`
repeatedly; drop one leading article; drop every `and` token except a
leading one; turn remaining punctuation into spaces and re-split; rejoin). A
name whose canonical form is empty is never available and never registered.

- Part 1: a stateless check — is a proposed name's canonical form distinct
  from every name in a preloaded registered-names block? Requests don't
  affect each other.
- Part 2: make acceptance persistent — an accepted name is registered to its
  requesting account immediately, and every later request for that canonical
  form (from any account, including the original registrant) is unavailable.
- Part 3: add `RECLAIM`, which frees a name, but only when issued by the
  account that actually registered it; anything else (wrong account,
  unregistered name, or a name from the original preloaded block) is quietly
  ignored and reclaim itself prints nothing.

**Constraints to state and honor**
- Normalization step order matters: suffix-stripping must happen before
  general punctuation is blanked out, or a suffix like `L.L.C.` gets
  shredded before it can be recognized.
- The leading-article removal happens before deciding which `and` token is
  "first," so `The And Co` becomes `and co`.
- `RECLAIM,account_id,name` lines may contain commas inside the name itself
  — split on the first two commas only, not on every comma.
- Output only for availability requests, one line per request in input
  order, `account_id|Name Available` or `account_id|Name Not Available`.

**Grading points**
- Normalization implemented as one pure function used identically for
  registered names, requests, and reclaim targets — not reimplemented or
  drifted between call sites.
- Suffix stripping is a loop ("while last token is a suffix"), not a single
  strip, since suffixes can stack (`Llama Inc. LLC`); a suffix word appearing
  mid-name is left alone.
- The registry stores canonical-form to registrant, with the preloaded block
  entries carrying no registrant (so no account can ever match them for
  reclaim) — a candidate should be able to explain why a single comparison
  like `registry.get(name) == account_id` simultaneously excludes the
  wrong-account, never-registered, and block-only cases.
- A rejected request registers nothing; an empty canonical form is never
  available and never stored.
- Re-requesting your own already-registered name is correctly Not Available
  — a common wrong assumption is that the registrant is exempt.
- Reclaim matches on canonical form, not literal spelling, and a name freed
  by reclaim becomes available again to anyone, including the original
  registrant, on the very next request.

**Source**
- `vault/interviews/companies/stripe/problems/q06_atlas_company_name/problem.md`
- `vault/interviews/companies/stripe/study/10-solutions/q06_atlas_company_name.md`
- `vault/interviews/companies/stripe/problems/q06_atlas_company_name/problem.md`
- `vault/interviews/companies/stripe/problems/q06_atlas_company_name/REPORT.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
