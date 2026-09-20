---
nodes: [problems.geo.proximity, storage.relational.indexing]
tags: [problem]
---
# Drill: Design a proximity search service like Yelp

Design the backend for a Yelp-like proximity search: users search for nearby businesses
(restaurants, shops) by location, radius, and optional category, and results are ranked by a
blend of distance and rating. A lightweight "nearby friends" variant also needs to exist,
where a small fraction of users share their live location.

**Constraints to state and honor**
- Roughly 800 peak search QPS and a business index of about twenty million records that
  should comfortably fit in memory on a single node.
- Search reads must stay well under 200ms P99; business location updates are allowed several
  minutes of staleness before being visible in search.
- Results are ranked by distance blended with rating, not pure distance, and pagination must
  stay stable while the candidate set changes underneath it.
- The nearby-friends variant refreshes locations roughly every 15 seconds and must not carry
  stale positions forward once a user goes offline.

**Grading points**
- Chooses an in-memory, density-adaptive spatial index (quadtree) for the read-heavy business
  index over a uniform geohash grid, and explains the concrete size/density argument for why
  it fits in memory and adapts to skewed density ([[problems-proximity-index-fits-in-memory]],
  [[problems-proximity-geohash-vs-quadtree-density]]).
- Explains why a blended distance+rating score forces a two-stage design — widen the spatial
  candidate set, then re-rank — and why pagination needs a composite cursor rather than a
  plain offset ([[problems-proximity-two-stage-ranking-composite-cursor]]).
- Can compare geohash's Z-order curve against S2's Hilbert curve or H3's hexagonal grid and
  say precisely what each buys over plain geohash ([[problems-proximity-s2-hilbert-vs-geohash-zorder]],
  [[problems-proximity-h3-uniform-neighbor-distance]]).
- Designs the nearby-friends variant around a TTL-based cache and a pull query model instead
  of reusing the business index's batch-rebuild approach, and justifies the choice against the
  location update rate ([[problems-proximity-nearby-friends-pull-vs-push]]).
- States a concrete degradation path for an index-rebuild failure that keeps search serving
  from the last good snapshot instead of erroring or falling back to a raw database scan
  ([[problems-proximity-double-buffer-index-outage]]).
- Describes how the design changes at 10x scale when the index no longer fits on one machine,
  including how boundary queries are handled across shards
  ([[problems-proximity-10x-geo-sharding-boundary]]).
- Connects the choice of spatial index back to how a plain B-tree index over raw latitude and
  longitude columns fails to serve a 2D range query efficiently, the way a composite B-tree
  index only helps a query that respects its leftmost-prefix order
  ([[storage-index-leftmost-prefix]]).

**Solution**: [[solution-proximity]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
