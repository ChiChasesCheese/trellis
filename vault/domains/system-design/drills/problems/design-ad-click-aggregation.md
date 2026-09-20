---
nodes: [problems.search.ad-click-aggregation, async.streaming.processing, async.delivery.exactly-once]
tags: [problem]
---
# Drill: Design a billing-grade ad click aggregation pipeline

Design the pipeline that counts ad clicks accurately enough to bill advertisers on, for a
network doing 500 million clicks/day (avg ≈ 5,787/s, peak ≈ 23,148/s at a 4x factor) at an
average CPC of $0.35/click (≈ $175M/day in ad spend). Advertisers need a near-real-time spend
dashboard (minute-level) and a daily, audit-grade "final" billing figure that must match a
full recount of the raw log exactly.

**Constraints to state and honor**
- Streaming (provisional) results queryable P99 < 1 minute after a window closes; the
  reconciled, final billing figure must land within 24 hours of the event.
- Target accuracy after reconciliation: zero discrepancy against a full batch recount — not
  "close enough."
- ~3% of raw click deliveries are duplicates of an already-seen click (client retries) that
  must never be billed twice.
- Click price (`click_price`) is fixed at the moment of the click and is never recomputed
  later.

**Grading points**
- Justifies why deduplication uses an exact keyed store rather than a probabilistic sketch,
  contrasting explicitly with a heavy-hitters/Top-K design's tolerance for bounded error
  ([[problems-ad-click-aggregation-exact-dedup-vs-sketch]]).
- Computes the dollar exposure of a given accuracy target from click volume and average CPC,
  and uses that number to justify the extra machinery rather than asserting "correctness
  matters" without a figure ([[problems-ad-click-aggregation-dollar-error-budget]]).
- Uses two different partition keys across the pipeline (by click identity for
  deduplication, by ad for aggregation) and explicitly repartitions between them, rather than
  assuming one partitioning scheme serves both stages
  ([[problems-ad-click-aggregation-dual-partition-key]]).
- States that a watermark is a heuristic estimate of completeness, not a correctness proof,
  and uses retractions (not silent overwrites) when a window re-triggers on late data
  ([[problems-ad-click-aggregation-watermark-heuristic-retraction]]).
- Lays out a graduated policy for late data arriving after the watermark, distinguishing
  what's cheap to correct from what should be excluded from automatic correction
  ([[problems-ad-click-aggregation-late-data-three-tiers]]).
- Builds the OLAP sink's idempotency key entirely from deterministic fields so a
  checkpoint-replay produces a safe overwrite instead of a duplicate row
  ([[problems-ad-click-aggregation-deterministic-upsert-key]]).
- Recognizes a viral ad campaign as a hot-partition scenario under ad_id partitioning and
  applies salting, while explaining why the resulting merge is always exact (unlike a Top-K
  shard merge) ([[problems-ad-click-aggregation-hot-ad-id-salting]]).
- Treats the streaming result as provisional and the nightly batch recount as the actual
  source of billing truth, with any correction logged rather than silently applied
  ([[problems-ad-click-aggregation-reconciliation-source-of-truth]]).
- Grounds the exactly-once sink argument in the idempotent-producer / transactional
  consume-transform-produce composition rather than treating "exactly-once" as a single
  feature toggle ([[async-eos-boundary-choice]], [[async-eos-sink-determinism]]).

**Solution**: [[solution-ad-click-aggregation]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
