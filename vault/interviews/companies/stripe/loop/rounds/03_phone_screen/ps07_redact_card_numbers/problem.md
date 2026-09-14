# ps07 · Redact card numbers from logs

**Type:** phone screen (technical) · **Stage:** 45 min technical phone screen, 4 parts · **Last asked:** report undated, page live 2026 (interviewing.io coding-round sample list); staffengprep lists a closely related "Valid Credit Card Number (Redaction)" prompt as active 2026
**Frequency:** 2 independent mentions (interviewing.io "How would you blur credit card numbers from logs?"; staffengprep redaction prompt) plus the general "Card Parsing" phone-screen shape (interviewdb, 2026) that starts from the same redact-then-validate progression · **Confidence:** medium (the interviewing.io line is a one-sentence prompt, not a transcribed I/O spec — this problem.md fixes a concrete, defensible contract for it; flagged in Open points)

## Context
Stripe's own logging pipeline must never persist raw PANs (Primary Account Numbers) — that is a
PCI-DSS requirement, not a style preference. A log-scrubbing filter sits in front of every log
sink and rewrites lines before they hit disk. The naive version ("mask any run of digits that
looks card-shaped") over-redacts: order numbers, Unix timestamps and phone numbers are also
long digit runs. The real filter needs Luhn + network-prefix validation to tell an actual PAN
from a look-alike, and it needs to do this at line-log volume without becoming the bottleneck.
This problem is q05's Luhn/network logic turned around: q05 asks "is this string a valid card
number", ps07 asks "does this line of free text contain one, and if so, blur it" — a Luhn/brand
checker is a *component* here, not the whole problem, and the interesting engineering is span
detection, format-preserving masking and false-positive control, so **do not re-derive q05's
digit-completion or corrupted-card puzzles here**.

## Networks and Luhn (subset relevant to this problem — a superset of q05's)
| network | length(s) | prefix |
|---|---|---|
| VISA | 13, 16, 19 | `4` |
| MASTERCARD | 16 | `51`–`55` or `2221`–`2720` |
| AMEX | 15 | `34` or `37` |
| DISCOVER | 16 | `6011` or `65` |

Luhn: from the rightmost digit moving left, double every **second** digit (2nd, 4th, … from the
right); if a doubled value is `> 9`, subtract 9; sum every digit; valid iff the sum `% 10 == 0`.
(Discover is new versus q05; the `2221`–`2720` Mastercard range is new versus q05 too — q05 only
implements `51`–`55`, so a card like `2223003122003222` is `UNKNOWN_NETWORK` there but a real,
redactable Mastercard here.)

## Input (stdin)
First line is `PART 1`..`PART 4`. Remaining lines are **raw log lines, taken verbatim** —
blank lines are log content (blank lines in the log) and must be **preserved**, not skipped; do
not strip or trim log line content beyond removing the trailing `\n` the line arrived with. A
line may contain arbitrary text: JSON, a URL, a sentence, punctuation. Up to 10^5 log lines;
each individual line up to 10^4 characters. A line may contain zero, one, or several card-like
sequences.

## Output
The same number of lines as the input log body, in the same order, each with any redacted spans
rewritten in place and everything else byte-identical. Part 4 additionally appends one final
line `REDACTED n` (n = total number of spans actually redacted across the whole input).

## Rules

### Part 1 — bare digit runs
A **candidate** is a maximal run of ASCII digits (bounded on both sides by a non-digit character
or start/end of line) whose length is between **13 and 19 digits inclusive** (the real-world PAN
length range). Every candidate found this way is redacted — Part 1 does **not** check Luhn or
network, so it will over-redact (see worked example 1c below; this is intentional and is the
motivation for Part 3). Redaction: replace every digit except the **last 4** with `*`, keep
length and position identical (`4242424242424242` → `************4242`). Runs shorter than 13 or
longer than 19 digits are left completely untouched (a 20-digit run is never partially masked —
document why in your solution: a PAN is never embedded inside a longer digit string here).

### Part 2 — formatted numbers (single space or `-` separators)
A candidate may also be a chain of digit groups joined by a **single** space or `-` between two
digit groups (`4111 1111 1111 1111`, `4111-1111-1111-1111`; mixed separators are accepted too).
A separator may not be doubled, and the chain may not start or end on a separator — the scan
always extends from digit to digit. The **total digit count across the whole chain** (separators
excluded) is what must fall in `[13, 19]`; the chain is one candidate. Redaction preserves the
original separators and grouping exactly, masking only digit characters, keeping the last 4
*digits* (not the last 4 *characters*) visible: `4111-1111-1111-1111` → `****-****-****-1111`.
Still no Luhn/network filter in Part 2 — and this makes the over-redaction risk worse, because
naively chaining "digit group + space + digit group" can accidentally splice two unrelated
numbers together across a space (worked example 2c).

### Part 3 — Luhn + brand filter (false-positive control)
A candidate found by Part 2's scanner (bare or separated, same scanner) is redacted **iff** its
digits pass Luhn **and** match one of the four `(length, prefix)` rules in the table above.
Everything else — wrong length, wrong prefix, right length/prefix but failing Luhn — is printed
**unchanged**, stars and all left out entirely. This is the part that turns Part 1/2's
"any digit-shaped thing" heuristic into a real PAN detector: order numbers, invoice numbers,
Unix-ms timestamps (13 digits, easy collision with the minimum PAN length) and multi-segment
international phone numbers (grouped by spaces, can total 13+ digits) must all survive Part 3
untouched even though they tripped Part 1/2's redaction.

### Part 4 — streaming at log volume
Same detection/redaction rule as Part 3, applied to up to 10^5 lines of up to 10^4 characters
each, with **multiple candidates per line** all handled. Must run in **O(total input length)** —
no line-by-line re-scans that are themselves quadratic in line length, no catastrophic-backtracking
regex. Append a final `REDACTED n` line counting every span actually masked (not every candidate
considered) across the whole input.

## Worked examples
1a. Part 1, single bare PAN:
```
PART 1
user 4242424242424242 charged $10
```
→ `user ************4242 charged $10`

1b. Part 1, boundary lengths (13 and 19 both count; 12 and 20 do not):
```
PART 1
4000000000006
4000000000000000006
123456789012
12345678901234567890
```
→ `*********0006` (13 digits, 9 stars), `***************0006` (19 digits, 15 stars),
`123456789012` (unchanged, 12 digits), `12345678901234567890` (unchanged, 20 digits — never
partially masked)

1c. Part 1 over-redaction (fixed in Part 3): a Unix-ms timestamp is exactly 13 digits.
```
PART 1
{"ts":1735689600000,"event":"login"}
```
→ `{"ts":*********0000,"event":"login"}` — Part 1 wrongly treats the timestamp as a PAN.

2a. Part 2, formatted VISA:
```
PART 2
Card: 4111-1111-1111-1111 charged $50
Card: 4111 1111 1111 1111 charged $50
```
→ `Card: ****-****-****-1111 charged $50`, `Card: **** **** **** 1111 charged $50`

2b. Part 2, a 20-digit chain (5 groups) is never touched:
```
PART 2
4111-1111-1111-1111-2222
```
→ `4111-1111-1111-1111-2222` (unchanged — 20 digits total, out of range)

2c. Part 2 over-grouping on an unrelated number (fixed in Part 3): an international phone number
written in 4 space-separated groups happens to total 13 digits, so Part 2's naive scanner treats
the whole thing as one candidate and redacts it — **wrong on purpose**, this is exactly the false
positive Part 3 exists to fix.
```
PART 2
call +86 138 0013 8000 now
```
→ `call +** *** **** 8000 now` (candidate is `86 138 0013 8000`, 13 digits total: `86`+`138`+
`0013`+`8000`; first 9 digits masked, last 4 — all of `8000` — kept, group/space structure
preserved; the leading `+` is not a digit so it stays outside the candidate).

3a. Part 3 fixes 1c and 2c — same two lines, same part header, now left alone:
```
PART 3
{"ts":1735689600000,"event":"login"}
call +86 138 0013 8000 now
order 1234567890123456 shipped
```
→ all three lines **unchanged**: the timestamp fails every brand prefix, the phone number's
combined digits (`8613800138000`) start with `86` (no brand matches), and the order number
starts with `12` (no brand matches) — none of the three is Luhn+brand-valid.

3b. Part 3, real PANs still get redacted, including the two networks q05 doesn't cover:
```
PART 3
mc old range 5555555555554444 refund
mc new range 2223003122003222 refund
discover 6011111111111117 refund
amex 378282246310005 refund
bad checksum 4242424242424241 refund
```
→ `mc old range ************4444 refund`, `mc new range ************3222 refund`,
`discover ************1117 refund`, `amex ***********0005 refund`,
`bad checksum 4242424242424241 refund` (last line unchanged — Luhn fails, `...4241` not `...4242`)

4a. Part 4, multiple cards on one line + trailing stats:
```
PART 4
4242424242424242 and 5555555555554444 both charged
not a card: 42 42
```
→
```
************4242 and ************4444 both charged
not a card: 42 42
REDACTED 2
```

## Edge cases hidden tests are known to target
- $0/empty lines and blank input lines must be **preserved** in the output, not dropped
- exactly 13 and exactly 19 digits both count; 12 and 20 do not (Part 1 boundary)
- a candidate embedded with no whitespace at all, e.g. `id=4242424242424242;` (non-digit
  boundary can be punctuation, not just whitespace)
- two candidates on the same line, some redacted and some not (mixed Part 3/4 result per line)
- a line entirely made of one redacted candidate (nothing else on the line)
- last-4-digit masking counts **digits**, not characters, when separators are present
- a chain with a doubled separator (`4111--1111`) or leading/trailing separator (`-4111 1111`,
  `4111 1111-`) stops the scan at the break — never redacted as one candidate across the break
- Luhn-valid, right length, wrong prefix (e.g. a 16-digit `9`-prefixed number) is left alone
- right length + prefix, Luhn fails → left alone (`4242424242424241`)
- `2221`–`2720` Mastercard prefix and `6011`/`65` Discover prefix, both absent from q05, must be
  recognized here
- 10^5 lines / 10^4 chars per line must complete comfortably inside the 2 s perf budget — no
  regex with nested quantifiers over the whole line, no O(line²) rebuilding of the output string
- `REDACTED n` counts spans actually masked (post-filter), not raw Part-1/2-style candidates
- Part 3/4 **by design**: a real PAN glued to a short number by one space (`ref 12 4242424242424242`)
  is scanned as one 18-digit chain that matches no brand, so it is left alone — the maximal-chain
  rule is the contract; the recall/precision trade-off is follow-up question 1

## Variants seen in the wild
- staffengprep's "Valid Credit Card Number (Redaction)" collapses masking + brand check + Luhn
  into one linear pass without the "naive first, filtered later" progression this problem uses —
  same end state, different part boundaries.
- Some retellings mask to a fixed display form (`•••• •••• •••• 1234`) instead of preserving the
  original text's punctuation; this problem keeps the source format intact, which is closer to
  what an actual log scrubber must do (it cannot rewrite unrelated surrounding text).
- q05's four-part Luhn/network/redacted-`*`/corrupted-`?` progression is the *upstream* validation
  problem this one assumes as a prerequisite skill, not a part of this problem — do not
  reimplement `*`-wildcard completion counting or `?`-corruption enumeration here.

## What this tests
skills: S02 parsing free text (not delimited records) · S09 exact, format-preserving output ·
S14 Luhn digit walking / string canonicalization (reused from q05, applied to a new purpose) ·
S18 false-positive/validation discipline (redact only what's provably a PAN) · S19 incremental
design (Part 1 ⊂ Part 2 ⊂ Part 3 ⊂ Part 4) · S21 stdlib fluency (single-pass scanning without
backtracking regex)

## Sources
- https://interviewing.io (coding-round sample question list, phrased "How would you blur credit
  card numbers from logs?" — no published transcript; C8 in `loop/raw/en_forums.md` §6.2)
- staffengprep, "Valid Credit Card Number (Redaction)" listing (via interviewdb's "Card Parsing" /
  "Credit Card Number" phone-screen entry, 2026; P13 in `loop/raw/en_forums.md` §3.3)
- https://docs.stripe.com/testing (Stripe test card numbers used verbatim in worked examples)
- q05 (`problems/q05_card_validation_luhn/problem.md`) for the Luhn algorithm and the three
  networks it already covers; this problem's brand table is q05's plus Discover and the
  `2221`–`2720` Mastercard range

## 面试官会怎么追问
1. "Your Part 2 scanner joined a phone number into one candidate across two spaces — walk me
   through why, and show me the input where that happens before I ask." (worked example 2c —
   answer: greedy space/`-` chaining has no notion of "this looks like a phone number", only
   Part 3's Luhn+brand filter fixes it; alternative would be requiring a canonical group shape
   like 4-4-4-4, trading recall for precision)
2. "What if the log line is split across a network buffer boundary and a card number spans two
   physical `read()` calls — does your Part 4 API still work?" (answer: `part4([...lines])`
   already assumes lines are reassembled before redaction; if the boundary can literally split a
   digit run, you'd need a stateful streaming scanner that carries an unresolved suffix between
   `process(chunk)` calls — sketch the API change without full-implementing it)
3. "Why not just use one `re.compile(...)` with `\d[\d -]{11,23}\d` and post-filter?" (answer:
   catastrophic backtracking risk on adversarial input with runs of separators, and it doesn't
   naturally give you per-position digit indices for the last-4 mask without a second pass — the
   hand-rolled scanner gives both in one O(n) pass)
4. "PCI-DSS says redact the PAN — why do you keep the last 4 digits at all instead of blurring
   everything?" (answer: last-4 is the standard partial-PAN display used for customer support /
   dispute lookup; it is explicitly allowed under PCI-DSS as long as it can't reconstruct the
   full PAN, unlike, say, keeping the first 6 which *is* the BIN and identifies the issuer)
5. "Extend this to JCB or UnionPay." (answer: one more row in the network table — length +
   prefix set; the scanner and Luhn check are untouched, which is the point of separating
   "is this candidate shaped like a PAN" from "which specific networks count")
6. "How would you convince yourself this is safe to deploy against real production logs before
   turning it on?" (answer: run it read-only against a sample of real logs, diff the before/after
   byte count and manually audit a sample of every *new* redaction and every *skipped* candidate
   near the boundary lengths, rather than trusting the unit tests alone)

## Open points
- The interviewing.io source is a single sentence with no published I/O contract, part count, or
  worked examples; everything in Rules/Worked examples beyond "find and blur card numbers in
  free-text logs" is this report's reconstruction, built from (a) q05's already-verified Luhn/
  network logic, (b) the general Stripe phone-screen "increasingly strict validation" template
  seen across P13/q05/ps05, and (c) real PCI-DSS partial-PAN display conventions. If a verbatim
  transcript of this prompt surfaces, reconcile the part boundaries against it.
