# q06 · Atlas Company Name Availability — normalize, register, reclaim

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 3 parts; "Atlas Company Name Check" on Blind) · **Last asked:** 2026-02 (extrabrain listing); 2025-09 (linkjob); Blind ijfwtgl0 2026-03 area
**Frequency:** 5 independent sources (femisowems repo with verbatim I/O, linkjob 2025-09, extrabrain 2026-02, Blind, programhelp low-confidence variant) · **Confidence:** high (verbatim statement + expected output)

## Context
Stripe Atlas incorporates companies in Delaware, where a name must be "distinguishable upon the
records" — small differences in case, punctuation, entity suffix (`Inc.`, `LLC`) or a leading
article do not make a name distinct. This exercise models the availability check: every name is
reduced to a canonical form and compared against the canonical forms of registered names. Later
parts turn the check into a persistent registry (an accepted name is taken from then on) and add
dissolution (`RECLAIM`), which frees a name — but only when the original registrant asks.

## Normalization (applies to registered and proposed names alike)
1. lowercase
2. `&` and `,` become spaces
3. split on whitespace (this collapses runs of spaces)
4. remove trailing entity-suffix tokens **repeatedly** while the last token is one of
   `inc` `inc.` `corp` `corp.` `llc` `l.l.c.` `llc.` (case-insensitive)
5. drop a leading article `the` / `a` / `an` (one token, once)
6. drop every `and` token **except when it is the first token** (after step 5)
7. in the remaining tokens, any other punctuation (`.`, `-`, `'`, `/`, …) becomes a space and the
   tokens are re-split *(reconstructed: sources only spell out `&` and `,`; flag
   `strip_punctuation=False` disables this step)*
8. join with single spaces. **Empty result → the name is Not Available** (and never registered).

`The Llama, Inc.` → `llama`; `Llama And Friend, Inc.` → `llama friend`; `And Llama Friend` →
`and llama friend` (distinct); ` &Co, LLC.` → `co`; `The Inc.` → `` (unavailable).

## Input (stdin)
First line `PART n` (n ∈ 1..3; optional, default 3). Then an optional block
```
REGISTERED
<one already-registered name per line>          (no account — nobody can reclaim these)
REQUESTS
```
followed by one request per line. Without the headers every line is a request. Blank lines are
ignored; leading/trailing whitespace of a line is stripped, interior spacing is significant only
up to normalization. Request forms:
- `account_id|proposed_name` — availability request (Parts 1–3)
- `RECLAIM,account_id,original_proposed_name` — dissolution (Part 3; the name may itself contain
  commas — split on the first two commas only)

## Output
One line per availability request, in input order: `account_id|Name Available` or
`account_id|Name Not Available`. `RECLAIM` lines print nothing.

## Rules
### Part 1 — basic availability check (stateless)
A proposed name is available iff its normalized form is non-empty and not equal to the normalized
form of any name in the `REGISTERED` block. Requests do not affect each other.
*(The repo statement already says "register it immediately"; that behaviour is Part 2. Use
`part1(lines, persist=True)` if a grader expects Part 1 to register.)*

### Part 2 — persistent registration
Part 1, plus: an **accepted** name is registered to the requesting account immediately and is
Not Available for every later request — from any account, **including the account that
registered it** (re-submitting your own name is Not Available). Rejected requests register nothing.

### Part 3 — reclamation
`RECLAIM,account_id,original_proposed_name`: if the normalized name is registered **and its
registrant is `account_id`**, remove it (the name becomes available to anyone, including the
former owner). Otherwise ignore the line: wrong account, name not registered, or a name from the
`REGISTERED` block (which has no registrant). Reclaiming never prints anything.

## Worked examples
Example 1 (Part 1 — stateless):
```
PART 1
REGISTERED
Llama, Inc.
Acme & Sons Corp.
REQUESTS
1|The Llama
2|acme and sons
3|Llama Friends
4|Llama Friends
5|The Inc.
```
→ `1|Name Not Available`, `2|Name Not Available` (`acme sons` both), `3|Name Available`,
`4|Name Available` (Part 1 does not register), `5|Name Not Available` (normalizes to empty).

Example 2 (Part 2 — persistent):
```
PART 2
1|Llama, Inc.
2|The Llama
3|Llama And Friend, Inc.
4|And Llama Friend, Inc.
5|Llama,  Inc.
6| &Co, LLC.
1|LLAMA
```
→ `1|Name Available`, `2|Name Not Available`, `3|Name Available`, `4|Name Available`,
`5|Name Not Available`, `6|Name Available`, `1|Name Not Available` (own name, still taken).

Example 3 (Part 3 — verbatim repo sample):
```
PART 3
1|Llama, Inc.
2|The Llama
3|Llama And Friend, Inc.
4|And Llama Friend, Inc.
5|Llama,  Inc.
6| &Co, LLC.
RECLAIM,1,Llama, Inc.
7|Llama
8|Co
9|and co
RECLAIM,6, &Co, LLC.
10|Co
```
→
```
1|Name Available
2|Name Not Available
3|Name Available
4|Name Available
5|Name Not Available
6|Name Available
7|Name Available
8|Name Not Available
9|Name Available
10|Name Available
```
(after `RECLAIM,1` the name `llama` is free so 7 gets it; 8 collides with 6's `co`; 9 keeps its
leading `and`; after `RECLAIM,6` 10 gets `co`.)

Example 4 (Part 3 — reclaim by the wrong account is ignored):
```
PART 3
1|Acme
RECLAIM,2,Acme
2|ACME
RECLAIM,1,acme inc
2|Acme
```
→ `1|Name Available`, `2|Name Not Available`, `2|Name Available` (reclaim by the registrant
matched on the normalized form `acme`; the former owner's name is free for anyone).

## Edge cases hidden tests are known to target
- normalized-empty names (`Inc.`, `The`, `A, LLC`, `&`, `,`) are Not Available and never registered
- repeated suffixes (`Llama Inc. LLC`) are all stripped; a suffix word in the middle (`Inc Llama`)
  stays; `L.L.C.` must be recognised before its dots are treated as punctuation
- `And` at the start is kept, elsewhere dropped; `The And Co` → `and co` (article removed first)
- article + suffix only differences: `The Llama` == `Llama, Inc.` == `llama`
- double spaces, tabs, leading/trailing spaces inside the name part
- same account re-registering its own name → Not Available; a rejected request registers nothing
- RECLAIM by a non-registrant, of an unregistered name, or of a `REGISTERED`-block name → ignored;
  reclaim matches on the normalized name, not the original spelling; reclaim prints nothing
- after a reclaim the very next identical request is Available; reclaiming twice is harmless
- names containing commas inside `RECLAIM,…` (split on the first two commas only)

## Variants seen in the wild
- programhelp (low confidence): "only letters/digits/spaces, length 2–50, not on a blacklist →
  valid/invalid". Not implemented.
- Part 1 already registering accepted names (femisowems wording) — `part1(lines, persist=True)`.
- Delaware-style suffix list extended with `Corporation`, `Ltd`, `Co.` — add to `SUFFIXES`.

## What this tests
skills: S02 parsing (two record shapes, commas inside names) · S03 registry keyed by normalized
name · S09 exact format · S11 idempotency of registration · S14 string canonicalization (case,
punctuation, suffix/article stripping) · S18 validation/ignored requests · S19 incremental design

## Sources
- https://github.com/femisowems/stripe-interview-questions/tree/main/question1 (verbatim Problem1.md + sample_input/expected_output)
- https://www.teamblind.com/post/what-does-stripe-hackerrank-test-have-ijfwtgl0 ("Atlas Company Name Check … three parts, only 60 minutes")
- linkjob.ai 2025-09-16 OA write-up; extrabrain.app 2026-02-10 (identical 3-part rules)
- programhelp.net 2025-09-21 (low-confidence variant)
- https://support.stripe.com/questions/choosing-a-name-for-your-stripe-atlas-company ; https://stripe.com/resources/more/is-your-company-name-available-in-delaware-here-is-how-to-find-out

## Clarifications (from adversarial review, 2026-08-26)
- The word `and` is dropped only as a standalone token (`Salt and-Pepper` keeps the hyphenated `and-pepper` token as is); step 7 (`and` removal) is reconstructed from aggregator descriptions.
