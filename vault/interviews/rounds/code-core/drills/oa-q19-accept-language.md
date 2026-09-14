---
nodes: [output.ordering, input.normalization, transfer.stripe-oa]
tags: [stripe-oa, q19]
---
# Drill: resolve an Accept-Language header against a supported-tag list

Sixty minutes, one program handling every rule (no separate parts to unlock — they
accumulate). Line 1 is a browser's `Accept-Language` header value; line 2 is the server's
supported tags in its own preference order. Return the supported tags that satisfy the
request, most preferred first, spelled exactly as the supported list spells them.

- Exact tags: return supported tags mentioned in the header, in header order.
- Language-only tags (`en` with no region): expand to every supported tag whose language
  part matches, in supported-list order, skipping anything already emitted.
- `*`: everything not covered by any explicit header entry, in supported-list order.
- `;q=` weights: the most specific matching entry (exact beats language-only beats `*`,
  ties by header position) decides each tag's weight; sort by weight descending, then by
  the deciding entry's header position, then by supported order; `q=0` drops a tag for
  good, even from a later `*`.

**Constraints to state and honor**
- Tags are `language[-REGION]`, compared case-insensitively; whitespace around tags and
  `;` parameters is ignored; unparsable `q` values default to `1.0`.
- Up to 10^4 header entries against up to 10^3 supported tags.
- A tag repeated in the header, or in the supported list, is still only emitted once.
- No match at all prints the literal `NONE`.

**Grading points**
- One pass that builds `(tag, q, header_position)` per header entry, then picks the *most
  specific* matching entry for each supported tag — not four independent filters applied
  in sequence, which double-counts tags across parts.
- `fr-FR, fr` never repeats `fr-FR`, and `fr, fr-FR` still emits `fr-CA` before `fr-FR`
  because the language-only entry claimed it first — dedup happens at emission, not at parse.
- `q=0` is an exclusion that no less-specific entry (including `*`) can override — model it
  as a claimed-and-rejected tag, not as a weight of zero competing normally.
- Case-insensitive matching, but the *supported list's* spelling is always what gets printed.
- Sort key is `(-q, header_position_of_deciding_entry, supported_index)` — three levels,
  and getting the tie-break order wrong is the easiest way to fail a hidden test that
  otherwise "looks right."

**Source**
- The full statement, solution notes and report: `vault/stripe/q19_accept_language/question.md`,
  `vault/stripe/q19_accept_language/solution.md`,
  `vault/Quick_Check/problems/q19_accept_language/problem.md`.

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
