# Task: map the old DDIA `system-design` domain onto today's 系统设计 tree (read-only)

Chi (2026-11-28): the old `system-design` domain (English, DDIA-structured, 856 cards, not in Anki) may be migrated
into today's 系统设计 (`skeleton/sysdesign.yaml`, local; public projection `atlas/skeletons/sysdesign.yaml`), in
today's card format, with new leaves where needed. Before any card is written we need to know what is actually new.

Read: `skeleton/system-design.yaml`, `vault/domains/system-design/` (cards, readings, drills, cases),
`skeleton/sysdesign.yaml` (node ids, titles, summaries), and the questions (`## Q` only) of the cards under each
sysdesign node (cards live in `vault/domains/hello-interview/`, `vault/domains/bagu/`, `vault/domains/payments/`; find a
card's node in its frontmatter). Never read `vault/private/`.

## Produce `sources/local/audit/ddia-map.md` and `ddia-map.json`

1. **Every old leaf** (system-design skeleton leaves, non-`problems` branches): old id, title, card count; the closest
   sysdesign node(s) (id + title); verdict `covered` (today's cards already ask the same mechanisms), `partial` (some
   of its cards add something; list which old card ids), or `unique` (nothing comparable); for `partial`/`unique`, one
   line on what is new and a proposed home: an existing sysdesign node, or a new leaf (parent node id + a Chinese
   title in today's style, English term in parentheses).
2. **Every old design problem** (`problems.*`): old id, title, cards; matching sysdesign problem (`qb.*`/`sd.*`
   problem-breakdown nodes) or none; verdict as above.
3. **Readings**: for each old reading, the sysdesign node it would serve as Go deeper (or none); count how many have
   a clipping on disk.
4. **Drills and cases**: count and one line each on where they would hang.
5. **Totals**: cards covered / partial / unique; new leaves proposed per sysdesign branch; an estimate of new Chinese
   cards to write (partial + unique, after merging near-duplicates).
6. **Ten sample candidates**: the ten old cards most worth migrating first (most load-bearing, not covered), with
   their target node — these become the first sample batch for Chi.

Judge by mechanism, not wording: an old card is covered only if a current card asks the same thing at the same depth.
Spot-check your verdicts by reading both sides for at least 15 leaves. Do not modify anything; do not commit.
Report: the totals, the ten candidates, and the three verdicts you are least sure about.
