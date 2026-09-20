---
nodes: [problems.social.tinder, distributed.consistency]
tags: [problem]
---
# Drill: Design a dating app's candidate feed and matching engine like Tinder

Design the candidate-feed and swipe/match paths for a dating app: 10 million daily active
users, each swiping about 150 times/day, geo- and preference-filtered candidates, and
exactly-once mutual-match detection when two right-swipes race.

**Constraints to state and honor**
- 10,000,000 DAU × 150 swipes/day → a computed peak swipe-write QPS of about 52,083, and
  a computed peak right-swipe QPS of about 10,417 (the load that drives match detection).
- A user must never be shown a profile they already swiped on, in either direction.
- Two users who right-swipe each other within milliseconds must be notified exactly once —
  no duplicate notification, no missed match.
- The design must identify which layer runs out of headroom first using real computed
  safety margins, not a guess, and must name what changes at 10x scale.

**Grading points**
- Computes the peak swipe-write QPS against an assumed relational-primary ceiling and
  shows the ratio that forces swipe writes onto a wide-column store partitioned by
  swiping user id, rather than a single relational primary ([[problems-tinder-swipe-write-forces-wide-column]]).
- Computes the right-swipe peak QPS (not the confirmed-match rate) against a single Redis
  instance's official benchmark and states the resulting safety margin, contrasting it
  with a much thinner margin elsewhere in this bank to argue when hot-key defenses are
  and aren't warranted ([[problems-tinder-match-gate-safety-margin]]).
- Chooses a seen-set representation (Bloom filter vs. explicit per-user set) using a
  computed storage comparison, and can state why a Bloom filter's only error direction is
  safe for this exclusion problem ([[problems-tinder-bloom-filter-storage-reduction]]).
- Recognizes that folding an entire seen-set into an index-side `must_not terms` query
  runs into a real per-query term-count ceiling at the size a heavy user's history reaches,
  and designs around it instead of assuming index-side filtering scales unboundedly
  ([[problems-tinder-index-side-filter-terms-cap]]).
- Designs match detection as an atomic check-and-set on a canonical pair key rather than a
  relational transaction (too slow at the computed peak) or an ordered log (too much
  latency for an instant match notification), and can argue why against both alternatives
  ([[problems-tinder-match-detection-canonical-pair-key]]).
- Applies preference filters bidirectionally in the candidate query (not just the viewer's
  own preferences) and explains why one-directional filtering wastes candidate density
  ([[problems-tinder-bidirectional-preference-filter]]).
- Names a real hot-spot/skew scenario in geo-sharded candidate indexes (time-zone-driven
  peak imbalance between shards) and a load-balancing fix that avoids solving an NP-hard
  placement problem ([[problems-tinder-geoshard-timezone-imbalance]]).
- States what happens to the match-gate's safety margin at 10x DAU and what concrete
  infrastructure change that forces ([[problems-tinder-10x-match-gate-sharding]]).

**Solution**: [[solution-tinder]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
