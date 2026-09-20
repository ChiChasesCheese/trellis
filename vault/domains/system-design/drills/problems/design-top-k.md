---
nodes: [problems.search.top-k, async.streaming.processing]
tags: [problem]
---
# Drill: Design a real-time Top-K / trending leaderboard

Design a "most-viewed" leaderboard for a content platform with 300M DAU generating 200
views/user/day (60 billion views/day, average QPS ≈ 694,000, peak ≈ 2.08M/s at a 3x diurnal
factor). The leaderboard must serve Top-K (K ≤ 1000) for four window granularities at once
(1 minute, 1 hour, 1 day, all-time), globally and sliced by dimensions like country and
category, with near-real-time freshness and a mathematically bounded error on any estimated
count.

**Constraints to state and honor**
- Read latency P99 < 50ms; a closed 1-minute window's leaderboard must be queryable P99 < 5s
  after close.
- Every returned estimated count must carry a computed, provable error bound — not "close
  enough" empiricism.
- ~80M distinct items receive at least one view on a given day (assumption).
- Deleted/taken-down items must never appear in results, even if their historical count is
  still high.

**Grading points**
- States when exact counting (hash map + heap) is actually the right answer — item-id-keyed
  partitioning with disjoint per-shard item sets — versus when unbounded or multi-dimensional
  cardinality forces an approximate structure
  ([[problems-top-k-partition-by-item-id-exact-merge]]).
- Sizes a Count-Min Sketch from a chosen (ε, δ) and computes its width, depth, memory, and
  guaranteed absolute error as ε·N — and explains why the same ε cannot be reused unchanged
  across window granularities with different N ([[problems-top-k-cms-error-bound]]).
- Uses Space-Saving to get a deterministic (not probabilistic) guarantee that any sufficiently
  frequent item survives into a bounded candidate set, and computes the counter count needed
  for a stated frequency floor ([[problems-top-k-space-saving-guarantee]]).
- Explains why Count-Min Sketch and Space-Saving are run together rather than picking one —
  one is mergeable but can't enumerate, the other enumerates but doesn't merge cleanly
  ([[problems-top-k-cms-vs-space-saving-tradeoff]]).
- Builds the four window granularities via hierarchical rollup (cell-wise sketch summation)
  instead of reprocessing the raw stream once per granularity
  ([[problems-top-k-hierarchical-window-rollup]]).
- Merges overlapping (non-disjoint) per-dimension sub-shard results correctly — candidate-id
  union plus a cell-summed merged sketch — rather than unioning or truncating local Top-K
  lists directly ([[problems-top-k-dimension-sharding-merge-correctness]]).
- Identifies the hot-key skew a viral item causes under item_id partitioning and states the
  salting mitigation and its cost ([[problems-top-k-hot-item-salting]]).
- Distinguishes event-time windowing and watermark-driven bucket closing (from stream
  processing fundamentals) from the counting-structure choice — a design can get windows
  right and still pick the wrong counting structure ([[async-event-time-watermarks]],
  [[async-window-types]]).
- Describes how the design absorbs 10x event volume without the counting structures' memory
  exploding, and identifies the merge fan-in as the actual new bottleneck
  ([[problems-top-k-10x-tree-merge]]).

**Solution**: [[solution-top-k]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
