---
nodes: [model.event-stream, model.reversal, model.idempotency, model.entity-state, rules.thresholds, output.ordering, output.sentinels, verification.edge-catalog, round.reading]
tags: [classic]
---
# Drill: an event stream with reversals, in four unlocking parts

Forty-five minutes, stdin to stdout, no libraries beyond the standard one.

A stream of comma-separated lines declares entities, then reports events against
them. Some events increment two counters per entity; a later event can *reverse*
an earlier one by id, undoing its effect completely. Each entity carries a
category, and each category carries a threshold that is either a **count** or a
**ratio** — an integer literal means count, a literal with a decimal point means
ratio, even `1.0`. A ratio only applies once the entity has a stated minimum
volume. Part 1 prints the parsed configuration, part 2 the per-entity counters,
part 3 the set of entities currently over threshold, part 4 the same after
reversals are honoured.

**Constraints to state and honor**
- Up to 10^5 event lines and 10^4 entities; 2 s wall time, 256 MB.
- Setup lines apply before all events wherever they appear in the file.
- Output is one line: the flagged ids in plain string order joined by `,`, or the
  literal `NONE`.
- No floating point anywhere in the comparison path.

**Grading points**
- Read all four parts before designing the state; the reversal in part 4 decides
  whether you keep a per-event ledger ([[cc-transfer-oa-four-stage-pipeline]]).
- Ratio compared by integer cross-multiplication, not division
  ([[cc-python-pitfalls-float-equality]]).
- Boundary handling on both thresholds: `==` is over, one below is not
  ([[cc-verification-edge-exact-threshold-triple]]).
- Reversal is idempotent: a second reversal of the same id is a no-op, an unknown
  id is ignored, and reversing the last event leaves 0/0 without dividing
  ([[cc-verification-edge-zero-negative-and-max]]).
- Only the touched entity is re-evaluated after each event
  ([[cc-performance-hot-loop-rescan-entities]]).
- `NONE` versus an empty line, and plain string order (`a10` before `a2`)
  ([[cc-python-io-exact-stdout]]).

**Attempt log**
- [ ] Attempt 1 (date, 45 min, self-graded notes):
