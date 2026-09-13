# q34 · Compress URL — numeronyms per path segment, tail folding, ambiguity check

**Type:** phone screen (live coding, ~35 min) · **Stage:** Stripe phone interview · **Last asked:** 2022 (joeytor/StripeInterview, README → "Phone Interview")
**Frequency:** 1 independent source with verbatim prompt + driver calls (joeytor/StripeInterview `Compress.java`) · **Confidence:** medium-high (verbatim prompt, single source)

## Context
Stripe logs billions of request URLs. The data-science team wants to run analytics on them, but
(1) the raw URLs leak user privacy and (2) they are expensive to store. Real systems hash; in the
interview we **compress each word into a numeronym** (`internationalization` → `i18n`,
`stripe` → `s4e`): first letter, number of letters in between, last letter. That keeps the
shape of the URL (path depth, word count) while hiding the words.

## Input (stdin)
First line `PART n` (n ∈ 1..4), then one query per line. Blank lines are ignored.
- Part 1: `url` — lowercase letters plus the separators `/` and `.` only; no empty parts
  (no leading/trailing separator, no `..`, no `//`); every minor part has ≥ 3 letters.
- Part 2: `url,m` — `m > 0` integer.
- Part 3: `url,min_len` — minor parts may now be shorter than 3 letters.
- Part 4: one `url` per line (a whole log); may contain duplicates.

## Output
- Parts 1–3: the compressed URL, one line per query.
- Part 4: every compressed form that is produced by **two or more distinct** original URLs,
  as `compressed: count` (count = number of distinct originals), sorted by compressed string;
  no output if none.

## Rules
### Part 1 — `compress(url)`
Split the string into **major parts** on `/`; split each major part into **minor parts** on `.`.
Replace every minor part `w` by its numeronym `w[0] + str(len(w) - 2) + w[-1]`. Re-join with
the same separators (`.` inside a major part, `/` between major parts).

### Part 2 — `compress(url, m)`: keep at most `m` minor parts per major part
If a major part has more than `m` minor parts, keep the first `m-1` numeronyms as in Part 1,
then fold **everything from the m-th minor part to the end** (dots included) into one
numeronym: first letter of the m-th minor part, the number of characters strictly between it
and the last letter of the last minor part (**dots count as characters**), last letter of the
last minor part. A major part with ≤ `m` minor parts is unchanged from Part 1.
(`m = 1` therefore folds each whole major part: `stripe.com` → `s8m`.)

### Part 3 — minimum length threshold (reconstructed)
Real URLs contain short words (`a`, `to`, `v1`). A minor part (or a Part-2 folded tail) with
fewer than `min_len` characters is emitted **unchanged** (`len == min_len` still compresses).
Parts 1–2 have no threshold (`min_len = 0`) and reproduce the source's Java for short words
(`to` → `t0o`, `a` → `a-1a`); with `min_len = 3`: `ab` stays `ab`, `abc` → `a1c`.

### Part 4 — decompression ambiguity (reconstructed)
Numeronyms are lossy: `payments` and `pastries` both become `p6s`. Given a log of URLs,
report each compressed form (Part 1 rules) that is shared by ≥ 2 **distinct** originals,
with the number of distinct originals, sorted by the compressed string. Exact duplicate URLs
count once.

## Worked examples
```
PART 1
stripe.com/payments/checkout/customer.maria           -> s4e.c1m/p6s/c6t/c6r.m3a
section/how.to.write.a.java.program.in.one.day        -> s5n/h1w.t0o.w3e.a-1a.j2a.p5m.i0n.o1e.d1y
```
(the second line shows why Part 3 exists: `a` → `a-1a` under the ≥ 3-letter assumption)
```
PART 2
stripe.com/payments/checkout/customer.maria,1         -> s8m/p6s/c6t/c12a
section/how.to.write.a.java.program.in.one.day,3      -> s5n/h1w.t0o.w29y
```
`w29y`: tail `write.a.java.program.in.one.day` is 31 characters, minus the first and last = 29.
```
PART 3
docs/a.b.to.api,3                                     -> d2s/a.b.to.a1i
docs/a.b.to.api,4                                     -> d2s/a.b.to.api
PART 4
payments/checkout
pastries/checkout
payments/checkout
pay/checkout                                          -> p6s/c6t: 2
```

## Edge cases hidden tests are known to target
- a major part with exactly `m` minor parts is *not* folded (identical to Part 1)
- `m = 1` folds the whole major part including its dots (`customer.maria` → `c12a`, not `c6r.m3a`)
- a 3-letter word → `x1x`; Part 3 `min_len` boundary: `len < min_len` unchanged, `len == min_len`
  compressed; without a threshold `to` → `t0o` and `a` → `a-1a` (the source's Java output)
- a single word with no separators; a URL that is one major part with many minor parts
- Part 4: exact duplicates count once; compressed forms with a single original are not printed;
  output sorted by compressed string (plain string order)
- Part 3 threshold applies to the folded tail as well (`a.b` is 3 characters → `a1b` at `min_len=3`)

## Variants seen in the wild
- Plain "numeronym" warm-up (`internationalization` → `i18n`, `localization` → `l10n`) before the
  URL framing.
- Hashing the parts instead (the prompt itself says the real-world fix is hashing).

## What this tests
skills: S02 parsing · S09 exact formatting · S14 string canonicalization · S19 incremental design · S20 self-testing

## Sources
- https://github.com/joeytor/StripeInterview `src/main/java/Compress.java` (README → Phone Interview; verbatim prompt + driver calls)
